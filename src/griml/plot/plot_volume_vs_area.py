import numpy as np
import geopandas as gp
import matplotlib as mpl
import matplotlib.pyplot as plt
import scipy.stats
from sklearn.metrics import mean_squared_error

# Set the font family to sans-serif
mpl.rcParams['font.family'] = 'sans-serif'

# Specify "Arial" as the font to use for the sans-serif family
mpl.rcParams['font.sans-serif'] = ['Arial']

# Optional: You can also set a default font size
mpl.rcParams['font.size'] = 10

# %%
f = 'misc/iml_2016-2025/final_v4/with_volumes/ALL-ESA-GRIML-IML-fv4-with-va-volumes.gpkg'
out_dir = 'misc/iml_2016-2025/figures/'
gdf = gp.read_file(f)

# -------------------------
# Split data by margin type
# -------------------------
gdf_clean = gdf[["area_all", "volume_km3", "margin"]].dropna()
gdf_clean = gdf_clean[(gdf_clean["area_all"] > 0) & (gdf_clean["volume_km3"] > 0)]

ice_sheet = gdf_clean[gdf_clean["margin"] == "ICE_SHEET"]
ice_cap   = gdf_clean[gdf_clean["margin"] == "ICE_CAP"]

# Font size for titles
fsize1 = 12
fsize2 = 11

# Colors (match your original style)
c_sheet = '#3589bc'
c_cap   = '#FFFFFF'
edge    = '#666699'

# -------------------------
# Helper: fit model
# -------------------------
def fit(x, y):
    m, b, r, *_ = scipy.stats.linregress(x, y)
    return m, b, r**2

# Fits for all
m_all, b_all, r2_all = fit(gdf_clean["area_all"], gdf_clean["volume_km3"])

# Fits per group
m_s, b_s, r2_s = fit(ice_sheet["area_all"], ice_sheet["volume_km3"])
m_c, b_c, r2_c = fit(ice_cap["area_all"], ice_cap["volume_km3"])

# -------------------------
# Figure layout
# -------------------------
fig, axes = plt.subplots(1, 2, figsize=(10, 5))
(axB, axC) = axes
#fig.patch.set_edgecolor("#666666")
#fig.patch.set_linewidth(3)

# -------------------------
# (B) Scatter + regression
# -------------------------
axB.scatter(ice_sheet["area_all"], ice_sheet["volume_km3"],
            color=c_sheet, edgecolor=edge, alpha=0.5, label="Ice Sheet margin")

axB.scatter(ice_cap["area_all"], ice_cap["volume_km3"],
            color=c_cap, edgecolor=edge, alpha=0.9, label="PGIC margin")

# Regression lines
xfit = np.linspace(gdf_clean["area_all"].min(),
                   gdf_clean["area_all"].max(), 200)

axB.plot(xfit, m_all * xfit + b_all, color='k', linestyle='-', linewidth=1.5, label=f"All lakes $R^2$ = {r2_all:.2f}")
axB.plot(xfit, m_s * xfit + b_s, color=c_sheet, linestyle='--', linewidth=1.5, label=f"Ice Sheet $R^2$ = {r2_s:.2f}")
axB.plot(xfit, m_c * xfit + b_c, color=edge, linestyle='--', linewidth=1.5, label=f"PGIC $R^2$ = {r2_c:.2f}")

axB.set_xlabel("Area (km$^2$, log scale)", fontsize=fsize2)
axB.set_ylabel("Volume (Gt, log scale)", fontsize=fsize2)
axB.set_title("a. Ice-marginal lake area vs. volume", fontsize=fsize1, fontweight="bold")

axB.legend(loc=4)
# Optional: cleaner legend (only show once in panel A)

# -------------------------
# (C) Mean depth by group
# -------------------------
depth_s = (ice_sheet["volume_km3"] / ice_sheet["area_all"]) * 1000
depth_c = (ice_cap["volume_km3"]   / ice_cap["area_all"]) * 1000

axC.scatter(ice_sheet["area_all"], depth_s,
            color=c_sheet, edgecolor=edge, alpha=0.5)

axC.scatter(ice_cap["area_all"], depth_c,
            color=c_cap, edgecolor=edge, alpha=0.9)

axC.set_xlabel("Area (km$^2$, log scale)", fontsize=fsize2)
axC.set_ylabel("Mean depth (m)", fontsize=fsize2)
axC.set_title("b. Ice-marginal lake depth variability", fontsize=fsize1, fontweight="bold")

# -------------------------
# Styling
# -------------------------
for ax in axes.flatten():
    ax.grid(True, linestyle='dashed', linewidth=0.5, alpha=0.5)
    ax.set_axisbelow(True)

axB.set_xscale('log')
axC.set_xscale('log')

# Only log y where appropriate
axB.set_yscale('log')
#axC.set_yscale('log')

plt.tight_layout()
# plt.show()
plt.savefig(out_dir + "lake_area_vs_volume.png", transparent=False, dpi=300)
