"""
Sensitivity of the volume-area relationship to the input volume data.

The bootstrap in get_v_a_prediction.py resamples which calibration lakes are
drawn, holding the observed volumes fixed. It therefore quantifies sampling
variability in the calibration set composition, and nothing else. This script
covers the uncertainty the bootstrap cannot see:

    Test 1  Construction     - observed V is a prism (dh * A), so area sits on
                               both sides of the regression. Quantifies how much
                               of the apparent fit is constructional.
    Test 2  Coverage         - the 1/coverage correction applied to observed
                               volumes, and how the total responds to it.
    Test 3  Errors-in-vars   - measurement error on dh propagates 1:1 into V,
                               which attenuates the fitted exponent. Monte Carlo
                               plus SIMEX for a noise-corrected exponent.
    Test 4  Extrapolation    - the inventory extends well beyond the calibration
                               area range, and those lakes dominate the total.
    Test 5  Fitting space    - NLS on raw values vs log-space OLS, with and
                               without the Duan smearing retransformation.

    Reference               - the existing bootstrap and a leave-one-out pass,
                               reproduced here so every variant is comparable
                               against the same baseline.

Outputs:
    sensitivity_v_a_summary.csv      one row per variant
    sensitivity_v_a_tornado.png      total volume response to each variant
    sensitivity_v_a_construction.png drop-height reframing and the null test
"""

import warnings

import geopandas as gpd
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.optimize import curve_fit
from scipy.stats import linregress

warnings.filterwarnings("ignore")

# ------------------------------------------------------------------
# CONFIGURATION
# ------------------------------------------------------------------
inventory_path = (
    "misc/iml_2016-2025/final_v4/"
    "ALL-ESA-GRIML-IML-fv4.gpkg"
)
validation_path = (
    "misc/lake_volumes/GLOF_lake_volumes_all.csv"
)

out_csv = "sensitivity_v_a_summary.csv"
out_tornado = "sensitivity_v_a_tornado.png"
out_construction = "sensitivity_v_a_construction.png"

# Monte Carlo / resampling sizes
n_boot = 1000
n_shuffle = 2000
n_mc = 1000
n_simex = 200

seed = 42

# ArcticDEM strip vertical error budget (m).
# The random component averages down over the n strips stacked per epoch;
# the bias component is a per-epoch datum offset that does not.
sigma_strip_random = 2.0
sigma_strip_bias = 1.0

# Uncertainty on the 1/coverage extrapolation, as a fraction of the corrected
# volume. Scales with the unobserved fraction: a lake at coverage 1.0 carries
# none, a lake at coverage 0.4 carries 0.5 * 0.6 = 30%.
coverage_alpha = 0.5

# Fitted exponent from the current model, used as the curve_fit starting point
p0 = (0.05, 1.3)


# ------------------------------------------------------------------
# MODEL AND FITTING HELPERS
# ------------------------------------------------------------------
def power_law(A, k, b):
    return k * A ** b


def fit_nls(A, V, p0=p0):
    """Nonlinear least squares on raw values. The current production fit."""
    pars, cov = curve_fit(
        power_law,
        A,
        V,
        p0=p0,
        bounds=([0, 0], [np.inf, np.inf]),
        maxfev=20000,
    )
    return pars[0], pars[1], cov


def fit_log(A, V, smearing=False):
    """
    OLS in log10 space.

    Back-transforming a log-space fit with 10**intercept predicts the median,
    not the mean, and so under-predicts a total. The Duan smearing estimator
    corrects this by folding the mean residual factor into k.
    """
    result = linregress(np.log10(A), np.log10(V))

    k = 10 ** result.intercept
    b = result.slope

    if smearing:
        residual = np.log10(V) - np.log10(power_law(A, k, b))
        k = k * np.mean(10 ** residual)

    return k, b, result


def total_volume(k, b, areas):
    return float(np.sum(power_law(areas, k, b)))


