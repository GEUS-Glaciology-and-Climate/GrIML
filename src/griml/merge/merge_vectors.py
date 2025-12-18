#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import geopandas as gpd
import pandas as pd
from glob import glob
from griml.load import load

__all__ = ["merge_vectors"]

def merge_vectors(inlist, proj="EPSG:3413", outfile=None, overwrite=False):
    """Compile features from multiple processings into one geodataframe

    Parameters
    ----------
    inlist : list
        List of files or geopandas.dataframe.DataFrame objects to merge
    proj : str, optional
        Projection identifier
    outfile : str, optional
        Output file path to write files toall_gdf.to_file(outfile)
    overwrite : bool, optional
        Flag to overwrite existing file
    Returns
    -------
    all_gdf : geopandas.dataframe.GeoDataFrame
        Compiled goedataframe
    """
    feature, method, collection, start_date, end_date = load_all(inlist)
    dfs=[]
    for a,b,c,d,e in zip(feature, method, collection, start_date, end_date):
        if a is not None:
            
            #Construct geodataframe with basic metadata
            gdf = gpd.GeoDataFrame(geometry=a, crs=proj)
            # gdf = dissolve_vectors(gdf)
            dfs.append(pd.DataFrame({"geometry": list(gdf.geometry), 
                                      "method": b, 
                                      "source": c, 
                                      "startdate" : d, 
                                      "enddate" : e}))   
           
    # Construct merged geodataframe
    all_gdf = pd.concat(dfs)
    all_gdf = gpd.GeoDataFrame(all_gdf, crs=proj, geometry=list(all_gdf.geometry))
    
    all_gdf["row_id"] = all_gdf.index + 1
    all_gdf.reset_index(drop=True, inplace=True)
    all_gdf.set_index("row_id", inplace = True)

    all_gdf["area_sqkm"] = all_gdf["geometry"].area/10**6
    all_gdf["length_km"] = all_gdf["geometry"].length/1000
    # all_gdf = gpd.GeoDataFrame(all_gdf, geometry=all_gdf.geometry, 
    #                             crs=proj)

    if outfile is not None:
        if os.path.isfile(outfile):
            if overwrite:
                print("Overwriting existing file")
                all_gdf.to_file(outfile)
                print("Overwritten file saved to " + str(outfile))
            else:
                print("File exists and will not be overwritten. Moving to next file")
        else:
            print("Writing new file")
            all_gdf.to_file(outfile)
            print("New file saved to "+str(outfile))
          
    return all_gdf

def load_all(inlist):
    """Load info from all features for merging

    Parameters
    ----------
    inlist : list
        List of files or geodataframe.dataframe.DataFrame objects to load info
        from

    Returns
    -------
    feature_list : list
        List of shapely features
    method_list : list
        List of strings denoting processing method
    collection_list : list
        List of strings denoting dataset collection
    date_list : list
        List of start and end date for processing
    """ 
    features=[]
    methods=[]
    sources=[]
    starts=[]
    ends=[]
    
    for f in inlist:
        i = load(f)
        features.append(list(i["geometry"]))
        methods.append(list(i["method"]))
        sources.append(list(i["source"]))
        starts.append(list(i["startdate"]))
        ends.append(list(i["enddate"]))
    
    return features, methods, sources, starts, ends

def dissolve_vectors(gdf):
    """Dissolve overlapping polygons in a Pandas GeoDataFrame

    Parameters
    ----------
    gdf : geopandas.GeoDataFrame
        Geodataframe with polygons for dissolving

    Returns
    -------
    gdf2 : geopandas.GeoDataFrame
        Geodataframe with dissolved polygons
    """
    geoms = gdf.geometry.unary_union
    gdf2 = gpd.GeoDataFrame(geometry=[geoms])
    gdf2 = gdf2.explode().reset_index(drop=True)
    return gdf2

if __name__ == "__main__": 
    infile1 = "test/test_data/test_merge_1.shp"
    infile2 = "test/test_data/test_merge_2.shp"
    merge_vectors([infile1,infile2])
