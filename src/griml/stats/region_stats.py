#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import geopandas as gpd
import pandas as pd
import numpy as np
from pathlib import Path
import glob

def region_stats(indir):
    '''Calculate region statistics from an inventory series
    
    Parameters
    ----------
    indir : str
        Input directory to inventory series files
    '''

    # Load inventory files
    aggfiles = []
    for f in list(sorted(glob.glob(indir))):
        print('Loading '+ str(Path(f).stem))
        geofile = gpd.read_file(f)
        ag = geofile.dissolve(by='lake_id')
        print (len(ag))
        aggfiles.append(ag)
    
    # Merge inventory dataframes
    lakes = pd.concat(aggfiles)
    lakes = lakes.dissolve(by='lake_id')
    lakes['area_sqkm']=[poly.area/10**6 for poly in list(lakes['geometry'])]
    
    # Define regions    
    regions = ['NW', 'NO', 'NE', 'CE', 'SE', 'SW', 'CW']
    
    # Calculate statistics for each defined region
    for r in regions:
        print('\n' + r)
    
        lakes_r = lakes[lakes['region'] == r]    
        print('Number of lakes (total): ' + str(len(lakes_r)))
        
        lakes_is = lakes_r[lakes_r['margin'] == 'ICE_SHEET']
        print('Number of lakes (Ice Sheet): ' + 
              str(len(lakes_is)))
    
        lakes_ic = lakes_r[lakes_r['margin'] == 'ICE_CAP']
        print('Number of lakes (PGIC): ' + 
              str(len(lakes_ic)))
        
        lake_max = lakes_r['area_sqkm'].idxmax()
        lake_max = lakes_r.loc[[lake_max]]
        print('Largest lake: ' + 
              str(np.max(lakes_r['area_sqkm'])) +
              ' (id: ' + str(lakes_r['area_sqkm'].idxmax()) + 
              ', name: ' + str(list(lake_max['lake_name'])[0])
              )
       
        print('Average lake size (total): ' + 
              str(np.mean(lakes_r['area_sqkm'])))
        
        print('Average lake size (Ice Sheet): ' +
              str(np.mean(lakes_is['area_sqkm'])))
    
        print('Average lake size (PGIC): ' + 
              str(np.mean(lakes_ic['area_sqkm'])))
    
        print('Median lake size (total): ' + 
              str(np.median(lakes_r['area_sqkm'])))
            
        print('Median lake size (Ice Sheet): ' +
              str(np.median(lakes_is['area_sqkm'])))
        
        print('Median lake size (PGIC): ' + 
              str(np.median(lakes_ic['area_sqkm'])))


if __name__ == "__main__":  
    workspace1 = '*IML-fv2.shp'
    region_stats(workspace1)