def corrected_volume(volume, coverage, cap=None, apply_above_one=False):
    """
    Scale observed volumes for partial strip coverage.

    volume          observed volume over the covered fraction (km3)
    coverage        observed fraction of the lake polygon
    cap             maximum inflation factor, or None for uncapped
    apply_above_one whether to also rescale lakes reporting coverage > 1

    The production code divides by coverage when 0 < coverage <= 1 and passes
    coverage > 1 through untouched, which is reproduced by the defaults.
    """
    volume = np.asarray(volume, dtype=float)
    coverage = np.asarray(coverage, dtype=float)

    factor = np.ones_like(volume)

    if apply_above_one:
        mask = coverage > 0
    else:
        mask = (coverage > 0) & (coverage <= 1.0)

    factor[mask] = 1.0 / coverage[mask]

    if cap is not None:
        factor = np.minimum(factor, cap)

    return volume * factor


def area_error_fraction(area):
    """
    Lake area uncertainty, as in the Monte Carlo block of get_v_a_prediction.py.
    10% below 0.2 km2, 1% above 5 km2, linear between.
    """
    area = np.asarray(area, dtype=float)

    frac = 0.10 - ((area - 0.2) / (5 - 0.2)) * (0.10 - 0.01)

    return np.clip(frac, 0.01, 0.10)


def lognormal_sigma(fraction):
    """Convert a fractional 1-sigma error to a log-space sigma."""
    return np.sqrt(np.log1p(np.asarray(fraction, dtype=float) ** 2))


# ------------------------------------------------------------------
# LOAD DATA
# ------------------------------------------------------------------
print("Loading inventory and validation data")

gdf = gpd.read_file(inventory_path)

df = pd.read_csv(validation_path)

filtered_df = df[
    (df["filled_verified"] == "yes") & (df["drained_verified"] == "yes")
]

merged_df = pd.merge(filtered_df, gdf, on="lake_id", how="left")

merged_df = merged_df[
    [
        "lake_id",
        "area_all",
        "volume_km3",
        "volume_coverage",
        "elevation_difference",
        "n_filled_strips",
        "n_drained_strips",
    ]
].dropna(subset=["area_all", "volume_km3", "volume_coverage"])

# Baseline calibration volumes, exactly as the production code builds them
merged_df["volume_km3_all"] = corrected_volume(
    merged_df["volume_km3"],
    merged_df["volume_coverage"],
)

A_cal = merged_df["area_all"].values
V_cal = merged_df["volume_km3_all"].values
dh_cal = merged_df["elevation_difference"].values

A_inv = gdf["area_all"].values

print(f"  calibration lakes : {len(merged_df)}")
print(f"  inventory lakes   : {len(gdf)}")
print(
    f"  calibration area  : {A_cal.min():.3f} - {A_cal.max():.2f} km2"
)
print(f"  inventory area    : {A_inv.min():.3f} - {A_inv.max():.2f} km2")

# Baseline: the current production model
k_base, b_base, cov_base = fit_nls(A_cal, V_cal)
total_base = total_volume(k_base, b_base, A_inv)

print(f"\nBaseline (NLS on raw values): V = {k_base:.4f} A^{b_base:.3f}")
print(f"Baseline total: {total_base:.1f} km3")

rows = []


def record(group, variant, k, b, total, note=""):
    rows.append(
        {
            "group": group,
            "variant": variant,
            "k": k,
            "b": b,
            "total_km3": total,
            "pct_change": 100 * (total - total_base) / total_base,
            "note": note,
        }
    )


record("baseline", "Current: NLS on raw values", k_base, b_base, total_base)


# ------------------------------------------------------------------
# TEST 1 - CONSTRUCTION
# ------------------------------------------------------------------
# The observed volume is a prism, V = dh * A. Area therefore appears on both
# sides of the V-A regression, which generates a strong apparent power law even
# when dh carries no information about area. The null is built by shuffling dh
# against area, which destroys any real depth-area link while preserving the
# V = dh * A construction.
# ------------------------------------------------------------------
print("\n" + "-" * 66)
print("TEST 1  Construction")
print("-" * 66)

rng = np.random.default_rng(seed)

# Confirm the prism construction
implied_area = (merged_df["volume_km3"].values * 1e9) / dh_cal / 1e6
prism_ratio = implied_area / A_cal

print(
    f"Implied area from V/dh vs area_all: median ratio {np.median(prism_ratio):.3f}"
)

