#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def assign_sources(gdf, col_names=['lake_id', 'source']):
    '''Assign source metadata to geodataframe, based on unique lake id and
    individual source information
    
    Parameters
    ----------
    gdf : geopandas.GeoDataFrame
        Vectors to assign sources to
    col_names : list
        Column names to assign sources from
    
    Returns
    -------
    gdf : geopandas.GeoDataFrame
        Vectors with assigned sources
    '''
    all_src=[]
    num_src=[]
    for idx, i in gdf.iterrows():
        idl = i[col_names[0]]
        g = gdf[gdf[col_names[0]] == idl]
        source = list(set(list(gdf[col_names[1]])))
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
    return gdf

def _get_indices(mylist, value):
    '''Get indices for value in list'''
    return[i for i, x in enumerate(mylist) if x==value]
