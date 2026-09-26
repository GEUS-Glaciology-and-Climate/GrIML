import geopandas as gpd
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import r2_score
from sklearn.metrics import mean_squared_error
from scipy.optimize import curve_fit
from scipy.stats import linregress

gdf = gpd.read_file("misc/iml_2016-2025/final_v4/ALL-ESA-GRIML-IML-fv4.gpkg")
out = "misc/iml_2016-2025/final_v4/with_volumes/ALL-ESA-GRIML-IML-fv4_with_va_estimates.gpkg"
out_pt = "misc/iml_2016-2025/final_v4/with_volumes/ALL-ESA-GRIML-IML-fv4_with_va_estimates_pts.gpkg"

# ------------------------------------------------------------------
# Volume validation
# From GLOF volumes derived from ArcticDEM strip data
# ------------------------------------------------------------------

# Load validation file
df = pd.read_csv("misc/lake_volumes/GLOF_lake_volumes_all.csv")
print(len(df))

filtered_df = df[(df["filled_verified"] == "yes") & (df["drained_verified"] == "yes")]
filtered_df["calibration"] = "yes"
print(len(filtered_df))

merged_df = pd.merge(filtered_df, gdf, on="lake_id", how="left")
merged_df = merged_df[["lake_id",
                       "margin",
                       "filled_date",
                       "drained_date",
                       "calibration",
                       "area_all",
                       "volume_km3",
                       "volume_coverage"]]

volume_dem = list(merged_df["volume_km3"])
coverage = list(merged_df["volume_coverage"])

volume_km3_all = []
for a,b in zip(volume_dem, coverage):
    if b > 1.0:
        volume_km3_all.append(a)
    elif b > 0:
        volume_km3_all.append(a / b)
    else:
        volume_km3_all.append(np.nan)

merged_df["volume_km3_all"] = volume_km3_all
print(merged_df.columns)

# Fit in log-log space
logA = np.log10(merged_df["area_all"])
logV = np.log10(merged_df["volume_km3_all"])

slope, intercept = np.polyfit(logA, logV, 1)

# Smooth x values
A_fit = np.logspace(
    np.log10(merged_df["area_all"].min()),
    np.log10(merged_df["area_all"].max()),
    200
)

V_fit = 10**intercept * A_fit**slope


# ------------------------------------------------------------------
# Model analysis based on validation
# ------------------------------------------------------------------
# Model 1 — Log-log linear regression
A = merged_df["area_all"].values          # km²
V = merged_df["volume_km3_all"].values    # km³

# Smooth area values for plotting
A_fit = np.logspace(
    np.log10(A.min()),
    np.log10(A.max()),
    300
)

logA = np.log10(A)
logV = np.log10(V)

result = linregress(logA, logV)
print(result)

slope, intercept = np.polyfit(logA, logV, 1)

V_log = 10**intercept * A_fit**slope

# Model 2 — Nonlinear least squares
def power_law(A, k, b):
    return k * A**b

pars, cov = curve_fit(
    power_law,
    merged_df["area_all"],
    merged_df["volume_km3_all"],
    p0=[10**intercept, slope],
    bounds=([0,0],[np.inf,np.inf])
)
k_fit, b_fit = pars
print(k_fit, b_fit)

V_nls = power_law(A_fit, k_fit, b_fit)

# Model 3 — Published relationship
A_m2 = A_fit * 1e6
V_pub_Mm3 = 4.66e-11 * A_m2**1.76
V_pub_km3 = V_pub_Mm3 / 1000


# ------------------------------------------------------------------
# Compute model stats
# ------------------------------------------------------------------

def model_stats(obs,pred):
    rmse = np.sqrt(mean_squared_error(obs,pred))
    r2 = r2_score(obs,pred)
    log_rmse = np.sqrt(
        mean_squared_error(
            np.log10(obs),
            np.log10(pred)
        )
    )
    return rmse,r2,log_rmse

