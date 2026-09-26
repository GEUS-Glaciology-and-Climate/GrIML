#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pyproj
import glob, re
import numpy as np
import pandas as pd
import geopandas as gpd
import matplotlib as mpl
import matplotlib.pyplot as plt
from pathlib import Path
import matplotlib.lines as mlines
from scipy.stats import linregress, spearmanr
import matplotlib.gridspec as gridspec
# import statsmodels.formula.api as smf

# -------------------------------------------------------------------------
# Define input files
iiml_file = 'misc/iml_2016-2025/final_v4/with_volumes/ALL-ESA-GRIML-IML-fv4-with-va-volumes.gpkg'
indir = 'misc/lake_temperature/2016-2025_inventory/gee_temperature_data/'
infile = glob.glob(indir+'*.csv')
print(infile)

# -------------------------------------------------------------------------
# Check for missing lakes
num = [int(re.findall(r'\d+', str(Path(f).stem))[0]) for f in infile]
res = [ele for ele in range(max(num)+1) if ele not in num]
print('Missing lake ids : ' + str(res))

# -------------------------------------------------------------------------
# Load inventory
iiml = gpd.read_file(iiml_file)
years_range = list(range(2016,2026))

lon_m = [float(i.split(', ')[0]) for i in list(iiml["centroid"])]
lat_m = [float(i.split(', ')[-1]) for i in list(iiml["centroid"])]

transformer = pyproj.Transformer.from_crs(
    "EPSG:3413",
    "EPSG:4326",
    always_xy=True
)

iiml["lon"], iiml["lat"] = transformer.transform(lon_m, lat_m)

# -------------------------------------------------------------------------
# Storage
dfs_st = []

# -------------------------------------------------------------------------
# Figure setup
fig = plt.figure(figsize=(8, 12))
gs = gridspec.GridSpec(3, 2)
ax1 = fig.add_subplot(gs[0, :])
ax2 = fig.add_subplot(gs[1, 0])
ax3 = fig.add_subplot(gs[1, 1])
ax4 = fig.add_subplot(gs[2, :])

# Styling
mpl.rcParams['font.family'] = 'sans-serif'
mpl.rcParams['font.sans-serif'] = ['Arial']
mpl.rcParams['font.size'] = 10
fsize1 = 12
fsize2 = 11

# -------------------------------------------------------------------------
# Loop over files
for f in infile:
    df = pd.read_csv(f, comment='#', index_col=2, parse_dates=True)

    df = df[df['ST'] >= 0]
    df['year'] = df.index.year
    df = df[(df['year'] >= years_range[0]) & (df['year'] <= years_range[-1])]

    df['month'] = df.index.month
    df = df[df['month'] == 8]

    def safe_float(x):
        try:
            return float(str(x).strip('[]'))
        except:
            return np.nan

    df['ST_max_int'] = df['ST_max'].apply(safe_float)
    df['ST_min_int'] = df['ST_min'].apply(safe_float)

    for lake_id in df.lake_id.unique():
        df_set = df[df['lake_id'] == lake_id].sort_index()

        if len(df_set) < 2:
            continue

        df_st = df_set['ST'].resample('YS').mean()
        df_st.index = df_st.index.year

        # Keep lake_id
        df_st = df_st.to_frame(name="ST")
        df_st["lake_id"] = lake_id

        ax1.plot(df_st.index, df_st["ST"].values, c='#D0D0D0', linewidth=0.2)

        dfs_st.append(df_st)

# -------------------------------------------------------------------------
# Combine
dfs_st = pd.concat(dfs_st)
dfs_st.index.name = "year"
dfs_st = dfs_st.reset_index()

# Convert year to datetime for resampling
dfs_st["year"] = pd.to_datetime(dfs_st["year"], format="%Y")
dfs_st = dfs_st.set_index("year")

# -------------------------------------------------------------------------
# Statistics
st_mean = dfs_st.groupby(pd.Grouper(freq='YS'))["ST"].mean()
st_q25 = dfs_st.groupby(pd.Grouper(freq='YS'))["ST"].quantile(0.25)
st_q75 = dfs_st.groupby(pd.Grouper(freq='YS'))["ST"].quantile(0.75)

# -------------------------------------------------------------------------
# Boxplot prep
df_box = dfs_st.reset_index()
df_box['year'] = df_box['year'].dt.year
plot_years = sorted(df_box['year'].unique())

box_colors = dict(facecolor='#267182', alpha=0.3, linewidth=1.2)
median_props = dict(color='#267182', alpha=0.3, linewidth=2)
whisker_props = dict(color='#667375', alpha=0.3, linewidth=1)
cap_props = dict(color='#667375', alpha=0.3, linewidth=1)
flier_props = dict(marker='.', markersize=3, alpha=0.3, color='#667375')

