#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import geopandas as gp
import glob
from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

workspace1 = '*IML-fv1.shp'
out_dir = 'out/'

geofiles=[]
aggfiles=[]
for f in list(sorted(glob.glob(workspace1))):
    print(Path(f).stem)
    geofile = gp.read_file(f)
    ag = geofile.dissolve(by='lake_id')
    geofiles.append(geofile)
    aggfiles.append(ag)

fsize1 = 14
fsize2 = 12
fsize3 = 10
fsize4 = 8
fsty = 'arial'
pad=1.
lloc=1
lw=1    
c1=['#045275', '#089099', '#7CCBA2', '#FCDE9C', '#F0746E', '#DC3977', '#7C1D6F']
c2=['#009392', '#39B185', '#9CCB86', '#E9E29C', '#EEB479', '#E88471', '#CF597E']
b=['NW', 'NO', 'NE', 'CE', 'SE', 'SW', 'CW']
methods = ['ARCTICDEM', 'S1', 'S2']
props = dict(boxstyle='round', facecolor='#6CB0D6', alpha=0.3)

# Plot unique lake abundance change
fig, ax = plt.subplots(1, figsize=(10,7))
ice_sheet=[]
ice_cap=[]
for ag in aggfiles:
    i1 = len(ag[ag['margin'] == 'ICE_SHEET'])
    i2 = len(ag[ag['margin'] == 'ICE_CAP'])
    ice_sheet.append(i1)
    ice_cap.append(i2)
out = [ice_sheet, ice_cap]
years=list(range(2016,2024, 1))
bottom=np.zeros(8)
labels=['Ice sheet', 'Ice cap']
col = [c1[1], c1[4]]
for i in range(len(out)):
    p = ax.bar(years, out[i], 0.5, color=col[i], label=labels[i], bottom=bottom)
    bottom += out[i]
    ax.bar_label(p, label_type='center', fontsize=fsize3)

ax.legend(loc=lloc)

fig.text(0.5, 0.03, 'Year', ha='center', fontsize=fsize1)
fig.text(0.045, 0.3, 'Number of ice marginal lakes', ha='center', 
         rotation='vertical', fontsize=fsize1)

ax.set_axisbelow(True)
ax.yaxis.grid(color='gray', linestyle='dashed', linewidth=0.5)
# plt.show()
plt.savefig(out_dir+'unique_lake_abundance_by_margin.png', dpi=300)

#--------------------------------

# Plot unique lake abundance change
fig, ax = plt.subplots(2,1, figsize=(10,10), sharex=False)
nw=[]
no=[]
ne=[]
ce=[]
se=[]
sw=[]
cw=[]
out1 = [nw, no, ne, ce, se, sw, cw]
for ag in aggfiles:
    icesheet = ag[ag['margin'] == 'ICE_SHEET']
    for i in range(len(b)):
        out1[i].append(icesheet['region'].value_counts()[b[i]])
years=list(range(2016,2024, 1))
bottom1=np.zeros(8)
for i in range(len(out1)):
    p = ax[0].bar(years, out1[i], 0.5, color=c1[i],  label=b[i], bottom=bottom1)
    bottom1 += out1[i]
    ax[0].bar_label(p, label_type='center', fontsize=fsize4)
print(bottom1)
ax[0].legend(bbox_to_anchor=(1.01,0.7))
ax[0].text(0.01, 1.04, 'Ice Sheet', fontsize=fsize1, horizontalalignment='left', 
           bbox=props, transform=ax[0].transAxes)

nw=[]
no=[]
ne=[]
ce=[]
se=[]
sw=[]
cw=[]
out2 = [nw, no, ne, ce, se, sw, cw]
for ag in aggfiles:
    icesheet = ag[ag['margin'] == 'ICE_CAP']
    for i in range(len(b)):
        out2[i].append(icesheet['region'].value_counts()[b[i]])
years=list(range(2016,2024, 1))
bottom2=np.zeros(8)
for i in range(len(out2)):
    p = ax[1].bar(years, out2[i], 0.5, color=c2[i], label=b[i], bottom=bottom2)
    bottom2 += out2[i]
    ax[1].bar_label(p, label_type='center', fontsize=fsize4)
print(bottom2)
ax[1].legend(bbox_to_anchor=(1.01,0.7))
ax[1].text(0.01, 1.04, 'Ice caps and periphery glaciers', fontsize=fsize1, 
           horizontalalignment='left', bbox=props, transform=ax[1].transAxes)

fig.text(0.5, 0.02, 'Year', ha='center', fontsize=fsize1)
fig.text(0.025, 0.35, 'Number of ice marginal lakes', ha='center', 
         rotation='vertical', fontsize=fsize1)