# log-log model
pred_log = 10**intercept * merged_df["area_all"]**slope

# non-linear model
pred_nls = power_law(merged_df["area_all"],k_fit, b_fit)

# published model
A_m2 = merged_df["area_all"] * 1e6

pred_pub = (
    4.66e-11 * A_m2**1.76
) / 1000
print(model_stats(
    merged_df["volume_km3_all"],
    pred_log
))
print(model_stats(
    merged_df["volume_km3_all"],
    pred_nls
))
print(model_stats(
    merged_df["volume_km3_all"],
    pred_pub
))

merged_df["residual_log"] = (merged_df["volume_km3_all"] - pred_log)
merged_df["residual_nls"] = (merged_df["volume_km3_all"] - pred_nls)
merged_df["residual_pub"] = (merged_df["volume_km3_all"] - pred_pub)


# ------------------------------------------------------------------
# Evaluation by lake size
# ------------------------------------------------------------------
bins = [
    0,
    0.5,
    1,
    5,
    np.inf
]

labels = [
    "<0.5",
    "0.5-1",
    "1-5",
    ">5"
]

merged_df["size_class"] = pd.cut(
    merged_df["area_all"],
    bins=bins,
    labels=labels
)

for cls, group in merged_df.groupby("size_class", observed=False):

    print("\n", cls)
    obs = group["volume_km3_all"]
    pred_log = 10**intercept * group["area_all"]**slope
    pred_nls = power_law(
        group["area_all"],
        k_fit,
        b_fit
    )
    A_m2 = group["area_all"] * 1e6
    pred_pub = (
        4.66e-11 * A_m2**1.76
    ) / 1000

    print( "n lakes:",len(group))
    print("log",model_stats(obs,pred_log))
    print("nls",model_stats(obs,pred_nls))
    print("published",model_stats(obs,pred_pub))


# Single regime model
pars_all,_ = curve_fit(
    power_law,
    merged_df.area_all,
    merged_df.volume_km3_all,
    p0=[0.05,1.3],
    bounds=([0,0],[np.inf,np.inf])
)

print("All:",pars_all)

# ------------------------------------------------------------------
# Bootstrap uncertainty analysis for single power law model
# ------------------------------------------------------------------
n_boot = 1000

rng = np.random.default_rng(42)

boot_coeffs = []
boot_totals = []

merged_df["size_class"] = pd.qcut(
    merged_df.area_all,
    5,
    labels=False
)

for i in range(n_boot):

    sample = (
        merged_df
        .groupby("size_class")
        .apply(
            lambda x: x.sample(
                n=len(x),
                replace=True,
                random_state=rng.integers(1e9)
            )
        )
        .reset_index(drop=True)
    )

    try:

        pars, _ = curve_fit(
            power_law,
            sample.area_all,
            sample.volume_km3_all,
            p0=[k_fit, b_fit],
            bounds=([0,0],[np.inf,np.inf])
        )

    except RuntimeError:
        continue

    boot_coeffs.append(pars)

    k, b = pars

    V = k * gdf.area_all**b

    boot_totals.append(V.sum())

total_lower = np.percentile(boot_totals,2.5)
total_upper = np.percentile(boot_totals,97.5)
total_median = np.percentile(boot_totals,50)

#------------------------------------------------------------------
# Calculate lake volume for all lakes
# ------------------------------------------------------------------
# Model:
# V = k * A^b
# where:
# A = lake area (km²)
# V = lake volume (km³ ≈ Gt)
# Coefficients are fitted above from ArcticDEM GLOF validation lakes
# ------------------------------------------------------------------
k_all, b_all = k_fit, b_fit

gdf["volume_km3"] = np.nan
gdf["volume_method"] = None

gdf["volume_km3"] = (k_all * gdf["area_all"] ** b_all)
gdf["volume_method"] = ("single_powerlaw")

