#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import geopandas as gpd
import pandas as pd
import glob

def merge_and_dissolve_all(indir, outdir):
    
    gdfs=[]
    for g in list(glob.glob(indir+'IML-fv1.shp')):
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
    gdf_dissolve['area_sqkm']=[g.area/10**6 for g in list(gdf_dissolve['geometry'])]
    gdf_dissolve['length_km']=[g.length/1000 for g in list(gdf_dissolve['geometry'])]
    
    # Save to file
    print('Saving merged geometries to file...')
    gdf_dissolve = gdf_dissolve.sort_values(by='lake_id')
    gdf_dissolve.to_file(outdir+'ALL-ESA-GRIML-IML-MERGED-fv1.shp')
    
    # Add centroid position
    print('Saving centroid geometries to file...')
    gdf_dissolve['geometry'] = gdf_dissolve['geometry'].centroid    
    gdf_dissolve.to_file(outdir+'ALL-ESA-GRIML-IML-MERGED-fv1_centroids.shp')
