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
method_labels = ['DEM', 'SAR', 'VIS']
props = dict(boxstyle='round', edgecolor="#666699", facecolor="#FFFFFF", 
             lw=2, alpha=1,fill=True,zorder=2000)


for i in range(len(regions)):
    print(f'Plotting {regions[i]}...')

    fig, ax= plt.subplots(1, figsize=(6,3))
    s1=[]
    s2=[]
    adem=[]
    s1adem=[]
    s1s2=[]
    s2adem=[]
    s1s2adem=[]
    for g in aggfiles:
        n = g[g['region']==regions[i]]
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
    wedges, texts, autotexts = ax.pie(percentage, colors=c1,
                           wedgeprops={"edgecolor": "#666699",
                           'linewidth': 1,
                           'antialiased': True},
                            autopct='%.0f%%', 
                            pctdistance=1.2)
    autotexts[2]._x=+0.6
    autotexts[2]._y=+1.0    
    

    # Ensure equal aspect ratio for a circular pie chart
    ax.set_aspect('equal')
    ax.text(0.5, 1, regions[i], fontsize=fsize1, horizontalalignment='center', 
                bbox=props, transform=ax.transAxes) 

    legend_elements = [Patch(facecolor=c1[0],  label='SAR'),
                       Patch(facecolor=c1[1], label='VIS'),
                       Patch(facecolor=c1[2], label='DEM'),
                       Patch(facecolor=c1[3],  label='SAR, DEM'),
                       Patch(facecolor=c1[4], label='SAR, VIS'),
                       Patch(facecolor=c1[5], label='VIS, DEM'),
                       Patch(facecolor=c1[6], label='SAR, VIS, DEM')] 

    if regions[i] in ['NO', 'NW', 'CW', 'SW']:         
        leg=ax.legend(handles=legend_elements, bbox_to_anchor=(0,0.85), fontsize=fsize3)
    else:
        leg=ax.legend(handles=legend_elements, bbox_to_anchor=(1.05,0.8), fontsize=fsize3)
    leg.get_frame().set_edgecolor('#666699')   
    
    # Add a bit more breathing room around the axes for the frames
    plt.subplots_adjust(top=0.9, bottom=0.1, left=0.1, right=0.9)
    
    # plt.show()
    plt.savefig(out_dir+f'{regions[i]}_sources.png', dpi=300, transparent=True)