# ------------------------------------------------------------------
# Bootstrap volume estimates for all lakes
# ------------------------------------------------------------------
volume_bootstrap = []

for _, lake in gdf.iterrows():
    area = lake["area_all"]
    estimates = []

    for kx,bx in boot_coeffs:
        v = kx * area**bx
        estimates.append(v)

    volume_bootstrap.append(estimates)

# Median and confidence intervals
gdf["volume_km3_median"] = [ np.median(x) for x in volume_bootstrap ]
gdf["volume_param_lower95"] = [ np.percentile(x,2.5) for x in volume_bootstrap ]
gdf["volume_param_upper95"] = [ np.percentile(x,97.5) for x in volume_bootstrap ]
gdf["volume_uncertainty_method"] = ( "bootstrap_parameter_uncertainty_only" )
gdf["volume_method"] = ( "single_powerlaw_v1" )



# ------------------------------------------------------------------
# Summary
# ------------------------------------------------------------------
best_model = "Nonlinear power law"
print(best_model)
print(f"V = {k_fit:.4f} A^{b_fit:.3f}")

print()

print(f"Total volume = {gdf.volume_km3.sum():.1f} km3")
print(f"Bootstrap median = {gdf.volume_km3_median.sum():.1f} km3")
print(
    f"95% CI = "
    f"{total_lower:.1f}"
    f"–"
    f"{total_upper:.1f} km3"
)

print("Total volume by region")
print(gdf.groupby('region')['volume_km3'].sum())

print("Total volume by margin type")
print(gdf.groupby('margin')['volume_km3'].sum())

print("Total volume by margin and region")
gdf_is = gdf[gdf["margin"]=="ICE_SHEET"]
print(gdf_is.groupby('region')['volume_km3'].sum())
gdf_ic = gdf[gdf["margin"]=="ICE_CAP"]
print(gdf_ic.groupby('region')['volume_km3'].sum())

print("Total volume by GLOF type")
print(gdf.groupby('glof_lake')['volume_km3'].sum())

# ------------------------------------------------------------------
# Save output
# ------------------------------------------------------------------
gdf = gdf.merge(merged_df[["lake_id", "calibration", "volume_km3_all"]], on="lake_id", how="left")
gdf["volume_calibrate"] = gdf["volume_km3_all"]
gdf= gdf[['row_id',
               'lake_id',
               'lake_name',
               'margin',
               'region',
               'volume_km3',
               'volume_calibrate',
               'area_all',
               'area_2016',
               'area_2017',
               'area_2018',
               'area_2019',
               'area_2020',
               'area_2021',
               'area_2022',
               'area_2023',
               'area_2024',
               'area_2025',
               'attached_up_to',
               'length_km',
               'centroid',
               'glof_lake',
               'drain_yrs',
               't_aver_all',
               't_aver_2016',
               't_aver_2017',
               't_aver_2018',
               't_aver_2019',
               't_aver_2020',
               't_aver_2021',
               't_aver_2022',
               't_aver_2023',
               't_aver_2024',
               't_aver_2025',
               't_max_2016',
               't_max_2017',
               't_max_2018',
               't_max_2019',
               't_max_2020',
               't_max_2021',
               't_max_2022',
               't_max_2023',
               't_max_2024',
               't_max_2025',
               't_min_2016',
               't_min_2017',
               't_min_2018',
               't_min_2019',
               't_min_2020',
               't_min_2021',
               't_min_2022',
               't_min_2023',
               't_min_2024',
               't_min_2025',
               't_stdev_2016',
               't_stdev_2017',
               't_stdev_2018',
               't_stdev_2019',
               't_stdev_2020',
               't_stdev_2021',
               't_stdev_2022',
               't_stdev_2023',
               't_stdev_2024',
               't_stdev_2025',
               't_count_2016',
               't_count_2017',
               't_count_2018',
               't_count_2019',
               't_count_2020',
               't_count_2021',
               't_count_2022',
               't_count_2023',
               't_count_2024',
               't_count_2025',
               't_date_2016',
               't_date_2017',
               't_date_2018',
               't_date_2019',
               't_date_2020',
               't_date_2021',
               't_date_2022',
               't_date_2023',
               't_date_2024',
               't_date_2025',
               'startdate',
               'enddate',
               'method',
               'source',
               'calibration',
               'verified',
               'verif_by',
               'edited',
               'edited_by',
               'geometry']]

