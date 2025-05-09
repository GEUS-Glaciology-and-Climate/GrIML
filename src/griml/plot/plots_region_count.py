#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import geopandas as gp
import glob
from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib.patches import Patch, FancyBboxPatch

# %%
workspace1 = '*IML-fv2.shp'
out_dir = 'out/'

geofiles = []
aggfiles = []
for f in list(sorted(glob.glob(workspace1))):
    print(Path(f).stem)
    geofile = gp.read_file(f)
    ag = geofile.dissolve(by='lake_id')
    geofiles.append(geofile)
    aggfiles.append(ag)

# %%
title = 16
fsize1 = 10
fsize2 = 8
fsize3 = 8
fsize4 = 8
fsty = 'arial'
pad = 1.
lw = 1
regions = ['NW', 'NO', 'NE', 'CE', 'SE', 'SW', 'CW']
methods = ['ARCTICDEM', 'S1', 'S2']
props = dict(boxstyle='round', edgecolor="#666699", facecolor="#FFFFFF", 
             lw=2, alpha=1,fill=True,zorder=2000)


for r in range(len(regions)):
    print(f'Plotting {regions[r]}...')

    # Plot unique lake abundance change
    fig, ax = plt.subplots(1, figsize=(3, 3))
    ice_sheet = []
    ice_cap = []
    for ag in aggfiles:
        n = ag[ag['region'] == regions[r]]
        i1 = len(n[n['margin'] == 'ICE_SHEET'])
        i2 = len(n[n['margin'] == 'ICE_CAP'])
        ice_sheet.append(i1)
        ice_cap.append(i2)
    out = [ice_sheet, ice_cap]
    years = list(range(2016, 2024, 1))
    bottom = np.zeros(8)
    labels = ['Ice sheet', 'PGIC']
    col = ['#0191ff', '#FFFFFF']
    for i in range(len(out)):
        p = ax.bar(years, out[i], 0.5, color=col[i], label=labels[i],
                      bottom=bottom, edgecolor='#666699')
        bottom += out[i]
        ax.bar_label(p, label_type='center', fontsize=fsize2)

    ax.legend(loc=4, ncol=2, bbox_to_anchor=(1.05,-0.3))
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


    # ax.set_xlabel('Year', fontsize=fsize1)
    ax.set_ylabel('Number of lakes by year',fontsize=fsize1)
    
    # Add a bit more breathing room around the axes for the frames
    plt.subplots_adjust(top=0.9, bottom=0.2, left=0.2, right=0.9)

    # rect = FancyBboxPatch(
    #     # (lower-left corner), width, height
    #     (0.05, 0.07), 0.92, 0.92, fill=False, color="#666699", lw=2, 
    #     zorder=2000, transform=fig.transFigure, figure=fig,
    #     boxstyle="round, pad=0, rounding_size=0.01",
    # )
    # fig.patches.extend([rect])    
    ax.text(0.45, 1.02, f'{regions[r]}', fontsize=title, 
               horizontalalignment='center', #weight='bold',
               bbox=props, transform=ax.transAxes)
    
    # plt.show()
    plt.savefig(out_dir+f'{regions[r]}_count.png', dpi=300, transparent=True)
