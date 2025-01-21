#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  5 13:11:30 2024

@author: pho
"""

import geopandas as gpd
import pandas as pd
import glob
import numpy as np

gdf_files = '*IML-fv1.shp'

gdfs=[]
for g in list(glob.glob(gdf_files)):
    print(g)
    gdf = gpd.read_file(g)
    gdfs.append(gdf)

all_gdf = pd.concat(gdfs)


# Reorder columns and index
all_gdf = all_gdf[['geometry', 
               'lake_id', 
               'lake_name', 
               'margin', 
               'region', 
               'area_sqkm', 
               'length_km',
               'all_src', 
               'num_src',
               'certainty',  
               'verified', 
               'verif_by', 
               'edited', 
               'edited_by']]
 
# Update geometry metadata
print('Dissolving geometries...')
all_gdf['idx'] = all_gdf['lake_id']    
gdf_dissolve = all_gdf.dissolve(by='idx')

# %%

gdf_dissolve['area_sqkm']=[g.area/10**6 for g in list(gdf_dissolve['geometry'])]
gdf_dissolve['length_km']=[g.length/1000 for g in list(gdf_dissolve['geometry'])]

print('Total number of classified lakes: ')
print(len(gdf_dissolve))

print('Total number of ice sheet lakes: ')
print(len(gdf_dissolve[gdf_dissolve['margin']=='ICE_SHEET']))

print('Total number of PGIC lakes: ')
print(len(gdf_dissolve[gdf_dissolve['margin']=='ICE_CAP']))

print('Total number of ice sheet lakes per region: ')
print(gdf_dissolve['region'].value_counts())

print('Total number of lakes above 10 sq km: ')
print(len(gdf_dissolve[gdf_dissolve['area_sqkm']>=10]))

print('Average lake size: ')
print(gdf_dissolve['area_sqkm'].values.mean())

print('Median lake size: ')
print(np.median(gdf_dissolve['area_sqkm'].values))

print('Total number of lakes below 1 sq km: ')
print(len(gdf_dissolve[gdf_dissolve['area_sqkm']<=1.0]))

print('Total number of lakes above 10 sq km: ')
print(len(gdf_dissolve[gdf_dissolve['area_sqkm']>=10]))

print('Largest lakes: ')
big = gdf_dissolve[gdf_dissolve['area_sqkm']>=80]
print(big['lake_name'])
print(big['region'])
print(big['area_sqkm'])
      
# # Save to file
# print('Saving merged geometries to file...')
# gdf_dissolve = gdf_dissolve.sort_values(by='lake_id')
# gdf_dissolve.to_file('/home/pho/Desktop/griml_dataset/cleaned_and_correct/ALL-ESA-GRIML-IML-MERGED-fv1.shp')

# # Add centroid position
# print('Saving centroid geometries to file...')
# gdf_dissolve['geometry'] = gdf_dissolve['geometry'].centroid    
# gdf_dissolve.to_file('/home/pho/Desktop/griml_dataset/cleaned_and_correct/ALL-ESA-GRIML-IML-MERGED-fv1_centroids.shp')