gdf.to_file(out, driver="GPKG")
print(f"Saved output to: {out}")

gdf_pts = gdf.copy()
gdf_pts["geometry"] = gdf_pts["geometry"].centroid
gdf_pts.to_file(out_pt, driver="GPKG")
print(f"Saved output to: {out_pt}")

# # ------------------------------------------------------------------
# # Monte Carlo uncertainty propagation #1
# # ------------------------------------------------------------------
# #
# # Sources of uncertainty:
# #
# # 1. Lake area uncertainty
# #    - ±10% for lakes <0.2 km²
# #    - ±1% for lakes >5 km²
# #    - linear interpolation between
# #
# # 2. Regression parameter uncertainty
# #    - sampled from covariance matrix of nonlinear fit
# #
# # Output:
# #    volume median
# #    volume 95% uncertainty interval
# #
# # ------------------------------------------------------------------
#
#
# n_mc = 10000
#
# rng = np.random.default_rng(42)
#
#
# # --------------------------------------------------------------
# # Parameter uncertainty
# # --------------------------------------------------------------
#
# parameter_samples = rng.multivariate_normal(
#     mean=pars,
#     cov=cov,
#     size=n_mc
# )
#
#
# # Remove impossible values
# parameter_samples = parameter_samples[
#     (parameter_samples[:,0] > 0) &
#     (parameter_samples[:,1] > 0)
# ]
#
#
# print(
#     "Monte Carlo parameter samples:",
#     len(parameter_samples)
# )
#
#
# # --------------------------------------------------------------
# # Area uncertainty function
# # --------------------------------------------------------------
#
# def area_error_fraction(area):
#
#     if area < 0.2:
#         return 0.10
#
#     elif area > 5:
#         return 0.01
#
#     else:
#         # interpolate between 10% and 1%
#         return (
#             0.10 -
#             (area-0.2)
#             /
#             (5-0.2)
#             *
#             (0.10-0.01)
#         )
#
#
# # --------------------------------------------------------------
# # Monte Carlo volume calculation
# # --------------------------------------------------------------
#
# mc_results = []
#
#
# for area in gdf["area_all"]:
#
#     area_sigma = area_error_fraction(area)
#
#
#     # Sample uncertain areas
#     area_samples = rng.normal(
#         loc=area,
#         scale=area*area_sigma,
#         size=len(parameter_samples)
#     )
#
#
#     # Prevent negative areas
#     area_samples = np.clip(
#         area_samples,
#         0,
#         None
#     )
#
#
#     volumes = []
#
#
#     for (k,b), A in zip(
#         parameter_samples,
#         area_samples
#     ):
#
#         volumes.append(
#             k*A**b
#         )
#
#
#     mc_results.append(
#         volumes
#     )
#
#
# mc_results = np.array(mc_results)
#
#
# # --------------------------------------------------------------
# # Save uncertainty estimates
# # --------------------------------------------------------------
#
# gdf["volume_km3"] = np.percentile(
#     mc_results,
#     50,
#     axis=1
# )
#
#
# gdf["volume_lower95"] = np.percentile(
#     mc_results,
#     2.5,
#     axis=1
# )
#
#
# gdf["volume_upper95"] = np.percentile(
#     mc_results,
#     97.5,
#     axis=1
# )
#
#
# gdf["volume_uncertainty_method"] = (
#     "Monte_Carlo_area_and_parameter_uncertainty"
# )
#
#
# gdf["volume_error_fraction"] = (
#     (
#         gdf["volume_upper95"]
#         -
#         gdf["volume_lower95"]
#     )
#     /
#     (2*gdf["volume_km3"])
# )
#
#
# print(
#     gdf[
#         [
#             "volume_km3",
#             "volume_lower95",
#             "volume_upper95",
#             "volume_error_fraction"
#         ]
#     ].describe()
# )
#
#
# # --------------------------------------------------------------
# # Regional total uncertainty
# # --------------------------------------------------------------
#
# total_volume_mc = mc_results.sum(axis=0)
#
#
# print(
#     "Regional volume median:",
#     np.percentile(total_volume_mc,50)
# )
#
# print(
#     "Regional 95% interval:",
#     np.percentile(total_volume_mc,2.5),
#     "-",
#     np.percentile(total_volume_mc,97.5)
# )
#
#
# # --------------------------------------------------------------
# # Residual uncertainty
# # --------------------------------------------------------------
#
# pred_validation = power_law(
#     merged_df["area_all"],
#     k_fit,
#     b_fit
# )
#
# log_residuals = (
#     np.log10(merged_df["volume_km3_all"])
#     - np.log10(pred_validation)
# )
#
# sigma_log = np.std(log_residuals, ddof=1)
#
# print(f"Residual sigma (log10): {sigma_log:.3f}")
#
#
# # --------------------------------------------------------------
# # Bias correction
# #
# # Multiplicative lognormal noise increases the arithmetic mean.
# # This correction keeps the Monte Carlo centred on the fitted
# # power-law prediction.
# # --------------------------------------------------------------
#
# bias_correction = (
#     sigma_log**2 * np.log(10) / 2
# )
#
# print(f"Bias correction = {bias_correction:.3f}")
#
# # ------------------------------------------------------------------
# # Monte Carlo uncertainty propagation #2
# # Including:
# #
# # 1. Lake area uncertainty
# # 2. Parameter uncertainty (k,b covariance)
# # 3. Residual model uncertainty
# #
# # Model:
# #
# # V = k * A^b * epsilon
# #
# # where:
# # epsilon is multiplicative residual uncertainty
# #
# # ------------------------------------------------------------------
#
# n_mc = 10000
#
# rng = np.random.default_rng(42)
#
#
# # --------------------------------------------------------------
# # 1. Parameter uncertainty
# # --------------------------------------------------------------
#
# # Sample k and b while preserving covariance
#
# parameter_samples = rng.multivariate_normal(
#     mean=pars,
#     cov=cov,
#     size=n_mc
# )
#
#
# # Keep physically valid models
#
# parameter_samples = parameter_samples[
#     (parameter_samples[:,0] > 0) &
#     (parameter_samples[:,1] > 0)
# ]
#
#
# print(
#     "Monte Carlo parameter samples:",
#     len(parameter_samples)
# )
#
#
# # --------------------------------------------------------------
# # 2. Residual uncertainty
# # --------------------------------------------------------------
#
# # Calculate residuals in log space
#
# pred_validation = power_law(
#     merged_df["area_all"],
#     k_fit,
#     b_fit
# )
#
#
# log_residuals = (
#     np.log10(merged_df["volume_km3_all"])
#     -
#     np.log10(pred_validation)
# )
#
#
# sigma_log = np.std(
#     log_residuals,
#     ddof=1
# )
#
#
# print(
#     "Residual sigma (log10 volume):",
#     sigma_log
# )
#
#
# # --------------------------------------------------------------
# # 3. Lake area uncertainty
# # --------------------------------------------------------------
#
# def area_error_fraction(area):
#
#     if area < 0.2:
#
#         return 0.10
#
#     elif area > 5:
#
#         return 0.01
#
#     else:
#
#         # Linear transition
#         return (
#             0.10 -
#             ((area-0.2)/(5-0.2))
#             *
#             (0.10-0.01)
#         )
#
#
# # --------------------------------------------------------------
# # 4. Monte Carlo volume simulation
# # --------------------------------------------------------------
#
# mc_results = []
#
#
# for area in gdf["area_all"]:
#
#
#     # Area uncertainty
#
#     area_sigma = area_error_fraction(area)
#
#
#     area_samples = rng.normal(
#         loc=area,
#         scale=area*area_sigma,
#         size=len(parameter_samples)
#     )
#
#
#     # Avoid negative lake areas
#
#     area_samples = np.clip(
#         area_samples,
#         0.000001,
#         None
#     )
#
#
#     volumes = []
#
#
#     for (k_mc,b_mc), A_mc in zip(
#         parameter_samples,
#         area_samples
#     ):
#
#
#         # Regression prediction
#
#         volume = (
#             k_mc *
#             A_mc**b_mc
#         )
#
#
#         # Add structural model uncertainty
#
#         residual_factor = (
#                 10 ** (
#                 rng.normal(0, sigma_log)
#                 - bias_correction
#         )
#         )
#
#
#         volume *= residual_factor
#
#
#         volumes.append(volume)
#
#
#     mc_results.append(volumes)
#
#
#
# mc_results = np.array(mc_results)
#
#
#
# # --------------------------------------------------------------
# # 5. Save lake-level uncertainty
# # --------------------------------------------------------------
#
# gdf["volume_km3"] = np.percentile(
#     mc_results,
#     50,
#     axis=1
# )
#
#
# gdf["volume_lower95"] = np.percentile(
#     mc_results,
#     2.5,
#     axis=1
# )
#
#
# gdf["volume_upper95"] = np.percentile(
#     mc_results,
#     97.5,
#     axis=1
# )
#
#
# gdf["volume_method"] = (
#     "single_powerlaw_MC"
# )
#
#
# gdf["volume_uncertainty_method"] = (
#     "area_plus_parameter_plus_residual_MC"
# )
#
#
#
# # Relative uncertainty
#
# gdf["volume_error_fraction"] = (
#     (
#         gdf["volume_upper95"]
#         -
#         gdf["volume_lower95"]
#     )
#     /
#     (2*gdf["volume_km3"])
# )
#
#
#
# print(
#     gdf[
#         [
#             "volume_km3",
#             "volume_lower95",
#             "volume_upper95",
#             "volume_error_fraction"
#         ]
#     ].describe()
# )
#
#
#
# # --------------------------------------------------------------
# # 6. Regional uncertainty
# # --------------------------------------------------------------
#
# regional_volume_mc = (
#     mc_results.sum(axis=0)
# )
#
#
# print(
#     "Regional volume median:",
#     np.percentile(
#         regional_volume_mc,
#         50
#     )
# )
#
#
# print(
#     "Regional 95% interval:",
#     np.percentile(
#         regional_volume_mc,
#         2.5
#     ),
#     "-",
#     np.percentile(
#         regional_volume_mc,
#         97.5
#     )
# )