# Observed relationship
obs_fit = linregress(np.log10(A_cal), np.log10(V_cal))
obs_slope = obs_fit.slope
obs_r2 = obs_fit.rvalue ** 2

# The independent signal: does drop height scale with area?
dh_fit = linregress(np.log10(A_cal), np.log10(dh_cal))

dh_boot_slopes = []
idx = np.arange(len(A_cal))

for _ in range(n_boot):
    s = rng.choice(idx, size=len(idx), replace=True)
    dh_boot_slopes.append(
        linregress(np.log10(A_cal[s]), np.log10(dh_cal[s])).slope
    )

dh_boot_slopes = np.array(dh_boot_slopes)
dh_lo, dh_hi = np.percentile(dh_boot_slopes, [2.5, 97.5])

# Construction null
null_slopes = []

for _ in range(n_shuffle):
    V_null = rng.permutation(dh_cal) * A_cal
    null_slopes.append(linregress(np.log10(A_cal), np.log10(V_null)).slope)

null_slopes = np.array(null_slopes)
null_lo, null_hi = np.percentile(null_slopes, [2.5, 97.5])

print(f"\nObserved log-log V-A : slope {obs_slope:.3f}, R2 {obs_r2:.3f}")
print(
    f"Construction null    : slope {null_slopes.mean():.3f} "
    f"[{null_lo:.3f}, {null_hi:.3f}]"
)
print(
    f"  -> observed slope is "
    f"{'OUTSIDE' if obs_slope > null_hi or obs_slope < null_lo else 'INSIDE'}"
    f" the null interval"
)

print(
    f"\nDrop height vs area  : log10(dh) = {dh_fit.slope:.3f} log10(A) "
    f"+ {dh_fit.intercept:.3f}"
)
print(
    f"  R2 {dh_fit.rvalue ** 2:.3f}, p {dh_fit.pvalue:.3g}, "
    f"95% CI on slope [{dh_lo:.3f}, {dh_hi:.3f}]"
)
print(
    f"  -> implied exponent b = 1 + {dh_fit.slope:.3f} = {1 + dh_fit.slope:.3f}"
)
print(
    f"  -> genuine explanatory power is R2 {dh_fit.rvalue ** 2:.3f}, "
    f"not the {obs_r2:.3f} of the V-A fit"
)

k_dh = 10 ** dh_fit.intercept * 1e6 / 1e9
b_dh = 1 + dh_fit.slope
record(
    "construction",
    "Reframed via drop height (dh ~ A)",
    k_dh,
    b_dh,
    total_volume(k_dh, b_dh, A_inv),
    f"dh R2={dh_fit.rvalue ** 2:.3f}",
)


# ------------------------------------------------------------------
# TEST 2 - COVERAGE CORRECTION
# ------------------------------------------------------------------
# The 1/coverage scaling assumes the unobserved fraction of a lake has the same
# mean depth as the observed fraction. Median coverage is around 0.7, so the
# typical calibration volume is inflated by roughly 40%.
# ------------------------------------------------------------------
print("\n" + "-" * 66)
print("TEST 2  Coverage correction")
print("-" * 66)

coverage = merged_df["volume_coverage"].values
volume_raw = merged_df["volume_km3"].values

print(
    f"Coverage: median {np.median(coverage):.3f}, "
    f"min {coverage.min():.3f}, "
    f"{(coverage > 1).sum()} lakes above 1.0"
)

coverage_variants = [
    ("No coverage correction", dict(cap=1.0)),
    ("Correction capped at 1.5x", dict(cap=1.5)),
    ("Correction capped at 2.0x", dict(cap=2.0)),
    ("Uncapped (current)", dict(cap=None)),
    ("Uncapped, also applied to cov>1", dict(cap=None, apply_above_one=True)),
]

for name, kwargs in coverage_variants:
    V_var = corrected_volume(volume_raw, coverage, **kwargs)
    k, b, _ = fit_nls(A_cal, V_var)
    record("coverage", name, k, b, total_volume(k, b, A_inv))
    print(f"  {name:34s} b={b:.3f}  total={total_volume(k, b, A_inv):7.1f} km3")

