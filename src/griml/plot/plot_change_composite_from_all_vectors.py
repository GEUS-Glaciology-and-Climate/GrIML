# -*- coding: utf-8 -*-

import numpy as np
import geopandas as gpd
import matplotlib as mpl
import matplotlib.pyplot as plt
import textwrap

# Set the font family to sans-serif
mpl.rcParams['font.family'] = 'sans-serif'

# Specify "Arial" as the font to use for the sans-serif family
mpl.rcParams['font.sans-serif'] = ['Arial']

# Optional: You can also set a default font size
mpl.rcParams['font.size'] = 10

# --------------------------------
# Paths
# --------------------------------

workspace1 = ('misc/iml_2016-2025/final_v4/ALL-ESA-GRIML-IML-fv4.gpkg')
out_dir = 'misc/iml_2016-2025/figures/'

# --------------------------------
# Load data
# --------------------------------

geofile = gpd.read_file(workspace1)
area_cols = [f"area_{y}" for y in range(2016, 2026)]
other_lakes = geofile[area_cols].isna().all(axis=1)
geofile["mask"] = other_lakes
print(geofile["mask"])


# --------------------------------
# Plot settings
# --------------------------------

title = 16
fsize1 = 12
fsize2 = 10
fsize3 = 8
fsize4 = 8
fsty = 'arial'
pad = 1.
lw = 1

basin = ['NW', 'NO', 'NE', 'CE', 'SE', 'SW', 'CW']
years = list(range(2016, 2026))

c1 = ['#045275', '#089099', '#7CCBA2', '#FCDE9C', '#F0746E', '#DC3977', '#7C1D6F']
c2 = ['#009392', '#39B185', '#9CCB86', '#E9E29C', '#EEB479', '#E88471', '#CF597E']

# --------------------------------
# Helper function
# --------------------------------

# Remove lakes with no area values in any year
def compute_region_stats(df, margin_type):

    region_stats = []

    for b in basin:

        subset = df[(df["margin"] == margin_type) &
                    (df["region"] == b)]

        basin_abun = []
        basin_mean = []
        basin_median = []
        basin_total = []

        extra_count = list(subset["mask"]).count(True)
        subset = subset.dropna(subset=area_cols, how="all")

        for y in years:

            areas = subset[f"area_{y}"].dropna().values

            basin_abun.append(len(areas)+extra_count)

            if len(areas) > 0:
                basin_mean.append(np.mean(areas))
                basin_median.append(np.median(areas))
                basin_total.append(np.sum(areas))
            else:
                basin_mean.append(np.nan)
                basin_median.append(np.nan)
                basin_total.append(np.nan)

        region_stats.append([basin_abun, basin_mean, basin_median, basin_total])

    return region_stats


# --------------------------------
# Calculate stats
# --------------------------------

ice_sheet_regions = compute_region_stats(geofile, "ICE_SHEET")
ice_cap_regions   = compute_region_stats(geofile, "ICE_CAP")

ice_sheet_abun = [i[0] for i in ice_sheet_regions]
ice_cap_abun   = [i[0] for i in ice_cap_regions]

ice_sheet_area = [i[1] for i in ice_sheet_regions]
ice_cap_area   = [i[1] for i in ice_cap_regions]

ice_sheet_med = [i[2] for i in ice_sheet_regions]
ice_cap_med   = [i[2] for i in ice_cap_regions]

ice_sheet_sum= [i[3] for i in ice_sheet_regions]
ice_cap_sum   = [i[3] for i in ice_cap_regions]


# --------------------------------
# Figure (Ice Sheet)
# --------------------------------
fig = plt.figure(constrained_layout=False, figsize=(5,5))

gs1 = fig.add_gridspec(nrows=3, ncols=1, left=0.15, right=0.8 , top=0.9,
                       bottom=0.08, wspace=0.05, hspace=0.0, height_ratios=[4,1,1])
ax1 = fig.add_subplot(gs1[0, :])
ax5 = fig.add_subplot(gs1[1, :], sharex=ax1)
ax2 = fig.add_subplot(gs1[2, :], sharex=ax1)

bottom1 = np.zeros(len(years))

for i in range(len(basin)):
    p1 = ax1.bar(
        years,
        ice_sheet_abun[i],
        0.5,
        color=c1[i],
        label=basin[i],
        bottom=bottom1
    )

    bottom1 += np.array(ice_sheet_abun[i])
    ax1.bar_label(p1, label_type='center', fontsize=fsize4)

for i in range(len(basin)):
    print('\nIce Sheet lakes ' + basin[i])
    print('Median: ' + str(ice_sheet_med[i]))
    print('Total: ' + str(ice_sheet_sum[i]))
    ax2.plot(years, ice_sheet_med[i], c=c1[i], label=basin[i])
    ax5.plot(years, ice_sheet_sum[i], c=c1[i], label=basin[i])

