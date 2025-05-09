#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import geopandas as gp
import glob, math
from functools import reduce
from pathlib import Path


def lake_area_change(indir):
    '''Calculate lake area change over time from a series of inventories
    
    Parameters
    ----------
    indir : str
        Input directory where inventory series can be found (including * 
        filtering, e.g. *.gpkg)
    
    Returns
    -------
    df_merged : geopandas.GeoDataFrame
        Geodataframe containing area change information
    '''
    # Load all files
    geofiles=[]
    aggfiles=[]
    for f in list(sorted(glob.glob(indir))):
        print(Path(f).stem)
        geofile = gp.read_file(f)
        ag = geofile.dissolve(by='lake_id')
        geofiles.append(geofile)
        aggfiles.append(ag)

    # Remove DEM classifications
    gdfs=[]
    for g in geofiles:
        f = g[g['method'] != 'DEM']
        f['idx'] = f['lake_id']
        f = f.dissolve(by='idx')
        f['area_sqkm']=[poly.area/10**6 for poly in list(f['geometry'])]
        year=list(f['start_date'])[0]
        area_name = 'area_'+year
        f[area_name] = f['area_sqkm']
        
        gdfs.append(f[['lake_id', area_name]])
    
    # Merge all inventories
    df_merged = reduce(lambda  left,right: pd.merge(left,right,on=['lake_id'],
                                                how='outer'), gdfs)
       
    # Determine area trend and append to row
    for i,j in df_merged.iterrows():
        areas = [j['area_20160701'], j['area_20170701'], j['area_20180701'], 
                 j['area_20190701'], j['area_20200701'], j['area_20210701'], 
                 j['area_20220701'], j['area_20230701']]
    
        count = sum(1 for num in areas if not math.isnan(num))
        if count >=2:
            valid_areas = [num for num in areas if not math.isnan(num)]
            df_merged.at[i, 'area_max'] = float(max(valid_areas))
            df_merged.at[i, 'area_min'] = float(min(valid_areas))
            df_merged.at[i, 'area_flux'] = float(abs(max(valid_areas) - min(valid_areas)))
            df_merged.at[i, 'area_count'] = float(len(valid_areas))
            
            area_diff = valid_areas[-1] - valid_areas[0]
            df_merged.at[i, 'area_diff'] = float(area_diff)
            
            if area_diff > 0.05:
                df_merged.at[i, 'area_flag'] = 'larger'
            elif area_diff < -0.05:
                df_merged.at[i, 'area_flag'] = 'smaller'
            else:
                df_merged.at[i, 'area_flag'] = 'stable'            
            
        else:
            df_merged.at[i, 'area_max'] = np.nan
            df_merged.at[i, 'area_min'] = np.nan
            df_merged.at[i, 'area_flux'] = np.nan
            df_merged.at[i, 'area_count'] = np.nan        
            df_merged.at[i, 'area_diff'] = np.nan       
            df_merged.at[i, 'area_flag'] = None
         
    # gdf = gp.read_file(file2)
    # gdf_all = pd.merge(gdf,df_merged,on=['lake_id'], how='outer')
    
    return df_merged
    

if __name__ == "__main__":  
    file1 = '*IML-fv2.shp'
    gdf_all = lake_area_change(file1)
    # gdf_all.to_file('ALL-ESA-GRIML-IML-MERGED-fv1_areal_change.shp')