# Coverage thresholds. These are confounded with area: coverage anti-correlates
# with lake size, so a high-coverage subset is also an area-truncated subset.
# The matched area-truncated control isolates which effect is responsible.
cov_area_r = linregress(np.log10(A_cal), coverage)
print(
    f"\nCoverage vs log area: r={cov_area_r.rvalue:.3f}, p={cov_area_r.pvalue:.3g}"
    " (subsets below are confounded with area range)"
)

for thresh in [0.5, 0.6, 0.7, 0.8]:
    mask = coverage >= thresh

    if mask.sum() < 15:
        continue

    k, b, _ = fit_nls(A_cal[mask], V_cal[mask])
    total = total_volume(k, b, A_inv)
    record(
        "coverage",
        f"Coverage >= {thresh} only (n={mask.sum()})",
        k,
        b,
        total,
        f"area range {A_cal[mask].min():.2f}-{A_cal[mask].max():.2f}",
    )

    # Area-matched control: same area range, no coverage filter
    control = (A_cal >= A_cal[mask].min()) & (A_cal <= A_cal[mask].max())
    k_c, b_c, _ = fit_nls(A_cal[control], V_cal[control])
    total_c = total_volume(k_c, b_c, A_inv)
    record(
        "coverage",
        f"Area-matched control for cov>={thresh} (n={control.sum()})",
        k_c,
        b_c,
        total_c,
        "isolates range restriction from data quality",
    )

    print(
        f"  cov>={thresh}: b={b:.3f} total={total:7.1f} | "
        f"area-matched control: b={b_c:.3f} total={total_c:7.1f}"
    )


# ------------------------------------------------------------------
# TEST 3 - ERRORS IN VARIABLES
# ------------------------------------------------------------------
# V = dh * A / coverage, so error in dh propagates directly into V. The smallest
# drop heights are only a few times the strip error, which makes the y-error
# strongly heteroscedastic and biases the fitted exponent toward zero
# (regression attenuation). SIMEX estimates the noise-free exponent by adding
# further known noise and extrapolating back.
# ------------------------------------------------------------------
print("\n" + "-" * 66)
print("TEST 3  Errors in variables")
print("-" * 66)

n_f = merged_df["n_filled_strips"].fillna(1).clip(lower=1).values
n_d = merged_df["n_drained_strips"].fillna(1).clip(lower=1).values

sigma_dh = np.sqrt(
    sigma_strip_random ** 2 / n_f
    + sigma_strip_random ** 2 / n_d
    + 2 * sigma_strip_bias ** 2
)

frac_dh = sigma_dh / dh_cal
frac_cov = coverage_alpha * (1.0 - np.clip(coverage, None, 1.0))
frac_V = np.sqrt(frac_dh ** 2 + frac_cov ** 2)

frac_A = area_error_fraction(A_cal)

print(
    f"Drop height: min {dh_cal.min():.1f} m, median {np.median(dh_cal):.1f} m"
)
print(
    f"sigma(dh)  : median {np.median(sigma_dh):.2f} m "
    f"-> volume error from dh alone: median {100 * np.median(frac_dh):.0f}%, "
    f"max {100 * frac_dh.max():.0f}%"
)
print(
    f"Total volume error fraction: median {100 * np.median(frac_V):.0f}%, "
    f"max {100 * frac_V.max():.0f}%"
)

sigma_ln_V = lognormal_sigma(frac_V)
sigma_ln_A = lognormal_sigma(frac_A)

rng = np.random.default_rng(seed)

mc_k, mc_b, mc_total = [], [], []

for _ in range(n_mc):
    # Multiplicative, median-preserving perturbation
    V_i = V_cal * np.exp(
        rng.normal(0, sigma_ln_V) - 0.5 * sigma_ln_V ** 2
    )
    A_i = A_cal * np.exp(
        rng.normal(0, sigma_ln_A) - 0.5 * sigma_ln_A ** 2
    )

    try:
        k, b, _ = fit_nls(A_i, V_i)
    except RuntimeError:
        continue

    mc_k.append(k)
    mc_b.append(b)
    mc_total.append(total_volume(k, b, A_inv))

mc_b = np.array(mc_b)
mc_total = np.array(mc_total)

eiv_lo, eiv_hi = np.percentile(mc_total, [2.5, 97.5])

