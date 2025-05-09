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
c1=['#045275', '#089099', '#7CCBA2', '#FCDE9C', '#F0746E', '#DC3977', '#7C1D6F']
regions = ['NW', 'NO', 'NE', 'CE', 'SE', 'SW', 'CW']
methods = ['ARCTICDEM', 'S1', 'S2']
props = dict(boxstyle='round', edgecolor="#666699", facecolor="#FFFFFF", 
             lw=2, alpha=1,fill=True,zorder=2000)


for r in range(len(regions)):
    print(f'Plotting {regions[r]}...')

    # Plot unique lake abundance change
    fig, ax = plt.subplots(2, 1, figsize=(6, 10))
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
    col = ['#0191ff', '#FFFFFF']
    for i in range(len(out)):
        p = ax[0].bar(years, out[i], 0.5, color=col[i], label=labels[i],
                      bottom=bottom, edgecolor='#666699')
        bottom += out[i]
        ax[0].bar_label(p, label_type='center', fontsize=fsize2)

    ax[0].legend(loc=4)
    ax[0].text(0.5, 1.05, 'Number of lakes by inventory year', fontsize=fsize1,
               horizontalalignment='center', transform=ax[0].transAxes)
    ax[0].set_axisbelow(True)
    ax[0].yaxis.grid(color='gray', linestyle='dashed', linewidth=0.5)

    ax[0].spines["top"].set_visible(False)
    ax[0].spines["right"].set_visible(False)
    ax[0].spines["left"].set_visible(False)

    ax[0].tick_params(
        axis='y',          # changes apply to the x-axis
        which='both',      # both major and minor ticks are affected
        left=False,         # ticks along the top edge are off
    )  # labels along the bottom edge are off


    # # Plot detection performance across regions
    # pie_colors = ['#39B185', '#EEB479', '#CF597E']
    # dem = []
    # s1 = []
    # s2 = []
    # for g in geofiles:
    #     n = g[g['region'] == regions[r]]
    #     dem.append(n['source'].value_counts()['ARCTICDEM'])
    #     s1.append(n['source'].value_counts()['S1'])
    #     try:
    #         s2.append(n['source'].value_counts()['S2'])
    #     except:
    #         s2.append(0)
    # s = sum(dem)+sum(s1)+sum(s2)
    # percentage = [round(f/s*100, 2) for f in [sum(dem), sum(s1), sum(s2)]]

    # # Plot the pie chart with autopct for percentages
    # wedges, texts = ax[1].pie(
    #     percentage, colors=pie_colors, startangle=90,
    #     wedgeprops={"edgecolor": "#666699",
    #                 'linewidth': 1,
    #                 'antialiased': True})

    # # Add method labels inside the pie chart
    # for i, method in enumerate(methods):
    #     # Use the wedge positions to place labels
    #     wedge = wedges[i]
    #     pct = percentage[i]
    #     angle = (wedge.theta2 + wedge.theta1) / \
    #         2  # Midpoint angle of the wedge
    #     # Adjust radius for placement
    #     x = 0.5 * wedge.r * np.cos(np.radians(angle))
    #     y = 0.5 * wedge.r * np.sin(np.radians(angle))
    #     ax[1].text(x, y, f'{method}\n{pct:.0f}%', ha='center',
    #                va='center', fontsize=fsize2, color='black')

    # # Ensure equal aspect ratio for a circular pie chart
    # ax[1].set_aspect('equal')
    # ax[1].text(0.5, 0.95, 'Lake classifications by method', fontsize=fsize1,
    #            horizontalalignment='center', transform=ax[1].transAxes)

    # # Add a bit more breathing room around the axes for the frames
    # plt.subplots_adjust(top=0.8, bottom=0.2, left=0.2, right=0.8)

    s1=[]
    s2=[]
    adem=[]
    s1adem=[]
    s1s2=[]
    s2adem=[]
    s1s2adem=[]
    for g in aggfiles:
        n = g[g['region']==regions[r]]
        s1.append(n['certainty'].value_counts()[0.298])
        try:
            s2.append(n['certainty'].value_counts()[0.398])
        except:
            s2.append(0) 
        try:
            adem.append(n['certainty'].value_counts()[0.304])
        except:
            adem.append(0)            
        try:
            s1adem.append(n['certainty'].value_counts()[0.298+0.304])
        except:
            s1adem.append(0)
        try:
            s1s2.append(n['certainty'].value_counts()[0.298+0.398])
        except:
            s1s2.append(0)
        try:
            s2adem.append(n['certainty'].value_counts()[0.398+0.304])
        except:
            s2adem.append(0)
        try:
            s1s2adem.append(n['certainty'].value_counts()[1.0])
        except:
            s1s2adem.append(0)
        
    s = sum(s1)+sum(s2)+sum(adem)+sum(s1adem)+sum(s1s2)+sum(s2adem)+sum(s1s2adem)
    percentage = [round(f/s*100,2) for f in [sum(s1),sum(s2),sum(adem),
                                             sum(s1adem),sum(s1s2),sum(s2adem),
                                             sum(s1s2adem)]]
    print(percentage)
    wedges, texts, autotexts = ax[1].pie(percentage, colors=c1,
                           wedgeprops={"edgecolor": "#666699",
                           'linewidth': 1,
                           'antialiased': True},
                            autopct='%.0f%%', 
                            pctdistance=1.2)
    autotexts[2]._x=+0.6
    autotexts[2]._y=+1.0    
    [a.set_fontsize(fsize2) for a in autotexts]
    # Ensure equal aspect ratio for a circular pie chart
    ax[1].set_aspect('equal')

    legend_elements = [Patch(facecolor=c1[0],  label='SAR'),
                       Patch(facecolor=c1[1], label='VIS'),
                       Patch(facecolor=c1[2], label='DEM'),
                       Patch(facecolor=c1[3],  label='SAR, DEM'),
                       Patch(facecolor=c1[4], label='SAR, VIS'),
                       Patch(facecolor=c1[5], label='VIS, DEM'),
                       Patch(facecolor=c1[6], label='SAR, VIS, DEM')] 

    leg=ax[1].legend(handles=legend_elements, bbox_to_anchor=(1.19,-0.01), 
                     ncol=3, fontsize=fsize3, alignment='center')
    leg.get_frame().set_edgecolor('#666699')   
    
    ax[1].text(0.5, 1.0, 'Lakes by classification/s', fontsize=fsize1,
               horizontalalignment='center', transform=ax[1].transAxes)   
    
    # Add a bit more breathing room around the axes for the frames
    plt.subplots_adjust(top=0.8, bottom=0.2, left=0.15, right=0.85)

    
    rect = FancyBboxPatch(
        # (lower-left corner), width, height
        (0.08, 0.11), 0.78, 0.8, fill=False, color="#666699", lw=2, 
        zorder=2000, transform=fig.transFigure, figure=fig,
        boxstyle="round, pad=0, rounding_size=0.01",
    )
    fig.patches.extend([rect])    
    ax[0].text(0.5, 1.22, f'{regions[r]}', fontsize=title, 
               horizontalalignment='center', #weight='bold',
               bbox=props, transform=ax[0].transAxes)
    
    # plt.show()
    plt.savefig(out_dir+f'{regions[r]}_overview2.png', dpi=300, 
                transparent=True)
