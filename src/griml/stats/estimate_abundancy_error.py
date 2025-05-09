#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import geopandas as gpd
import glob
import pandas as pd


def estimate_abundancy_error(gdf1, gdf2):
    '''Estimate abundancy error by comparing number of lakes in a inventory,
    or series of inventories, with a manually defined set of points (i.e. 
    lakes that have been manually identified)
    
    Parameters
    ----------
    gdf1 : str, list
        File path or list of file paths for estimating abundancy error from
    gdf2 : str
        File path to file for validating against
    '''

    gdf2_corr = gdf2.drop(gdf2[gdf2.geometry==None].index)
    
    if type(gdf1) is list:
        
        # Iterate across inventory series files
        gdfs=[]
        for g in gdf1:
            print('Loading ' + g)
            gdf = gpd.read_file(g)
            gdf = gdf.dissolve(by='lake_id')
            print(len(gdf['geometry']))
            gdfs.append(gdf)
        
        dfs = pd.concat(gdfs)
        dfs = dfs.dissolve(by='lake_id')
    
    else:
        dfs = gpd.read_file(gdf1)
    
    print('Number of lakes in inventory/inventory series: ' + len(dfs))
    print('Number of manually validated lakes: ' + len(gdf2_corr))
    print('Difference in lakes: ' + (len(gdf2_corr)-len(dfs)))
    print('Abundancy error estimate: +/- '+ ((len(gdf2_corr)-len(dfs))/2) + 
          ' (' + (len(dfs)/len(gdf2_corr))*100 + '%)')

if __name__ == "__main__":

    indir = '*IML_fv2.gpkg'
    infiles = sorted(list(glob.glob(indir)))
    
    manual_file = 'CURATED-ESA-GRIML-IML-fv2.gpkg'
    estimate_abundancy_error(infiles, manual_file)