print(
    f"\nEIV Monte Carlo ({len(mc_total)} fits): "
    f"b = {np.median(mc_b):.3f} [{np.percentile(mc_b, 2.5):.3f}, "
    f"{np.percentile(mc_b, 97.5):.3f}]"
)
print(
    f"  total = {np.median(mc_total):.1f} km3 "
    f"[{eiv_lo:.1f}, {eiv_hi:.1f}]  "
    f"({100 * (eiv_lo - total_base) / total_base:+.0f}% / "
    f"{100 * (eiv_hi - total_base) / total_base:+.0f}%)"
)

record(
    "errors-in-variables",
    "EIV Monte Carlo, 2.5th percentile",
    np.percentile(mc_k, 2.5),
    np.percentile(mc_b, 2.5),
    eiv_lo,
)
record(
    "errors-in-variables",
    "EIV Monte Carlo, 97.5th percentile",
    np.percentile(mc_k, 97.5),
    np.percentile(mc_b, 97.5),
    eiv_hi,
)

# SIMEX: add noise at increasing levels, then extrapolate back to zero noise
lambdas = np.array([0.0, 0.5, 1.0, 1.5, 2.0])
simex_b = []

for lam in lambdas:
    reps = []

    for _ in range(n_simex):
        s = sigma_ln_V * np.sqrt(lam)
        V_i = V_cal * np.exp(rng.normal(0, s) - 0.5 * s ** 2)

        try:
            _, b, _ = fit_nls(A_cal, V_i)
        except RuntimeError:
            continue

        reps.append(b)

    simex_b.append(np.mean(reps))

simex_b = np.array(simex_b)

# Quadratic extrapolation to lambda = -1 (the zero-noise case)
simex_coef = np.polyfit(lambdas, simex_b, 2)
b_simex = np.polyval(simex_coef, -1.0)

k_simex, _ = curve_fit(
    lambda A, k: power_law(A, k, b_simex),
    A_cal,
    V_cal,
    p0=[k_base],
    bounds=([0], [np.inf]),
    maxfev=20000,
)
k_simex = float(k_simex[0])
total_simex = total_volume(k_simex, b_simex, A_inv)

print(f"\nSIMEX b by noise level: {np.round(simex_b, 3)}")
print(
    f"  noise-corrected b = {b_simex:.3f} "
    f"(fitted b = {b_base:.3f}, attenuation {b_simex - b_base:+.3f})"
)
print(f"  total at corrected b = {total_simex:.1f} km3")

record(
    "errors-in-variables",
    "SIMEX noise-corrected exponent",
    k_simex,
    b_simex,
    total_simex,
    f"attenuation {b_simex - b_base:+.3f}",
)


# ------------------------------------------------------------------
# TEST 4 - EXTRAPOLATION
# ------------------------------------------------------------------
# The calibration set spans a narrower area range than the inventory. Because
# b > 1, the handful of lakes above the calibration maximum carry a large share
# of the total, and that share is where the model is least constrained.
# ------------------------------------------------------------------
print("\n" + "-" * 66)
print("TEST 4  Extrapolation beyond the calibration range")
print("-" * 66)

cal_min, cal_max = A_cal.min(), A_cal.max()

V_inv_base = power_law(A_inv, k_base, b_base)

below = A_inv < cal_min
above = A_inv > cal_max

print(
    f"Calibration range: {cal_min:.3f} - {cal_max:.2f} km2"
)
print(
    f"  below range: {below.sum():4d} lakes ({100 * below.mean():.0f}%), "
    f"{100 * V_inv_base[below].sum() / V_inv_base.sum():.0f}% of total volume"
)
print(
    f"  above range: {above.sum():4d} lakes ({100 * above.mean():.1f}%), "
    f"{100 * V_inv_base[above].sum() / V_inv_base.sum():.0f}% of total volume"
)

record(
    "extrapolation",
    "Exclude lakes above calibration range",
    k_base,
    b_base,
    total_volume(k_base, b_base, A_inv[~above]),
    f"{above.sum()} lakes dropped",
)

