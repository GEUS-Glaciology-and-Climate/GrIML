#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 26 16:09:20 2024

@author: pho
"""
import geopandas as gpd
import glob
import numpy as np
import pandas as pd
from pathlib import Path
from scipy.sparse.csgraph import connected_components
from scipy.spatial import cKDTree

# Map inventory file locations
gdf_files = '/home/pho/Desktop/python_workspace/GrIML/other/iml_2016-2023/final/checked/*IML-fv1.shp'

# Load inventory point file with lake_id, region, basin-type and placename info
gdf2 = gpd.read_file('/home/pho/Desktop/python_workspace/GrIML/other/iml_2016-2023/manual_validation/iml_manual_validation_with_names.shp')
gdf2_corr = gdf2.drop(gdf2[gdf2.geometry==None].index)


# Iterate across inventory series files
gdfs=[]
for g in list(sorted(glob.glob(gdf_files))):
    print(g)
    gdf = gpd.read_file(g)
    gdf = gdf.dissolve(by='lake_id')
    print(len(gdf['geometry']))
    gdfs.append(gdf)

dfs = pd.concat(gdfs)
dfs = dfs.dissolve(by='lake_id')
dfs['area_sqkm']=[g.area/10**6 for g in list(dfs['geometry'])]
dfs['length_km']=[g.length/1000 for g in list(dfs['geometry'])]

    
print('Average lake size: ' + str(dfs.area_sqkm.mean()))

dfs.to_file('/home/pho/Desktop/python_workspace/GrIML/other/iml_2016-2023/final/checked/'+'ALL-ESA-GRIML-IML-MERGED-fv1.shp')