# -*- coding: utf-8 -*-

import numpy as np
import geopandas as gpd
import matplotlib.pyplot as plt

# --------------------------------
# Paths
# --------------------------------

workspace1 = ('ALL-ESA-GRIML-IML-fv4.gpkg')

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

fsize1 = 14
fsize2 = 13
fsize3 = 10
fsize4 = 8

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
# Figure layout
# --------------------------------
fig = plt.figure(constrained_layout=False, figsize=(10,13))

gs1 = fig.add_gridspec(nrows=3, ncols=1, left=0.08, right=0.9 , top=0.95,
                       bottom=0.54, wspace=0.05, hspace=0.0, height_ratios=[4,1,1])
ax1 = fig.add_subplot(gs1[0, :])
ax5 = fig.add_subplot(gs1[1, :], sharex=ax1)
ax2 = fig.add_subplot(gs1[2, :], sharex=ax1)

gs2 = fig.add_gridspec(nrows=3, ncols=1, left=0.08, right=0.9, top=0.46,
                       bottom=0.05, wspace=0.05, hspace=0.0,height_ratios=[4,1,1])
ax3 = fig.add_subplot(gs2[0, :])
ax6 = fig.add_subplot(gs2[1, :], sharex=ax3)
ax4 = fig.add_subplot(gs2[2, :], sharex=ax3)

# --------------------------------
# Stacked abundance bars
# --------------------------------

bottom1 = np.zeros(len(years))
bottom2 = np.zeros(len(years))

for i in range(len(basin)):

    p1 = ax1.bar(
        years,
        ice_sheet_abun[i],
        0.5,
        color=c1[i],
        label=basin[i],
        bottom=bottom1
    )

    p2 = ax3.bar(
        years,
        ice_cap_abun[i],
        0.5,
        color=c2[i],
        label=basin[i],
        bottom=bottom2
    )

    bottom1 += np.array(ice_sheet_abun[i])
    bottom2 += np.array(ice_cap_abun[i])

    ax1.bar_label(p1, label_type='center', fontsize=fsize4)
    ax3.bar_label(p2, label_type='center', fontsize=fsize4)

# --------------------------------
# Mean lake area lines
# --------------------------------

for i in range(len(basin)):
    print('\nIce Sheet lakes ' + basin[i])
    print('Median: ' + str(ice_sheet_med[i]))
    print('Total: ' + str(ice_sheet_sum[i]))
    ax2.plot(years, ice_sheet_med[i], c=c1[i], label=basin[i])
    ax5.plot(years, ice_sheet_sum[i], c=c1[i], label=basin[i])

for i in range(len(basin)):
    print('\nPGIC lakes ' + basin[i])
    print('Median: ' + str(ice_cap_med[i]))
    print('Total: ' + str(ice_cap_sum[i]))
    ax4.plot(years, ice_cap_med[i], c=c2[i], label=basin[i])
    ax6.plot(years, ice_cap_sum[i], c=c2[i], label=basin[i])

# --------------------------------
# Styling
# --------------------------------

props = dict(boxstyle='round', facecolor='#6CB0D6', alpha=0.3)
for a in [ax1,ax3]:
    # a.legend(bbox_to_anchor=(1.01,0.5))
    handles, labels = a.get_legend_handles_labels()
    a.legend(handles[::-1], labels[::-1], bbox_to_anchor=(1.01,0.5))

for a in [ax1,ax2,ax3,ax4,ax5,ax6]:
    a.set_axisbelow(True)
    a.yaxis.grid(color='gray', linestyle='dashed', linewidth=0.5)
    a.set_facecolor("#f2f2f2")

ax1.text(0.01, 1.05, 'Ice Sheet lake change', fontsize=fsize1,
         horizontalalignment='left', bbox=props, transform=ax1.transAxes)
ax3.text(0.01, 1.05, 'Periphery glaciers/ice caps (PGIC) lake change',
         fontsize=fsize1, horizontalalignment='left', bbox=props, transform=ax3.transAxes)

fig.text(0.5, 0.018, 'Year', ha='center', fontsize=fsize2)
fig.text(0.5, 0.51, 'Year', ha='center', fontsize=fsize2)

fig.text(0.02, 0.76, 'Lake abundance', ha='center',
         rotation='vertical', fontsize=fsize2)
fig.text(0.02, 0.27, 'Lake abundance', ha='center',
         rotation='vertical', fontsize=fsize2)

fig.text(0.012, 0.645, 'Total area', ha='center', va='center',
         rotation='vertical', fontsize=fsize2)
fig.text(0.028, 0.645, r'(km$^2$)', ha='center', va='center',
         rotation='vertical', fontsize=fsize2)
fig.text(0.012, 0.155, 'Total area', ha='center', va='center',
         rotation='vertical', fontsize=fsize2)
fig.text(0.028, 0.155, r'(km$^2$)', ha='center', va='center',
         rotation='vertical', fontsize=fsize2)

fig.text(0.012, 0.565, 'Median area', ha='center', va='center',
         rotation='vertical', fontsize=fsize2)
fig.text(0.028, 0.565, r'(km$^2$)', ha='center', va='center',
         rotation='vertical', fontsize=fsize2)
fig.text(0.012, 0.075, 'Median area', ha='center', va='center',
         rotation='vertical', fontsize=fsize2)
fig.text(0.028, 0.075, r'(km$^2$)', ha='center', va='center',
         rotation='vertical', fontsize=fsize2)

fig.text(0.016, 0.96, 'a.', ha='left', fontsize=fsize1+4)
fig.text(0.016, 0.47, 'b.', ha='left', fontsize=fsize1+4)

ax2.set_yticks([0.0,0.25,0.5,0.75])
ax2.set_yticklabels(['0.0','0.25','0.50', ''])
ax4.set_yticks([0.0,0.25,0.5,0.75])
ax4.set_yticklabels(['0.0','0.25','0.50', ''])

ax5.set_yticks([0,300,600,900])
ax5.set_yticklabels(['0','300','600', ''])
ax6.set_yticks([0,100,200,300])
ax6.set_yticklabels(['0','100','200', ''])

# fig.tight_layout(pad=3.0)
# plt.subplots_adjust(wspace=0, hspace=0)
# plt.show()
plt.savefig('lake_change_by_region.png', dpi=300)