# ------------------------------------------------------------------
# Three-panel model evaluation plot
# ------------------------------------------------------------------
import matplotlib as mpl

# Set the font family to sans-serif
mpl.rcParams['font.family'] = 'sans-serif'

# Specify "Arial" as the font to use for the sans-serif family
mpl.rcParams['font.sans-serif'] = ['Arial']

# Optional: You can also set a default font size
mpl.rcParams['font.size'] = 12

fig, axes = plt.subplots(
    nrows=1,
    ncols=3,
    figsize=(18, 6)
)

ax1, ax2, ax3 = axes

pt_size = 50
pt_alpha = 0.6
pt_col = "#408CBD"
line_col = "#959BA1"

# ==============================================================
# Panel A: Area-volume relationship
# ==============================================================

ax1.scatter(
    merged_df["area_all"],
    merged_df["volume_km3_all"],
    c=pt_col,
    s=pt_size,
    alpha=pt_alpha,
    label="Observed GLOF lakes"
)

A_plot = np.logspace(
    np.log10(merged_df.area_all.min()),
    np.log10(merged_df.area_all.max()),
    300
)

# Nonlinear power law
V_nls_plot = power_law(
    A_plot,
    k_fit,
    b_fit
)

ax1.plot(
    A_plot,
    V_nls_plot,
    lw=2,
    c=pt_col,
    label=f"Power law: V={k_fit:.3g}A$^{{{b_fit:.2f}}}$"
)