for a in ax:
    a.set_axisbelow(True)
    a.yaxis.grid(color='gray', linestyle='dashed', linewidth=0.5)
    a.set_facecolor("#f2f2f2")
fig.tight_layout(pad=3.0)
# plt.show()
plt.savefig(out_dir+'unique_lake_abundance_by_region.png', dpi=300)

#--------------------------------

# Plot unique lake area change
fig, ax = plt.subplots(1, figsize=(10,7))
ice_sheet=[]
ice_cap=[]
for g in geofiles:
    f = g[g['method'] != 'DEM']
    f = f.dissolve(by='lake_id')
    
    i1 = f[f['margin'] == 'ICE_SHEET']
    i2 = f[f['margin'] == 'ICE_CAP']
    
    i1['area_sqkm']=[poly.area/10**6 for poly in list(i1['geometry'])]
    i2['area_sqkm']=[poly.area/10**6 for poly in list(i2['geometry'])]
    
    ice_sheet.append(np.average(i1.area_sqkm))
    ice_cap.append(np.average(i2.area_sqkm))
   
out = [ice_sheet, ice_cap]
years=list(range(2016,2024, 1))
bottom=np.zeros(8)
labels=['Ice sheet', 'Ice cap']
col = [c1[1], c1[4]]
for i in range(len(out)):
    p = ax.plot(years, out[i], color=col[i], label=labels[i])

ax.legend(loc=lloc)

fig.text(0.5, 0.03, 'Year', ha='center', fontsize=fsize1)
fig.text(0.045, 0.3, 'Average ice marginal lake area', ha='center', 
         rotation='vertical', fontsize=fsize1)

ax.set_axisbelow(True)
ax.yaxis.grid(color='gray', linestyle='dashed', linewidth=0.5)
# plt.show()
plt.savefig(out_dir+'lake_area_by_margin.png', dpi=300)



#--------------------------------

# Plot regional lake area change
fig, ax = plt.subplots(2,1, figsize=(10,10), sharex=True)
is_nw=[]
is_no=[]
is_ne=[]
is_ce=[]
is_se=[]
is_sw=[]
is_cw=[]
ice_sheet_area = [is_nw, is_no, is_ne, is_ce, is_se, is_sw, is_cw]
ic_nw=[]
ic_no=[]
ic_ne=[]
ic_ce=[]
ic_se=[]
ic_sw=[]
ic_cw=[]
ice_cap_area = [ic_nw, ic_no, ic_ne, ic_ce, ic_se, ic_sw, ic_cw]
for g in geofiles:
    f = g[g['method'] != 'DEM']
    f = f.dissolve(by='lake_id')
    
    i1 = f[f['margin'] == 'ICE_SHEET']
    i2 = f[f['margin'] == 'ICE_CAP']
    
    i1['area_sqkm']=[poly.area/10**6 for poly in list(i1['geometry'])]
    i2['area_sqkm']=[poly.area/10**6 for poly in list(i2['geometry'])]
    
    for i in range(len(b)):
        isheet = i1[i1['region'] == b[i]]
        ice_sheet_area[i].append(np.average(isheet.area_sqkm))
        icap = i2[i2['region'] == b[i]]
        ice_cap_area[i].append(np.average(icap.area_sqkm))
   
years=list(range(2016,2024, 1))

for i in range(len(b)):
    ax[0].plot(years, ice_sheet_area[i], c=c1[i], label=b[i])
ax[0].legend(loc=lloc)

for i in range(len(b)):
    ax[1].plot(years, ice_cap_area[i], c=c2[i], label=b[i])
ax[1].legend(loc=lloc)

fig.text(0.5, 0.03, 'Year', ha='center', fontsize=fsize1)
fig.text(0.045, 0.3, 'Average ice marginal lake area', ha='center', 
         rotation='vertical', fontsize=fsize1)

for a in ax:
    a.set_axisbelow(True)
    a.yaxis.grid(color='gray', linestyle='dashed', linewidth=0.5)
# plt.show()
plt.savefig(out_dir+'lake_area_by_region.png', dpi=300)

#--------------------------------

# Plot detection performance across regions

