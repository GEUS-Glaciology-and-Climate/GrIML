#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 18 15:41:24 2024

@author: pho
"""
import geopandas as gpd
import glob, sys
import numpy as np
import pandas as pd
from pathlib import Path
from scipy.sparse.csgraph import connected_components
from scipy.spatial import cKDTree

# Map inventory file locations
gdfs = '/home/pho/python_workspace/GrIML/other/iml_2016-2023/final/unchecked/*MERGED-fv1.shp'

# Load inventory point file with lake_id, region, basin-type and placename info
gdf2 = gpd.read_file('/home/pho/python_workspace/GrIML/other/iml_2016-2023/manual_validation/CURATED-ESA-GRIML-IML-fv1.shp')

# Iterate across inventory series files
for g in list(glob.glob(gdfs)):
    gdf1 = gpd.read_file(g)

    year = str(Path(g).stem).split('-')[0]
    print('\n')
    print(year)
    print(len(gdf1))
    
    # Assign ID, region, basin-type and placename attributes
    gdf1_corr = gdf1.drop(gdf1[gdf1.geometry==None].index)
    gdf2_corr = gdf2.drop(gdf2[gdf2.geometry==None].index)
    print(len(gdf1_corr))
    
    gdf1_corr = gdf1_corr.drop(columns=['lake_id','margin','region','lake_name'])
    
    distance=100
    nA = np.array(list(gdf1_corr.geometry.centroid.apply(lambda x: (x.x, x.y))))
    nB = np.array(list(gdf2_corr.geometry.apply(lambda x: (x.x, x.y))))
    
    btree = cKDTree(nB)
    dist, idx = btree.query(nA, k=1)
    gdf2_nearest = gdf2_corr.iloc[idx].drop(columns="geometry").reset_index(drop=True)
    gdf = pd.concat(
        [
            gdf1_corr.reset_index(drop=True),
            gdf2_nearest,
            pd.Series(dist, name='dist')
        ], 
        axis=1)   

    # Reorder columns and index
    gdf_new = gdf[['geometry', 
                   'lake_id', 
                   'lake_name', 
                   'margin', 
                   'region', 
                   'area_sqkm', 
                   'length_km',
                   'temp_aver',
                   'temp_min',
                   'temp_max',
                   'temp_stdev',
                   'method',
                   'source',
                   'all_src', 
                   'num_src',
                   'certainty',
                   'start_date',
                   'end_date',   
                   'verified', 
                   'verif_by', 
                   'edited', 
                   'edited_by']]
    gdf_new = gdf_new.sort_values(by='lake_id')
    # gdf_new = gdf_new.reset_index(drop=True) 
    
    
    # # Add sources
    # def _get_indices(mylist, value):
    #     '''Get indices for value in list'''
    #     return[i for i, x in enumerate(mylist) if x==value]
    
    # col_names=['lake_id', 'source']
    # ids = gdf[col_names[0]].tolist()
    # source = gdf[col_names[1]].tolist()
    # satellites=[]
    
    # # Construct source list
    # for x in range(len(ids)):
    #     indx = _get_indices(ids, x)
    #     if len(indx) != 0:
    #         res = []
    #         if len(indx) == 1:
    #             res.append(source[indx[0]].split('/')[-1])
    #         else:
    #             unid=[]
    #             for dx in indx:
    #                 unid.append(source[dx].split('/')[-1])
    #             res.append(list(set(unid)))
                
    #         for z in range(len(indx)):
    #             if len(indx) == 1:
    #                 satellites.append(res)
    #             else:
    #                 satellites.append(res[0])
    #     else:
    #         print(x)
    #         print('Nothing appended!')
    # # Compile lists for appending
    # satellites_names = [', '.join(i) for i in satellites]
    # number = [len(i) for i in satellites]
    
    # # Return updated geodataframe    
    # gdf['all_src']=satellites_names
    # gdf['num_src']=number


    # all_src=[]
    # num_src=[]
    # for idx, i in gdf.iterrows():
    #     idl = i['lake_id']
    #     g = gdf[gdf['lake_id'] == idl]
    #     source = list(set(list(g['source'])))
    #     satellites=''
    #     if len(source)==1:
    #         satellites = satellites.join(source)
    #         num = 1
    #     elif len(source)==2:
    #         satellites = satellites.join(source[0]+', '+source[1])
    #         num = 2
    #     elif len(source)==3:
    #         satellites = satellites.join(source[0]+', '+source[1]+', '+source[2])
    #         num = 3
    #     else:
    #         print('Unknown number of sources detected')
    #         print(source)
    #         satellites=None
    #         num=None
    #     all_src.append(satellites)
    #     num_src.append(num)
    # satellites
    # gdf['all_src']=all_src
    # gdf['num_src']=num_src


    # # Add certainty score
    # def _get_score(value, search_names, scores):
    #     '''Determine score from search string'''
    #     if search_names[0] in value:
    #         return scores[0]
    #     elif search_names[1] in value:
    #         return scores[1]
    #     elif search_names[2] == value:
    #         return scores[2]
    #     else:
    #         return None
        
    # source='all_src'
    # search_names = ['S1','S2','ARCTICDEM']
    # scores = [0.298, 0.398, 0.304]
    # cert=[]
    # srcs = list(gdf[source])
    
    # for a in range(len(srcs)):
    #     if srcs[a].split(', ')==1:
    #         out = _get_score(srcs.split(', '))
    #         cert.append(out)    
    #     else:
    #         out=[]
    #         for b in srcs[a].split(', '):
    #             out.append(_get_score(b, search_names, scores))
    #         cert.append(sum(out))
    
    # gdf['certainty'] = cert

    # # Add average summer temperature fields
    # gdf['temp_aver']=''
    # gdf['temp_max']=''
    # gdf['temp_min']=''
    # gdf['temp_stdev']=''
    # gdf['temp_src']=''
    # gdf['temp_num']=''

    # # Add verification and manual intervention fields
    # gdf['verified']='Yes'
    # gdf['verif_by']='How'
    # gdf['edited']=''
    # gdf['edited_by']=''
    
    # Re-format index
    gdf_new["row_id"] = gdf_new.index + 1
    gdf_new.reset_index(drop=True, inplace=True)
    gdf_new.set_index("row_id", inplace=True)
    
    print(len(gdf_new))
        
    gdf_new.to_file('/home/pho/Desktop/griml_dataset/'+str(year)+'-ESA-GRIML-IML-fv1.shp')
    