# Cap the prediction at the calibration maximum rather than extrapolating
A_capped = np.clip(A_inv, None, cal_max)
record(
    "extrapolation",
    "Cap prediction at calibration max area",
    k_base,
    b_base,
    total_volume(k_base, b_base, A_capped),
    "conservative upper-range treatment",
)

# Calibration truncated to its own upper half, to test range stability
for lo in [0.5, 1.0]:
    mask = A_cal >= lo
    k, b, _ = fit_nls(A_cal[mask], V_cal[mask])
    record(
        "extrapolation",
        f"Calibrate on lakes >= {lo} km2 only (n={mask.sum()})",
        k,
        b,
        total_volume(k, b, A_inv),
    )
    print(
        f"  calibrate on A >= {lo} km2 (n={mask.sum()}): "
        f"b={b:.3f} total={total_volume(k, b, A_inv):7.1f} km3"
    )


# ------------------------------------------------------------------
# TEST 5 - FITTING SPACE
# ------------------------------------------------------------------
# NLS on raw values minimises absolute error, so the largest calibration lakes
# dominate the objective. Log-space OLS weights all lakes proportionally but
# predicts the median unless retransformed.
# ------------------------------------------------------------------
print("\n" + "-" * 66)
print("TEST 5  Fitting space")
print("-" * 66)

k_log, b_log, _ = fit_log(A_cal, V_cal, smearing=False)
k_duan, b_duan, _ = fit_log(A_cal, V_cal, smearing=True)

record("fitting space", "log-OLS, no smearing", k_log, b_log,
       total_volume(k_log, b_log, A_inv))
record("fitting space", "log-OLS + Duan smearing", k_duan, b_duan,
       total_volume(k_duan, b_duan, A_inv))

print(
    f"  NLS on raw values     : k={k_base:.4f} b={b_base:.3f} "
    f"total={total_base:7.1f} km3"
)
print(
    f"  log-OLS, no smearing  : k={k_log:.4f} b={b_log:.3f} "
    f"total={total_volume(k_log, b_log, A_inv):7.1f} km3"
)
print(
    f"  log-OLS + Duan        : k={k_duan:.4f} b={b_duan:.3f} "
    f"total={total_volume(k_duan, b_duan, A_inv):7.1f} km3"
)
print(f"  Duan smearing factor  : {k_duan / k_log:.3f}")


# ------------------------------------------------------------------
# REFERENCE - EXISTING BOOTSTRAP AND LEAVE-ONE-OUT
# ------------------------------------------------------------------
print("\n" + "-" * 66)
print("REFERENCE  Existing bootstrap and leave-one-out")
print("-" * 66)

rng = np.random.default_rng(seed)

boot_df = merged_df.copy()
boot_df["size_class"] = pd.qcut(boot_df["area_all"], 5, labels=False)

boot_totals, boot_b = [], []

for _ in range(n_boot):
    sample = (
        boot_df.groupby("size_class")
        .apply(
            lambda x: x.sample(
                n=len(x), replace=True, random_state=rng.integers(1e9)
            )
        )
        .reset_index(drop=True)
    )

    try:
        k, b, _ = fit_nls(sample["area_all"].values, sample["volume_km3_all"].values)
    except RuntimeError:
        continue

    boot_totals.append(total_volume(k, b, A_inv))
    boot_b.append(b)

boot_totals = np.array(boot_totals)
boot_lo, boot_hi = np.percentile(boot_totals, [2.5, 97.5])

print(
    f"Bootstrap 95% CI : {boot_lo:.1f} - {boot_hi:.1f} km3 "
    f"({100 * (boot_lo - total_base) / total_base:+.0f}% / "
    f"{100 * (boot_hi - total_base) / total_base:+.0f}%)"
)
print(
    f"Bootstrap b 95%  : {np.percentile(boot_b, 2.5):.3f} - "
    f"{np.percentile(boot_b, 97.5):.3f}"
)

record("reference", "Bootstrap 2.5th percentile", np.nan,
       np.percentile(boot_b, 2.5), boot_lo)
record("reference", "Bootstrap 97.5th percentile", np.nan,
       np.percentile(boot_b, 97.5), boot_hi)

# Leave-one-out
loo_totals, loo_b = [], []