fig, ((ax1,ax2),(ax3,ax4),(ax5,ax6),(ax7,ax8))= plt.subplots(4,2, figsize=(5,10))
ax=[ax1,ax2,ax3,ax4,ax5,ax6,ax7,ax8]
pie_colors = [c2[1], c2[4], c2[6]]
for i in range(len(b)):
    dem=[]
    s1=[]
    s2=[]
    for g in geofiles:
        n = g[g['region']==b[i]]
        try:
            dem.append(n['source'].value_counts()['ARCTICDEM'])
        except:
            dem.append(0)
        try:
            s1.append(n['source'].value_counts()['S1'])
        except:
            s1.append(0)
        try:
            s2.append(n['source'].value_counts()['S2'])
        except:
            s2.append(0)
    s = sum(dem)+sum(s1)+sum(s2)
    percentage = [round(f/s*100,2) for f in [sum(dem), sum(s1), sum(s2)]]
    ax[i].pie(percentage, colors=pie_colors, autopct='%.0f%%')
    ax[i].text(0.5, 1, b[i], fontsize=fsize2, horizontalalignment='center', 
                bbox=props, transform=ax[i].transAxes)
fig.delaxes(ax[-1])   

legend_elements = [Patch(facecolor=pie_colors[0],  label='DEM'),
                   Patch(facecolor=pie_colors[1], 
                         label='SAR'),
                   Patch(facecolor=pie_colors[2], 
                         label='VIS')]
        
ax[-2].legend(handles=legend_elements, bbox_to_anchor=(1.45,0.7), fontsize=fsize2)
# plt.show()
plt.savefig(out_dir+'method_performance_by_region.png', dpi=300)

#--------------------------------

# Plot number of detection performance across regions

fig, ((ax1,ax2),(ax3,ax4),(ax5,ax6),(ax7,ax8))= plt.subplots(4,2, figsize=(5,10))
ax=[ax1,ax2,ax3,ax4,ax5,ax6,ax7,ax8]
pie_colors = [c1[1], c1[4], c1[6]]
for i in range(len(b)):
    one=[]
    two=[]
    three=[]
    for g in geofiles:
        n = g[g['region']==b[i]]
        one.append(n['num_src'].value_counts()[1])
        two.append(n['num_src'].value_counts()[2])
        try:
            three.append(n['num_src'].value_counts()[3])
        except:
            three.append(0)
    s = sum(one)+sum(two)+sum(three)
    percentage = [round(f/s*100,2) for f in [sum(one), sum(two), sum(three)]]
    ax[i].pie(percentage, colors=pie_colors, autopct='%.0f%%')
    ax[i].text(0.5, 1, b[i], fontsize=fsize2, horizontalalignment='center', 
                bbox=props, transform=ax[i].transAxes)
fig.delaxes(ax[-1])   

legend_elements = [Patch(facecolor=pie_colors[0],  label='One detection'),
                   Patch(facecolor=pie_colors[1], 
                         label='Two detections'),
                   Patch(facecolor=pie_colors[2], 
                         label='Three detections')]
        
ax[-2].legend(handles=legend_elements, bbox_to_anchor=(1.1,1.05), fontsize=fsize2)
# plt.show()
plt.savefig(out_dir+'lake_certainty_by_region.png', dpi=300)



# Plot number of detection performance across regions
fig, ((ax1,ax2),(ax3,ax4),(ax5,ax6),(ax7,ax8))= plt.subplots(4,2, figsize=(5,10))
ax=[ax1,ax2,ax3,ax4,ax5,ax6,ax7,ax8]
for i in range(len(b)):
    s1=[]
    s2=[]
    adem=[]
    s1adem=[]
    s1s2=[]
    s2adem=[]
    s1s2adem=[]
    for g in geofiles:
        n = g[g['region']==b[i]]
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
    patches, texts, autotexts = ax[i].pie(percentage, 
                                          colors=c1, 
                                          autopct='%.0f%%', 
                                          pctdistance=1.2)
    autotexts[2]._x=+0.6
    autotexts[2]._y=+1.0
    ax[i].text(0.5, 1, b[i], fontsize=fsize2, horizontalalignment='center', 
                bbox=props, transform=ax[i].transAxes)
fig.delaxes(ax[-1])   

legend_elements = [Patch(facecolor=c1[0],  label='SAR'),
                   Patch(facecolor=c1[1], label='VIS'),
                   Patch(facecolor=c1[2], label='DEM'),
                   Patch(facecolor=c1[3],  label='SAR, DEM'),
                   Patch(facecolor=c1[4], label='SAR, VIS'),
                   Patch(facecolor=c1[5], label='VIS, DEM'),
                   Patch(facecolor=c1[6], label='SAR, VIS, DEM')]
        
ax[-2].legend(handles=legend_elements, bbox_to_anchor=(1.1,1.05), fontsize=fsize2)
# plt.show()
plt.savefig(out_dir+'lake_all_certainty_by_region.png', dpi=300)


