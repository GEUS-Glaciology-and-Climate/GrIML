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

aggfiles = []
for f in list(sorted(glob.glob(workspace1))):
    print(Path(f).stem)
    geofile = gp.read_file(f)
    ag = geofile.dissolve(by='lake_id')
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
c1=['#7e4794','#36b700','#c8c8c8','#f0c571','#59a89c','#0b81a2','#e25759','#9d2c00']
# c1=['#045275', '#089099', '#7CCBA2', '#FCDE9C', '#F0746E', '#DC3977', '#7C1D6F']
c2=['#009392', '#39B185', '#9CCB86', '#E9E29C', '#EEB479', '#E88471', '#CF597E']
regions = ['NW', 'NO', 'NE', 'CE', 'SE', 'SW', 'CW']
props = dict(boxstyle='round', edgecolor="#666699", facecolor="#FFFFFF", 
             lw=2, alpha=1,fill=True,zorder=2000)


fig = plt.figure(figsize=(15,10), constrained_layout=False)
gs = fig.add_gridspec(nrows=10, ncols=2, wspace=0.05, left=0.05, right=0.48 )
ax1 = fig.add_subplot(gs[:-6, :])
ax2 = fig.add_subplot(gs[-5:, :-1])
ax3 = fig.add_subplot(gs[-5:, -1:])


s1=[]
s2=[]
adem=[]
s1adem=[]
s1s2=[]
s2adem=[]
s1s2adem=[]
for n in aggfiles:
    # n = g[g['region']==regions[i]]
    s1.append(n['certainty'].value_counts()[0.298])
    s2.append(n['certainty'].value_counts()[0.398])
    adem.append(n['certainty'].value_counts()[0.304])
    s1adem.append(n['certainty'].value_counts()[0.298+0.304])
    s1s2.append(n['certainty'].value_counts()[0.298+0.398])
    s2adem.append(n['certainty'].value_counts()[0.398+0.304])
    s1s2adem.append(n['certainty'].value_counts()[1.0])

s = sum(s1)+sum(s2)+sum(adem)+sum(s1adem)+sum(s1s2)+sum(s2adem)+sum(s1s2adem)
percentage = [round(f/s*100,2) for f in [sum(s1),sum(s2),sum(adem),
                                         sum(s1adem),sum(s1s2),sum(s2adem),
                                         sum(s1s2adem)]]
print(percentage)
method_labels = [f'SAR\n({sum(s1)})', f'VIS\n({sum(s2)})', f'DEM\n({sum(adem)})', 
                 f'SAR & DEM\n({sum(s1adem)})', f'SAR & VIS\n({sum(s1s2)})', 
                 f'VIS & DEM\n({sum(s2adem)})', f'SAR, VIS & DEM\n({sum(s1s2adem)})'] 
wedges, texts, autotexts = ax1.pie(percentage, colors=c1, labels=method_labels,
                       wedgeprops={"edgecolor": "#666699",
                       'linewidth': 1,
                       'antialiased': True},
                        autopct='%.0f%%', 
                        pctdistance=0.7)

texts[0]._y=texts[0]._y-0.1  
texts[3]._y=texts[3]._y-0.1  
texts[4]._x=texts[4]._x-0.1
texts[4]._y=texts[4]._y-0.1    
texts[5]._x=texts[5]._x+0.08
texts[5]._y=texts[5]._y+0.05 

# Ensure equal aspect ratio for a circular pie chart
ax1.set_aspect('equal')
ax1.text(0.03, 0.98, "a. Methodology performance for lake detection\nacross all inventory years (2016-2023)", fontsize=fsize1, 
         horizontalalignment='center', bbox=props, transform=ax1.transAxes) 

legend_elements = [Patch(facecolor=c1[0],  label='SAR'),
                   Patch(facecolor=c1[1], label='VIS'),
                   Patch(facecolor=c1[2], label='DEM'),
                   Patch(facecolor=c1[3],  label='SAR & DEM'),
                   Patch(facecolor=c1[4], label='SAR & VIS'),
                   Patch(facecolor=c1[5], label='VIS & DEM'),
                   Patch(facecolor=c1[6], label='SAR, VIS & DEM')] 

leg=ax1.legend(handles=legend_elements, bbox_to_anchor=(0.0,0.7), fontsize=fsize3)
# leg=ax1.legend(handles=legend_elements, bbox_to_anchor=(1.05,0.8), fontsize=fsize3)
leg.get_frame().set_edgecolor('#666699')   