# Published relationship
A_m2 = A_plot * 1e6

V_pub_plot = (
    4.66e-11 *
    A_m2**1.76
) / 1000

ax1.plot(
    A_plot,
    V_pub_plot,
    linestyle="--",
    lw=1.5,
    c=line_col,
    label="Global power law"
)


ax1.set_xscale("log")
ax1.set_yscale("log")

ax1.set_xlabel("Lake area (km²)")
ax1.set_ylabel("Lake volume (km³)")
ax1.set_title("a. Volume-area relationship", fontweight="bold")

ax1.legend(loc=2)


# ==============================================================
# Panel B: Observed vs predicted
# ==============================================================

obs = merged_df["volume_km3_all"]

pred = power_law(
    merged_df["area_all"],
    k_fit,
    b_fit
)

ax2.scatter(
    obs,
    pred,
    c=pt_col,
    s=pt_size,
    alpha=pt_alpha,
)


# 1:1 line

lims = [
    min(obs.min(), pred.min()),
    max(obs.max(), pred.max())
]

ax2.plot(
    lims,
    lims,
    linestyle="--",
    lw=1.5,
    c=line_col,
    label="1:1 line"
)


ax2.set_xscale("log")
ax2.set_yscale("log")

ax2.set_xlim(lims)
ax2.set_ylim(lims)

