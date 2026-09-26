#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import geopandas as gp
import glob
from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib.patches import Patch, FancyBboxPatch
import matplotlib as mpl

# Set the font family to sans-serif
mpl.rcParams['font.family'] = 'sans-serif'

# Specify "Arial" as the font to use for the sans-serif family
mpl.rcParams['font.sans-serif'] = ['Arial']

# Optional: You can also set a default font size
mpl.rcParams['font.size'] = 10

# %%
f = '/home/pho/python_workspace/GrIML/misc/iml_2016-2025/final_v4/with_volumes/ALL-ESA-GRIML-IML-fv4-with-va-volumes.gpkg'
out_dir = '/home/pho/python_workspace/GrIML/misc/iml_2016-2025/figures/'

gdf = gp.read_file(f)

colors=['#045275', '#089099', '#7CCBA2', '#FCDE9C', '#F0746E', '#DC3977', '#7C1D6F']
regions = ['NW', 'NO', 'NE', 'CE', 'SE', 'SW', 'CW']
region_count = []
region_is_count = []
region_pgic_count = []
region_area = []
region_volume = []
for r in regions:
    gdf_r = gdf[gdf["region"] == r]
    region_count.append(len(gdf_r))
    region_area.append(np.sum(gdf_r["area_all"]))
    region_volume.append(np.sum(gdf_r["volume_km3"]))
    region_is_count.append(len(gdf_r[gdf_r["margin"]=="ICE_SHEET"]))
    region_pgic_count.append(len(gdf_r[gdf_r["margin"]=="ICE_CAP"]))

# %%
title = 16
fsize1 = 12
fsize2 = 10
fsize3 = 8
fsize4 = 8
fsty = 'arial'
pad = 1.
lw = 1
props = dict(boxstyle='round', edgecolor="#666699", facecolor="#FFFFFF", 
             lw=2, alpha=1,fill=True,zorder=2000)

fig, ax = plt.subplots(1, figsize=(3, 3))
bottom = np.zeros(len(regions))
labels = ['Ice sheet', 'PGIC']
col = ['#0191ff', '#FFFFFF']
for i in range(len(region_count)):

    # Plot the first set of bars (bottom layer)
    bar1 = ax.bar(regions, region_is_count, 0.5, color='#3589bc', edgecolor='#666699')

    # Plot the second set of bars, starting at the top of the first set
    bar2 = ax.bar(regions, region_pgic_count, 0.5, color='#ffffff', edgecolor='#666699', bottom=region_is_count)

    ax.bar_label(bar1, fmt='{:,.0f}', label_type="center", fontweight="bold")# fontsize=fsize2)
    ax.bar_label(bar2, fmt='{:,.0f}', label_type='center', fontweight="bold")# fontsize=fsize2)

# ax.legend(loc=4)
ax.text(0.5, 1.05,
        'e. Number of lakes by region',
        fontsize=fsize1,
        fontname=fsty,
        fontweight="bold",
        horizontalalignment='center',
        transform=ax.transAxes)

legend_elements = [Patch(facecolor="#3589bc", edgecolor='#666699', label='Ice Sheet'),
                Patch(facecolor="#ffffff", edgecolor='#666699', label='PGIC')]
leg=ax.legend(handles=legend_elements, title="Margin type", bbox_to_anchor=(0.91,-0.13), ncol=2, fontsize=fsize3, alignment='center')
#leg.get_frame().set_edgecolor('#666699')

ax.set_axisbelow(True)
ax.yaxis.grid(color='gray', linestyle='dashed', linewidth=0.5)

ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.spines["left"].set_visible(False)

ax.tick_params(
    axis='y',          # changes apply to the x-axis
    which='both',      # both major and minor ticks are affected
    left=False,         # ticks along the top edge are off
)  # labels along the bottom edge are off

plt.subplots_adjust(top=0.9, bottom=0.25, left=0.15, right=0.9)
# plt.show()
# plt.savefig(out_dir + 'number_of_lakes_by_region_and_margin.png', dpi=300, transparent=True)



fig, ax = plt.subplots(1, figsize=(4, 3))

s = sum(region_area)
region_area_percentage = [round(f / s * 100, 2) for f in region_area]
region_area_labels = [regions[r] + "\n(" + str(int(region_area_percentage[r])) + "%)" for r in list(range(len(regions)))]
[print(r) for r in region_area_labels]

