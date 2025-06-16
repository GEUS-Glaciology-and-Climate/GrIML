#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import itertools
from operator import itemgetter

import geopandas as gpd
import numpy as np
import pandas as pd

from scipy.spatial import cKDTree
from shapely.geometry import Point, LineString, Polygon
from griml.load import load

def assign_names(gdf, gdf_names, distance=1000.0):
    '''Assign placenames to geodataframe geometries based on names in another 
    geodataframe point geometries

    Parameters
    ----------
    gdf : geopandas.GeoDataFrame
        Vectors to assign uncertainty to
    gdf_names : geopandas.GeoDataFrame
        Vector geodataframe with placenames
    distance : int
        Distance threshold between a given vector and a placename
    
    Returns
    -------
    gdf : geopandas.GeoDataFrame
        Vectors with assigned IDs
    '''  
    
    # Load geodataframes
    gdf1 = load(gdf)
    gdf2 = load(gdf_names)
    
    # Compile placenames into new dataframe
    names = _compile_names(gdf2)
    placenames = gpd.GeoDataFrame({"geometry": list(gdf2['geometry']),
                                   "placename": names})
    
    # Remove invalid geometries
    gdf1 = _check_geometries(gdf1)
                                    
    # Assign names based on proximity
    a = _get_nearest_point(gdf1, placenames, distance)
    
    return a


def _get_nearest_point(gdA, gdB, distance=1000.0):
    '''Return properties of nearest point in Y to geometry in X'''
    nA = np.array(list(gdA.geometry.centroid.apply(lambda x: (x.x, x.y))))
    nB = np.array(list(gdB.geometry.apply(lambda x: (x.x, x.y))))

    btree = cKDTree(nB)
    dist, idx = btree.query(nA, k=1)
    gdB_nearest = gdB.iloc[idx].drop(columns="geometry").reset_index(drop=True)
    gdf = pd.concat(
        [
            gdA.reset_index(drop=True),
            gdB_nearest,
            pd.Series(dist, name='dist')
        ], 
        axis=1)
    
    gdf.loc[gdf['dist']>=distance, 'placename'] = 'Unknown'
    gdf = gdf.drop(columns=['dist'])    
    return gdf

def _get_indices(mylist, value):
    '''Get indices for value in list'''
    return[i for i, x in enumerate(mylist) if x==value]


def _check_geometries(gdf):
    '''Check that all geometries within a geodataframe are valid'''  
    return gdf.drop(gdf[gdf.geometry==None].index)

def _compile_names(gdf):
    '''Get preferred placenames from placename geodatabase'''  
    placenames=[]
    for i,v in gdf.iterrows():
        if v['New Greenl'] != None: 
            placenames.append(v['New Greenl'])
        else:
            if v['Old Greenl'] != None: 
                placenames.append(v['Old Greenl'])
            else:
            	if v['Danish'] != None: 
                    placenames.append(v['Danish'])
            	else:
                    if v['Alternativ'] != None:
                        placenames.append(v['Alternativ'])
                    else:
                        placenames.append(None)
    return placenames
