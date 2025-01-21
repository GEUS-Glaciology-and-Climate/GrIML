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
gdf_files = '/home/pho/Desktop/griml_dataset/cleaned_and_correct/*IML-fv1.shp'

# Load inventory point file with lake_id, region, basin-type and placename info
gdf2 = gpd.read_file('/home/pho/python_workspace/GrIML/other/iml_2016-2023/manual_validation/CURATED-ESA-GRIML-IML-fv1.shp')
# gdf2 = gdf2.drop(gdf2[gdf2.geometry==None].index)


# Iterate across inventory series files
for g in list(glob.glob(gdf_files)):
    gdf1 = gpd.read_file(g)
    # gdf1 = gdf1.drop(gdf1[gdf1.geometry==None].index)

    year = str(Path(g).stem)[0:4]
    print('\n')
    print(year)
    print(len(gdf1))
    
    # Join by attribute
    # gdf1['new_lakeid']=list(gdf1['lake_id'])
    gdf = gdf1.merge(gdf2, on='lake_id')
    print(len(gdf))


    # Rename columns
    # gdf['lake_id']=gdf['lake_id_y']
    gdf['margin']=gdf['margin_y']
    gdf['region']=gdf['region_y']
    gdf['lake_name']=gdf['lake_name_y']
    # gdf['start_date']=gdf['startdate']
    # gdf['end_date']=gdf['enddate']
    
    # Reformat geometry
    gdf['geometry'] = gdf['geometry_x']
    gdf = gdf.drop(gdf[gdf.geometry==None].index)
    gdf['area_sqkm']=[s.area/10**6 for s in list(gdf['geometry'])]
    gdf['length_km']=[s.length/1000 for s in list(gdf['geometry'])]
    gdf = gpd.GeoDataFrame(gdf, geometry='geometry')
        

    all_src=[]
    num_src=[]
    for idx, i in gdf.iterrows():
        idl = i['lake_id']
        gi = gdf[gdf['lake_id'] == idl]
        source = list(set(list(gi['source'])))
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

    # # Add average summer temperature fields
    # gdf['temp_aver']=''
    # gdf['temp_max']=''
    # gdf['temp_min']=''
    # gdf['temp_stdev']=''
    # gdf['temp_src']=''
    # gdf['temp_num']=''

    # Reorder columns and index
    gdf_final = gdf[['geometry', 
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
    
    # Re-format index
    gdf_final = gdf_final.sort_values(by='lake_id')
    gdf_final["row_id"] = gdf.index + 1
    gdf_final.reset_index(drop=True, inplace=True)
    gdf_final.set_index("row_id", inplace=True)
     

    print(len(gdf_final))
    gdf_final.to_file('/home/pho/Desktop/griml_dataset/cleaned_and_correct/'+str(year)+'0101-ESA-GRIML-IML-fv1.shp')

    gdf_final['idx'] = gdf_final['lake_id']    
    gdf_dissolve = gdf_final.dissolve(by='idx')
    gdf_dissolve['area_sqkm']=[g.area/10**6 for g in list(gdf_dissolve['geometry'])]
    gdf_dissolve['length_km']=[g.length/1000 for g in list(gdf_dissolve['geometry'])]

    # # Add centroid position
    # gdf_dissolve['centroid'] = gdf_dissolve['geometry'].centroid
    
    # Reorder columns and index
    gdf_dissolve = gdf_dissolve[['geometry', 'lake_id','margin','region','lake_name',
               'start_date','end_date',  'area_sqkm','length_km','all_src',
               'num_src','certainty', 'verified','verif_by','edited', 'edited_by']]
    
    gdf_dissolve = gdf_dissolve.reset_index(drop=True)
    gdf_dissolve.to_file('/home/pho/Desktop/griml_dataset/cleaned_and_correct/'+str(year)+'0101-ESA-GRIML-IML-MERGED-fv1.shp')