ax1.boxplot(
    [df_box[df_box['year'] == y]['ST'].dropna() for y in plot_years],
    positions=plot_years,
    widths=0.6,
    patch_artist=True,
    boxprops=box_colors,
    medianprops=median_props,
    whiskerprops=whisker_props,
    capprops=cap_props,
    flierprops=flier_props
)

# IQR shading
ax1.fill_between(
    st_mean.index.year,
    st_q25.values,
    st_q75.values,
    alpha=0.2
)

# Mean line
ax1.plot(st_mean.index.year, st_mean.values, c='k', linewidth=2)

# Annotate mean
for i, val in enumerate(st_mean.values):
    ax1.annotate(str(round(val, 1)),
                 (st_mean.index.year[i], val + 0.5),
                 ha='center', fontsize=11)

ax1.set_ylabel('Surface temperature (°C)', fontsize=fsize2)
ax1.set_xlabel('Year', fontsize=fsize2)
ax1.set_title("a. Time-series of estimated lake surface temperature",
              fontsize=fsize1, loc="left", fontweight="bold")

ax1.set_ylim([0, 15])
ax1.grid(axis='y', linestyle='--', alpha=0.4)

# -------------------------------------------------------------------------
# Compute slopes FROM dfs_st (FIXED)
lake_slopes = []

dfs_st_reset = dfs_st.reset_index()

for lake_id, group in dfs_st_reset.groupby("lake_id"):
    group = group.sort_values("year")

    if len(group) < 3:
        continue

    yrs = group["year"].dt.year.values
    temps = group["ST"].values

    slope, *_ = linregress(yrs, temps)

    row = iiml[iiml["lake_id"] == lake_id]
    if row.empty:
        continue
    row = row.iloc[0]

    lake_slopes.append((
        row["area_all"],
        row["volume_km3"],
        row["lat"],
        row["lon"],
        row["region"],
        row["margin"],
        slope
    ))

areas = np.array([l[0] for l in lake_slopes])
volumes = np.array([l[1] for l in lake_slopes])
latitudes = np.array([l[2] for l in lake_slopes])
longitudes = np.array([l[3] for l in lake_slopes])
regions = [l[4] for l in lake_slopes]
margins = [l[5] for l in lake_slopes]
slopes = np.array([l[6] for l in lake_slopes])

# -------------------------------------------------------------------------
# Panel b
ax2.scatter(areas, slopes, alpha=0.3)
ax2.set_xscale('log')

slope_fit, intercept, r_value, p_value, _ = linregress(np.log10(areas), slopes)
x_vals = np.logspace(np.log10(areas.min()), np.log10(areas.max()), 100)
y_vals = intercept + slope_fit * np.log10(x_vals)
ax2.plot(x_vals, y_vals, color='black')

ax2.set_xlabel("Area (km², log)")
ax2.set_ylabel("Temp change (°C/yr)")
ax2.set_title("b. Lake area vs. temperature change", loc="left")

# -------------------------------------------------------------------------
# Panel c
mask = volumes > 0
ax3.scatter(volumes[mask], slopes[mask], alpha=0.3)
ax3.set_xscale('log')

slope_fit, intercept, *_ = linregress(np.log10(volumes[mask]), slopes[mask])
x_vals = np.logspace(np.log10(volumes[mask].min()), np.log10(volumes[mask].max()), 100)
y_vals = intercept + slope_fit * np.log10(x_vals)
ax3.plot(x_vals, y_vals, color='black')

ax3.set_xlabel("Volume (log)")
ax3.set_ylabel("Temp change (°C/yr)")
ax3.set_title("c. Lake volume vs. temperature change", loc="left")

# -------------------------------------------------------------------------
# Panel d
abs_latitudes = np.abs(latitudes)

ax4.scatter(abs_latitudes, slopes, alpha=0.3)
slope_fit, intercept, *_ = linregress(abs_latitudes, slopes)

x_vals = np.linspace(abs_latitudes.min(), abs_latitudes.max(), 100)
y_vals = intercept + slope_fit * x_vals
ax4.plot(x_vals, y_vals, color='black')

ax4.set_xlabel("Absolute latitude")
ax4.set_ylabel("Temp change (°C/yr)")
ax4.set_title("d. Latitude vs. temperature change", loc="left")

# -------------------------------------------------------------------------
plt.tight_layout()
plt.show()

# -------------------------------------------------------------------------
# Regression
df = pd.DataFrame({
    "slope": slopes,
    "area": areas,
    "volume": volumes,
    "latitude": latitudes,
    "longitude": longitudes,
    "region": regions,
    "margin": margins
})

df = df.replace([np.inf, -np.inf], np.nan)
df = df[(df.area > 0) & (df.volume > 0)].dropna()

df["log_area"] = np.log10(df["area"])
df["log_volume"] = np.log10(df["volume"])
df["abs_latitude"] = np.abs(df["latitude"])

#model = smf.ols(
#    "slope ~ latitude * region + log_volume + log_area",
#    data=df
#).fit()

#print(model.summary())