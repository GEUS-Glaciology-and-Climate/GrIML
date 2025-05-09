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
title = 20
fsize1 = 14
fsize2 = 12
fsize3 = 10
fsize4 = 8
fsty = 'arial'
pad = 1.
lw = 1
regions = ['NW', 'NO', 'NE', 'CE', 'SE', 'SW', 'CW']
methods = ['ARCTICDEM', 'S1', 'S2']
method_labels = ['DEM', 'SAR', 'VIS']
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
    labels = ['Ice sheet', 'Ice cap']

    # Plot detection performance across regions
    pie_colors = ['#39B185', '#EEB479', '#CF597E']
    dem = []
    s1 = []
    s2 = []
    for g in geofiles:
        n = g[g['region'] == regions[r]]
        dem.append(n['source'].value_counts()['ARCTICDEM'])
        s1.append(n['source'].value_counts()['S1'])
        try:
            s2.append(n['source'].value_counts()['S2'])
        except:
            s2.append(0)
    s = sum(dem)+sum(s1)+sum(s2)
    percentage = [round(f/s*100, 2) for f in [sum(dem), sum(s1), sum(s2)]]

    # Plot the pie chart with autopct for percentages
    wedges, texts = ax.pie(
        percentage, colors=pie_colors, startangle=90,
        wedgeprops={"edgecolor": "#666699",
                    'linewidth': 1,
                    'antialiased': True})

    # Add method labels inside the pie chart
    for i, method in enumerate(method_labels):
        # Use the wedge positions to place labels
        wedge = wedges[i]
        pct = percentage[i]
        angle = (wedge.theta2 + wedge.theta1) / \
            2  # Midpoint angle of the wedge
        # Adjust radius for placement
        x = 0.5 * wedge.r * np.cos(np.radians(angle))
        y = 0.5 * wedge.r * np.sin(np.radians(angle))
        ax.text(x, y, f'{method}\n{pct:.0f}%', ha='center',
                   va='center', fontsize=fsize2, color='black')

    # Ensure equal aspect ratio for a circular pie chart
    ax.set_aspect('equal')
    ax.text(0.5, 0.02, 'Classifications by method', fontsize=fsize3,
               horizontalalignment='center', transform=ax.transAxes)

    # Add a bit more breathing room around the axes for the frames
    plt.subplots_adjust(top=0.9, bottom=0.1, left=0.1, right=0.9)


    
    # rect = FancyBboxPatch(
    #     # (lower-left corner), width, height
    #     (0.05, 0.1), 0.9, 0.87, fill=False, color="#666699", lw=2, 
    #     zorder=2000, transform=fig.transFigure, figure=fig,
    #     boxstyle="round, pad=0, rounding_size=0.01",
    # )
    # fig.patches.extend([rect])    
    ax.text(0.5, 0.99, f'{regions[r]}', fontsize=title, 
               horizontalalignment='center', #weight='bold',
               bbox=props, transform=ax.transAxes)
    
    # plt.show()
    plt.savefig(out_dir+f'{regions[r]}_methods.png', dpi=300, transparent=True)
