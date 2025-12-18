#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
from griml.load import load
from griml.metadata import assign_id, assign_sources, assign_certainty, \
    assign_names, assign_regions

__all__ = ["add_metadata"]

def add_metadata(iml, names, regions, outfile=None, overwrite=False):
    """Add all metadata information to inventory

    Parameters
    ----------
    iml : geopandas.GeoDataFrame or str
        Inventory GeoDataFrame object or filepath
    names : geopandas.GeoDataFrame or str
        Placenames database GeoDataFrame object or filepath
    regions : geopandas.GeoDataFrame or str
        Regions identifier GeoDataFrame object or filepath
    outfile : str
        Filepath for output to be saved to
    overwrite : bool, optional
        Flag whether to overwrite existing file

    Returns
    -------
    iml : geopandas.GeoDataFrame
        Inventory GeoDataFrame with metadata
    """
    iml = load(iml)
    names = load(names)
    regions = load(regions)
    
    print("Assigning ID...")
    iml = assign_id(iml)
        
    print("Assigning sources...")
    iml = assign_sources(iml)
        
    print("Assigning certainty scores...")
    n = ["S1","S2","ARCTICDEM"]
    scores = [0.298, 0.398, 0.304]
    iml = assign_certainty(iml, n, scores)

    print("Assigning regions...")
    iml = assign_regions(iml, regions)
        
    print("Assigning placenames...")
    iml = assign_names(iml, names)
    
    if outfile:
        if os.path.exists(outfile) and overwrite:
            print("File exists and will not be overwritten")
        else:
            print("Saving file...")
            iml.to_file(outfile)
            print("Saved to "+str(outfile)+"_metadata.gpkg")

    return iml
        
        
if __name__ == "__main__": 
    infile1 = "test/test_merge_2.gpkg"
    infile2 = "test/test_placenames.gpkg"
    infile3 = "test/greenland_basins_polarstereo.gpkg"
    add_metadata(infile1, infile2, infile3)
