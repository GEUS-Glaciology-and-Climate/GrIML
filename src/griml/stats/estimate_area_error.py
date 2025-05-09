#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import geopandas as gpd
import glob


def get_method_area(g, method):
    '''Compute classified lake area from a specific classification method'''
    f = g[g['method'] == method]
    f['idx'] = f['lake_id']
    f = f.dissolve(by='idx')
    f['area_sqkm']=[poly.area/10**6 for poly in list(f['geometry'])]
    return f[['lake_id','area_sqkm']]
    

def estimate_area_error(infile):
    '''Estimate area error by comparing the area of SAR and VIS classified 
    lakes in a inventory, or series of inventories
    
    Parameters
    ----------
    infile : str, list
        File path or list of file paths for estimating abundancy error from
    '''
    # For a series of files
    if type(infile) is list:
        gdfs=[]
        for g in infile:
            
            # Load geodataframe
            print('Loading ' + g)
            gdf = gpd.read_file(g)

            # Get area for SAR and VIS classifications
            sar = get_method_area(gdf, 'SAR')
            vis = get_method_area(gdf, 'VIS')
            
            # Retain common classifications
            common = pd.merge(sar,vis,on=['lake_id'], how='inner')
            common['area_sqkm_diff'] = np.abs(common['area_sqkm_x']-common['area_sqkm_y'])
            gdfs.append(common)
        
        # Concatenate all classifications
        all_common_lakes = pd.concat(gdfs)  

      
    # For a single file
    else:
        gdf = gpd.read_file(infile)
        
        # Get area for SAR and VIS classifications
        sar = get_method_area(gdf, 'SAR')
        vis = get_method_area(gdf, 'VIS')
        
        # Retain common classifications
        all_common_lakes = pd.merge(sar,vis,on=['lake_id'], how='inner')       
          
    # Calculate error as percentage
    perc = []
    for i,j in all_common_lakes.iterrows():
        perc.append((j['area_sqkm_diff']/max([j['area_sqkm_x'],j['area_sqkm_y']]))*100)
    all_common_lakes['diff_perc']=perc      


    # Calculate average and median difference, and average percentage        
    average = np.average(all_common_lakes['area_sqkm_diff'])
    median = np.median(all_common_lakes['area_sqkm_diff'])
    average_percentage = np.average(all_common_lakes['diff_perc'])
    
    print('Computed from ' + str(len(all_common_lakes)) + ' lakes')
    print('Average difference: '+str(average))
    print('Median difference: '+str(median))
    print('Average percentage difference: '+str(average_percentage))

if __name__ == "__main__":
    indir = '*IML_fv2.gpkg'
    infiles = sorted(list(glob.glob(indir)))
    estimate_area_error(infiles)