wedges, texts, autotexts = ax.pie(region_area_percentage,
                                  colors=colors,
                                  wedgeprops={"edgecolor": "#666699",
                                              'linewidth': 1,
                                              'antialiased': True},
                                  autopct=lambda p: '{:.0f} km$^2$'.format(p * s / 100),
                                  labels=regions,
                                  textprops={'family': 'arial'},
                                  pctdistance=1.4,
                                  labeldistance=0.6)
# Change CE text position
current_pos = texts[3].get_position()
new_y_position = current_pos[1] - 0.05
new_x_position = current_pos[0]
texts[3].set_position((new_x_position, new_y_position))

# Change SE text position
current_pos = texts[4].get_position()
new_y_position = current_pos[1] - 0.15
new_x_position = current_pos[0] - 0.05
texts[4].set_position((new_x_position, new_y_position))

# Change SW text position
texts[5]._x = -0.04

# Change autotext positions
autotexts[1]._y = +1.0
autotexts[3]._x = -1.25
autotexts[3]._y = -0.6
autotexts[4]._x = -1.0
autotexts[4]._y = -0.9
autotexts[5]._y = -1.1

for a,r in zip(autotexts, region_area):
    a.set_label(f"${r:.2f} km$^2")

# Set the color for each label individually
for t in [texts[0],texts[1],texts[5],texts[6]]:
    t.set_color("#ffffff")
for t in texts:
    t.set_weight("bold")

# Ensure equal aspect ratio for a circular pie chart
ax.set_aspect('equal')
ax.text(0.5, 1.02,
        "d. Total lake area by region",
        fontsize=fsize1,
        fontname=fsty,
        fontweight="bold",
        horizontalalignment='center',
        # bbox=props,
        transform=ax.transAxes)


# Add a bit more breathing room around the axes for the frames
plt.subplots_adjust(top=0.9, bottom=0.1, left=0.1, right=0.9)

# plt.show()
# plt.savefig(out_dir + 'total_area_by_region.png', dpi=300, transparent=True)




fig, ax = plt.subplots(1, figsize=(4, 3))
s = sum(region_volume)
region_vol_percentage = [round(f / s * 100, 2) for f in region_volume]
region_vol_labels = [regions[r] + "\n(" + str(int(region_vol_percentage[r])) + "%)" for r in list(range(len(regions)))]
[print(r) for r in region_vol_labels]

wedges, texts, autotexts = ax.pie(region_vol_percentage,
                                  colors=colors,
                                  wedgeprops={"edgecolor": "#666699",
                                              'linewidth': 1,
                                              'antialiased': True},
                                  autopct=lambda p: '{:.2f} Gt'.format(p * s / 100),
                                  labels=regions,
                                  textprops={'family': 'arial'},
                                  pctdistance=1.4,
                                  labeldistance=0.6)
# Change CE text position
current_pos = texts[3].get_position()
new_y_position = current_pos[1] - 0.13
new_x_position = current_pos[0] - 0.10
texts[3].set_position((new_x_position, new_y_position))

# Change SE text position
current_pos = texts[4].get_position()
new_y_position = current_pos[1] - 0.2
new_x_position = current_pos[0] - 0.12
texts[4].set_position((new_x_position, new_y_position))

# Change SW text position
current_pos = texts[5].get_position()
new_y_position = current_pos[1] - 0.1
new_x_position = current_pos[0] - 0.07
texts[5].set_position((new_x_position, new_y_position))

# Change CW text position
current_pos = texts[6].get_position()
new_y_position = current_pos[1] - 0.03
new_x_position = current_pos[0]
texts[6].set_position((new_x_position, new_y_position))

# Change autotext positions
autotexts[0]._x = +1.3
autotexts[1]._y = +0.95
autotexts[2]._y = +0.6
autotexts[3]._y = -0.6
autotexts[4]._y = -0.8
autotexts[5]._y = -1.1
autotexts[6]._x = +1.3

for a,r in zip(autotexts, region_area):
    a.set_label(f"${r:.2f} Gt")

# Set the color for each label individually
for t in [texts[0],texts[1],texts[5],texts[6]]:
    t.set_color("#ffffff")
for t in texts:
    t.set_weight("bold")

# Ensure equal aspect ratio for a circular pie chart
ax.set_aspect('equal')
ax.text(0.5, 1.02,
        "d. Total lake volume by region",
        fontsize=fsize1,
        fontname=fsty,
        fontweight="bold",
        horizontalalignment='center',
        # bbox=props,
        transform=ax.transAxes)


# Add a bit more breathing room around the axes for the frames
plt.subplots_adjust(top=0.9, bottom=0.1, left=0.1, right=0.9)

# plt.show()
plt.savefig(out_dir + 'total_volume_by_region.png', dpi=300, transparent=True)