for i in range(len(merged_df)):
    keep = np.arange(len(merged_df)) != i

    try:
        k, b, _ = fit_nls(A_cal[keep], V_cal[keep])
    except RuntimeError:
        continue

    loo_totals.append(total_volume(k, b, A_inv))
    loo_b.append(b)

loo_totals = np.array(loo_totals)
loo_b = np.array(loo_b)

worst = int(np.argmax(np.abs(loo_totals - total_base)))

print(
    f"Leave-one-out    : total {loo_totals.min():.1f} - {loo_totals.max():.1f} km3 "
    f"({100 * (loo_totals.min() - total_base) / total_base:+.0f}% / "
    f"{100 * (loo_totals.max() - total_base) / total_base:+.0f}%)"
)
print(f"                   b {loo_b.min():.3f} - {loo_b.max():.3f}")
print(
    f"Most influential : lake_id {merged_df['lake_id'].iloc[worst]} "
    f"({A_cal[worst]:.2f} km2, {V_cal[worst]:.4f} km3) -> "
    f"{100 * (loo_totals[worst] - total_base) / total_base:+.0f}%"
)

record("reference", "Leave-one-out minimum", np.nan, loo_b[np.argmin(loo_totals)],
       loo_totals.min())
record("reference", "Leave-one-out maximum", np.nan, loo_b[np.argmax(loo_totals)],
       loo_totals.max())


# ------------------------------------------------------------------
# SUMMARY TABLE
# ------------------------------------------------------------------
summary = pd.DataFrame(rows)
summary.to_csv(out_csv, index=False)

print("\n" + "=" * 66)
print("SUMMARY")
print("=" * 66)
print(
    summary[["group", "variant", "b", "total_km3", "pct_change"]].to_string(
        index=False,
        float_format=lambda x: f"{x:.3f}",
    )
)

sens = summary[~summary["group"].isin(["baseline", "reference"])]

print(
    f"\nBootstrap spread          : "
    f"{100 * (boot_lo - total_base) / total_base:+.0f}% to "
    f"{100 * (boot_hi - total_base) / total_base:+.0f}%"
)
print(
    f"Input-data variant spread : "
    f"{sens['pct_change'].min():+.0f}% to {sens['pct_change'].max():+.0f}%"
)
print(f"\nSaved {out_csv}")


# ------------------------------------------------------------------
# FIGURE 1 - TORNADO
# ------------------------------------------------------------------
mpl.rcParams["font.family"] = "sans-serif"
mpl.rcParams["font.sans-serif"] = ["Arial"]
mpl.rcParams["font.size"] = 11

col_up = "#408CBD"
col_down = "#C85A3C"
line_col = "#959BA1"
surface = "#f2f2f2"

plot_df = sens.sort_values("pct_change")

fig, ax = plt.subplots(figsize=(11, 0.42 * len(plot_df) + 2.2))

y = np.arange(len(plot_df))
vals = plot_df["pct_change"].values

# Bootstrap CI shown as a reference band, so the comparison the figure exists
# to make is visible without reading the caption
ax.axvspan(
    100 * (boot_lo - total_base) / total_base,
    100 * (boot_hi - total_base) / total_base,
    color=line_col,
    alpha=0.22,
    lw=0,
    label="Existing bootstrap 95% CI",
    zorder=1,
)

ax.barh(
    y,
    vals,
    color=[col_up if v >= 0 else col_down for v in vals],
    height=0.62,
    zorder=3,
)

ax.axvline(0, color="#4a4a4a", lw=1.2, zorder=4)

for yi, v in zip(y, vals):
    offset = 1.2 if v >= 0 else -1.2
    ax.text(
        v + offset,
        yi,
        f"{v:+.0f}%",
        va="center",
        ha="left" if v >= 0 else "right",
        fontsize=9,
        color="#3a3a3a",
        zorder=5,
    )

ax.set_yticks(y)
ax.set_yticklabels(plot_df["variant"], fontsize=9)

ax.set_xlabel("Change in Greenland total lake volume (%)")
ax.set_title(
    f"Sensitivity of total lake volume to input volume data\n"
    f"baseline = {total_base:.0f} km³ (NLS on raw values, V = "
    f"{k_base:.4f} A$^{{{b_base:.3f}}}$)",
    fontweight="bold",
    loc="left",
)