ax2.set_aspect("equal", adjustable="box")

ax2.set_xlabel("Observed volume (km³)")
ax2.set_ylabel("Predicted volume (km³)")

ax2.set_title(
    "b. Observed vs predicted volume",
    fontweight="bold"
)


# Statistics
r2 = r2_score(obs, pred)

log_rmse = np.sqrt(
    mean_squared_error(
        np.log10(obs),
        np.log10(pred)
    )
)

ax2.text(
    0.7,
    0.12,
    f"$R^2$ = {r2:.2f}\n"
    f"log RMSE = {log_rmse:.2f}",
    transform=ax2.transAxes,
    verticalalignment="top"
)

ax2.legend(loc=2)


# ==============================================================
# Panel C: Residual ratio
# ==============================================================

ratio = pred / obs

ax3.scatter(
    merged_df["area_all"],
    ratio,
    c=pt_col,
    s=pt_size,
    alpha=pt_alpha,
)


ax3.axhline(
    1,
    linestyle="--",
    lw = 1.5,
    c = line_col,
)


ax3.set_xscale("log")
ax3.set_yscale("log")


ax3.set_xlabel("Lake area (km²)")
ax3.set_ylabel(
    "Predicted / observed volume"
)

ax3.set_title(
    "c. Residual ratio",
    fontweight="bold"
)


# Add factor-of-two bounds

ax3.axhline(
    2,
    linestyle=":",
    lw=1.5,
    c=line_col,
)

ax3.axhline(
    0.5,
    linestyle=":",
    lw=1.5,
    c=line_col,
)

median_ratio = np.median(ratio)
ax3.axhline(
    median_ratio,
    linestyle="--",
    c=pt_col,
    label=f"Median = {median_ratio:.2f}"
)

ax3.legend(loc=2)

for a in [ax1, ax2, ax3]:
    a.set_axisbelow(True)
    a.yaxis.grid(color='gray', linestyle='dashed', linewidth=0.5)
    a.set_facecolor("#f2f2f2")
plt.tight_layout()

plt.savefig(
    "lake_volume_model_evaluation.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()