is_regions = []
ic_regions = []
for i in range(len(regions)):
    print(f'Plotting {regions[i]}...')
    is_s1=[]
    is_s2=[]
    is_adem=[]
    is_s1adem=[]
    is_s1s2=[]
    is_s2adem=[]
    is_s1s2adem=[]
    ic_s1=[]
    ic_s2=[]
    ic_adem=[]
    ic_s1adem=[]
    ic_s1s2=[]
    ic_s2adem=[]
    ic_s1s2adem=[]
    for g in aggfiles:
        n = g[g['margin']=='ICE_SHEET']
        n = n[n['region']==regions[i]]
        try:
            is_s1.append(n['certainty'].value_counts()[0.298])
        except:
            is_s1.append(0)
        try:
            is_s2.append(n['certainty'].value_counts()[0.398])
        except:
            is_s2.append(0) 
        try:
            is_adem.append(n['certainty'].value_counts()[0.304])
        except:
            is_adem.append(0)            
        try:
            is_s1adem.append(n['certainty'].value_counts()[0.298+0.304])
        except:
            is_s1adem.append(0)
        try:
            is_s1s2.append(n['certainty'].value_counts()[0.298+0.398])
        except:
            is_s1s2.append(0)
        try:
            is_s2adem.append(n['certainty'].value_counts()[0.398+0.304])
        except:
            is_s2adem.append(0)
        try:
            is_s1s2adem.append(n['certainty'].value_counts()[1.0])
        except:
            is_s1s2adem.append(0)
            
        o = g[g['margin']=='ICE_CAP']
        o = o[o['region']==regions[i]]
        try:
            ic_s1.append(o['certainty'].value_counts()[0.298])
        except:
            ic_s1.append(0)
        try:
            ic_s2.append(o['certainty'].value_counts()[0.398])
        except:
            ic_s2.append(0) 
        try:
            ic_adem.append(o['certainty'].value_counts()[0.304])
        except:
            ic_adem.append(0)            
        try:
            ic_s1adem.append(o['certainty'].value_counts()[0.298+0.304])
        except:
            ic_s1adem.append(0)
        try:
            ic_s1s2.append(o['certainty'].value_counts()[0.298+0.398])
        except:
            ic_s1s2.append(0)
        try:
            ic_s2adem.append(o['certainty'].value_counts()[0.398+0.304])
        except:
            ic_s2adem.append(0)
        try:
            ic_s1s2adem.append(o['certainty'].value_counts()[1.0])
        except:
            ic_s1s2adem.append(0)
        
        
    is_regions.append([sum(is_s1), sum(is_s2), sum(is_adem), 
                          sum(is_s1adem), sum(is_s1s2), sum(is_s2adem), 
                          sum(is_s1s2adem)])
    ic_regions.append([sum(ic_s1), sum(ic_s2), sum(ic_adem), 
                          sum(ic_s1adem), sum(ic_s1s2), sum(ic_s2adem), 
                          sum(ic_s1s2adem)])
        
total_is_regions = [sum(i) for i in is_regions]
total_ic_regions = [sum(i) for i in ic_regions]

is_regions = list(zip(*is_regions))
ic_regions = list(zip(*ic_regions))   
           
bottom1=np.zeros(7)
bottom2=np.zeros(7)

for i in range(len(is_regions)):
    p1 = ax2.bar(regions, is_regions[i], 0.5, color=c1[i], label=is_regions[i], 
                 edgecolor='#666699', bottom=bottom1)
    p2 = ax3.bar(regions, ic_regions[i], 0.5, color=c1[i], label=ic_regions[i],
                 edgecolor='#666699', bottom=bottom2)

    bottom1 += is_regions[i]
    bottom2 += ic_regions[i]

ax2.bar_label(p1, labels=total_is_regions, label_type='edge', fontsize=fsize4)
ax3.bar_label(p2, labels=total_ic_regions, label_type='edge', fontsize=fsize4)
    
    
print(bottom1)
print(bottom2)   
    

    # Ensure equal aspect ratio for a circular pie chart
    # ax.set_aspect('equal')
ax2.text(-0.15, 1.08, 'b. Ice sheet by region', fontsize=fsize1, 
         horizontalalignment='left', bbox=props, transform=ax2.transAxes) 

ax3.text(1.04, 1.08, 'c. PGIC by region', fontsize=fsize1, 
         horizontalalignment='left', bbox=props, transform=ax2.transAxes) 


ax2.set_ylabel('Number of lake classifications across all inventory years', fontsize=fsize3)
ax2.set_xlabel('Ice sheet region', fontsize=fsize3)
ax3.set_xlabel('PGIC region', fontsize=fsize3)
ax3.set_yticks([0,500,1000,1500,2000,2500])
ax3twin = ax3.twinx()
ax3twin.set_yticks([0,500,1000,1500,2000,2500])
ax3twin.set_ylabel('Number of lake classifications across all inventory years', 
                   rotation=270, labelpad=15, fontsize=fsize3)
ax3.set_yticklabels(['','','','','',''])

for a in [ax2,ax3,ax3twin]:  
    a.set_axisbelow(True)
    a.yaxis.grid(color='gray', linestyle='dashed', linewidth=0.5)
    a.spines["top"].set_visible(False)
    a.spines["right"].set_visible(False)
    a.spines["left"].set_visible(False)
    a.tick_params(
        axis='y',          # changes apply to the x-axis
        which='both',      # both major and minor ticks are affected
        left=False,         # ticks along the top edge are off
        right=False,
    )  # labels along the bottom edge are off

plt.subplots_adjust(wspace=0, hspace=0)    
# plt.show()
plt.savefig(out_dir+'method_performance.png', dpi=300)
