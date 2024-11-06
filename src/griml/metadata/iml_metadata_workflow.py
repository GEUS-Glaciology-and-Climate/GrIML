#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 18 15:41:24 2024

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
gdfs = '/home/pho/Desktop/python_workspace/GrIML/other/iml_2016-2023/merged/*.shp'

# Load inventory point file with lake_id, region, basin-type and placename info
gdf2 = gpd.read_file('/home/pho/Desktop/python_workspace/GrIML/other/iml_2016-2023/manual_validation/iml_manual_validation_with_names.shp')

# Iterate across inventory series files
for g in list(glob.glob(gdfs)):
    gdf1 = gpd.read_file(g)
# gdf1 = gpd.read_file('/home/pho/Desktop/python_workspace/GrIML/other/iml_2016-2023/merged/2016_merged.shp')
    
    year = str(Path(g).stem).split('_')[0]
    print(year)
    
    # Assign ID, region, basin-type and placename attributes
    gdf1_corr = gdf1.drop(gdf1[gdf1.geometry==None].index)
    gdf2_corr = gdf2.drop(gdf2[gdf2.geometry==None].index)
    
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
    
    
    # Rename columns
    gdf['lake_id']=gdf['new_lakeid']
    gdf['margin']=gdf['BasinType']
    gdf['region']=gdf['Region']
    gdf['lake_name']=gdf['placename']
    gdf['start_date']=gdf['startdate']
    gdf['end_date']=gdf['enddate']
    
    
    # Reorder columns and index
    gdf = gdf[['geometry', 'lake_id','margin','region','lake_name',
               'start_date','end_date','area_sqkm','length_km','method','source']]
    gdf = gdf.sort_values(by='lake_id')
    gdf = gdf.reset_index(drop=True) 
    
    
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


    all_src=[]
    num_src=[]
    for idx, i in gdf.iterrows():
        idl = i['lake_id']
        g = gdf[gdf['lake_id'] == idl]
        source = list(set(list(g['source'])))
        satellites=''
        if len(source)==1:
            satellites = satellites.join(source)
            num = 1
        elif len(source)==2:
            satellites = satellites.join(source[0]+', '+source[1])
            num = 2
        elif len(source)==3:
            satellites = satellites.join(source[0]+', '+source[1]+', '+source[2])
            num = 3
        else:
            print('Unknown number of sources detected')
            print(source)
            satellites=None
            num=None
        all_src.append(satellites)
        num_src.append(num)
    satellites
    gdf['all_src']=all_src
    gdf['num_src']=num_src


    # Add certainty score
    def _get_score(value, search_names, scores):
        '''Determine score from search string'''
        if search_names[0] in value:
            return scores[0]
        elif search_names[1] in value:
            return scores[1]
        elif search_names[2] == value:
            return scores[2]
        else:
            return None
        
    source='all_src'
    search_names = ['S1','S2','ARCTICDEM']
    scores = [0.298, 0.398, 0.304]
    cert=[]
    srcs = list(gdf[source])
    
    for a in range(len(srcs)):
        if srcs[a].split(', ')==1:
            out = _get_score(srcs.split(', '))
            cert.append(out)    
        else:
            out=[]
            for b in srcs[a].split(', '):
                out.append(_get_score(b, search_names, scores))
            cert.append(sum(out))
    
    gdf['certainty'] = cert

    # Add average summer temperature fields
    gdf['temp_aver']=''
    gdf['temp_max']=''
    gdf['temp_min']=''
    gdf['temp_stdev']=''
    gdf['temp_src']=''
    gdf['temp_num']=''

    # Add verification and manual intervention fields
    gdf['verified']='Yes'
    gdf['verif_by']='How'
    gdf['edited']=''
    gdf['edited_by']=''
    
    # Re-format index
    gdf["row_id"] = gdf.index + 1
    gdf.reset_index(drop=True, inplace=True)
    gdf.set_index("row_id", inplace=True)
        
    gdf.to_file('/home/pho/Desktop/python_workspace/GrIML/other/iml_2016-2023/metadata/'+str(year)+'0101-ESA-GRIML-IML-MERGED-fv1.shp')
    