props = dict(boxstyle='round', facecolor='#6CB0D6', alpha=0.3)
handles, labels = ax1.get_legend_handles_labels()
ax1.legend(handles[::-1], labels[::-1], bbox_to_anchor=(1.01,0.5))

for a in [ax1,ax2,ax5]:
    a.set_axisbelow(True)
    a.yaxis.grid(color='gray', linestyle='dashed', linewidth=0.5)
    a.set_facecolor("#f2f2f2")

ax1.text(-0.2, 1.05, 'a. Ice Sheet lake change', fontsize=fsize1, fontweight="bold",
         horizontalalignment='left', transform=ax1.transAxes) # bbox=props)
ax1.set_ylabel('Number of lakes', ha='center',
         labelpad=8, rotation='vertical', fontsize=fsize2)
ax5.set_ylabel('Total area (km$^2$)',
               ha='center', va='center', rotation='vertical',
               fontsize=fsize2)
ax2.set_ylabel('Median area (km$^2$)',
               ha='center', va='center', rotation='vertical',
               labelpad=15, fontsize=fsize2)
ax2.set_xlabel('Year', ha='center', va='center', labelpad=8, fontsize=fsize2)

ax1.xaxis.set_visible(False)

ax2.set_ylim([0,0.6])
ax2.set_yticks([0.0,0.2,0.4,0.6])
ax2.set_yticklabels(['0.00','0.20','0.40', ''])

ax5.set_ylim([0,900])
ax5.set_yticks([0,300,600,900])
ax5.set_yticklabels(['0','300','600', ''])
ax5.xaxis.set_visible(False)

# plt.show()
plt.savefig(out_dir+'lake_change_by_ice_sheet_region.png', dpi=300, transparent=True)


# --------------------------------
# Figure (PGIC)
# --------------------------------
fig = plt.figure(constrained_layout=False, figsize=(5,5))

gs1 = fig.add_gridspec(nrows=3, ncols=1, left=0.15, right=0.8 , top=0.9,
                       bottom=0.08, wspace=0.05, hspace=0.0, height_ratios=[4,1,1])
ax1 = fig.add_subplot(gs1[0, :])
ax5 = fig.add_subplot(gs1[1, :], sharex=ax1)
ax2 = fig.add_subplot(gs1[2, :], sharex=ax1)

bottom1 = np.zeros(len(years))

for i in range(len(basin)):
    p1 = ax1.bar(
        years,
        ice_cap_abun[i],
        0.5,
        color=c2[i],
        label=basin[i],
        bottom=bottom1
    )

    bottom1 += np.array(ice_cap_abun[i])
    ax1.bar_label(p1, label_type='center', fontsize=fsize4)

for i in range(len(basin)):
    print('\nIce Sheet lakes ' + basin[i])
    print('Median: ' + str(ice_cap_med[i]))
    print('Total: ' + str(ice_cap_sum[i]))
    ax2.plot(years, ice_cap_med[i], c=c2[i], label=basin[i])
    ax5.plot(years, ice_cap_sum[i], c=c2[i], label=basin[i])

props = dict(boxstyle='round', facecolor='#6CB0D6', alpha=0.3)
handles, labels = ax1.get_legend_handles_labels()
ax1.legend(handles[::-1], labels[::-1], bbox_to_anchor=(1.01,0.5))

for a in [ax1,ax2,ax5]:
    a.set_axisbelow(True)
    a.yaxis.grid(color='gray', linestyle='dashed', linewidth=0.5)
    a.set_facecolor("#f2f2f2")

ax1.text(-0.2, 1.05, 'c. PGIC lake change', fontsize=fsize1, fontweight="bold",
         horizontalalignment='left', transform=ax1.transAxes) # bbox=props)
ax1.set_ylabel('Number of lakes', ha='center',
         labelpad=8, rotation='vertical', fontsize=fsize2)
ax5.set_ylabel('Total area (km$^2$)',
               ha='center', va='center', rotation='vertical',
               fontsize=fsize2)
ax2.set_ylabel('Median area (km$^2$)',
               ha='center', va='center', rotation='vertical',
               labelpad=15, fontsize=fsize2)
ax2.set_xlabel('Year', ha='center', va='center', labelpad=8, fontsize=fsize2)

ax1.xaxis.set_visible(False)

ax2.set_ylim([0,0.45])
ax2.set_yticks([0.0,0.15,0.3,0.45])
ax2.set_yticklabels(['0.00','0.15','0.30', ''])

ax5.set_ylim([0,300])
ax5.set_yticks([0,100,200,300])
ax5.set_yticklabels(['0','100','200', ''])
ax5.xaxis.set_visible(False)

plt.show()
# plt.savefig(out_dir+'lake_change_by_pgic_region.png', dpi=300, transparent=True)