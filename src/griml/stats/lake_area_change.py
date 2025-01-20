# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import geopandas as gp
import glob, math
from functools import reduce
from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

file1 = '*IML-fv1.shp'
file2 = 'ALL-ESA-GRIML-IML-MERGED-fv1_centroids.shp'

geofiles=[]
aggfiles=[]
for f in list(sorted(glob.glob(file1))):
    print(Path(f).stem)
    geofile = gp.read_file(f)
    ag = geofile.dissolve(by='lake_id')
    geofiles.append(geofile)
    aggfiles.append(ag)

# %%
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


df_merged = reduce(lambda  left,right: pd.merge(left,right,on=['lake_id'],
                                            how='outer'), gdfs)
   
# %%
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

print(df_merged)        
# %%       
gdf = gp.read_file(file2)
gdf_all = pd.merge(gdf,df_merged,on=['lake_id'], how='outer')

# gdf_all.to_file('/home/pho/Desktop/griml_dataset/cleaned_and_correct/ALL-ESA-GRIML-IML-MERGED-fv1_areal_change.shp')