pad = 0.12 * (vals.max() - vals.min())
ax.set_xlim(vals.min() - pad, vals.max() + pad)
ax.set_ylim(-0.8, len(plot_df) - 0.2)

# Identity is not carried by colour alone: every bar is direct-labelled and
# named on the y axis. The legend covers the one band that is not a bar.
ax.legend(loc="lower right", frameon=False, fontsize=9)

ax.set_axisbelow(True)
ax.xaxis.grid(color="gray", linestyle="dashed", linewidth=0.5)
ax.set_facecolor(surface)

for spine in ["top", "right", "left"]:
    ax.spines[spine].set_visible(False)

plt.tight_layout()
plt.savefig(out_tornado, dpi=300, bbox_inches="tight")
print(f"Saved {out_tornado}")


# ------------------------------------------------------------------
# FIGURE 2 - CONSTRUCTION
# ------------------------------------------------------------------
fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, figsize=(13, 5.2))

# Panel a: the independent signal
ax1.scatter(A_cal, dh_cal, c=col_up, s=45, alpha=0.6, label="Calibration lakes")

A_plot = np.logspace(np.log10(A_cal.min()), np.log10(A_cal.max()), 200)

ax1.plot(
    A_plot,
    10 ** dh_fit.intercept * A_plot ** dh_fit.slope,
    c=col_up,
    lw=2,
    label=(
        f"Δh = {10 ** dh_fit.intercept:.1f} A$^{{{dh_fit.slope:.2f}}}$, "
        f"R² = {dh_fit.rvalue ** 2:.2f}"
    ),
)

ax1.fill_between(
    A_plot,
    10 ** dh_fit.intercept * A_plot ** dh_lo,
    10 ** dh_fit.intercept * A_plot ** dh_hi,
    color=col_up,
    alpha=0.15,
    lw=0,
    label="95% CI on exponent",
)

ax1.set_xscale("log")
ax1.set_yscale("log")
ax1.set_xlabel("Lake area (km²)")
ax1.set_ylabel("Drainage drop height, Δh (m)")
ax1.set_title(
    "a. The independent signal: drop height vs area",
    fontweight="bold",
    loc="left",
)
ax1.legend(loc="upper left", frameon=False, fontsize=9)

# Panel b: how much of the V-A fit is constructional
ax2.hist(
    null_slopes,
    bins=45,
    color=line_col,
    alpha=0.75,
    label=f"Null: Δh shuffled ({n_shuffle} draws)",
)

ax2.axvline(
    obs_slope,
    color=col_down,
    lw=2.5,
    label=f"Observed slope = {obs_slope:.2f}",
)

ax2.axvline(
    1.0,
    color="#4a4a4a",
    lw=1.2,
    linestyle="--",
    label="Slope 1 (pure construction)",
)

ax2.set_xlabel("Fitted log-log V–A slope")
ax2.set_ylabel("Count")
ax2.set_title(
    "b. Construction null for the V–A slope",
    fontweight="bold",
    loc="left",
)
ax2.legend(loc="upper left", frameon=False, fontsize=9)

ax2.set_xlim(
    min(null_slopes.min(), obs_slope) - 0.05,
    max(null_slopes.max(), obs_slope) + 0.05,
)

# Anchored lower left, clear of both the legend and the observed-slope line
ax2.text(
    0.02,
    0.46,
    f"V = Δh · A, so area is on\nboth sides of the fit.\n\n"
    f"V–A R² = {obs_r2:.2f}\nΔh–A R² = {dh_fit.rvalue ** 2:.2f}",
    transform=ax2.transAxes,
    ha="left",
    va="top",
    fontsize=9,
    color="#3a3a3a",
)

for a in [ax1, ax2]:
    a.set_axisbelow(True)
    a.yaxis.grid(color="gray", linestyle="dashed", linewidth=0.5)
    a.set_facecolor(surface)
    for spine in ["top", "right"]:
        a.spines[spine].set_visible(False)

plt.tight_layout()
plt.savefig(out_construction, dpi=300, bbox_inches="tight")
print(f"Saved {out_construction}")

plt.show()
