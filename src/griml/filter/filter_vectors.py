#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from griml.filter import filter_margin, filter_area
from griml.load import load
import geopandas as gpd
from pathlib import Path

__all__ = ["filter_vectors"]

def filter_vectors(inlist, margin_file, min_area=0.05, outdir=None, overwrite=False):
    """Filter vectors by area and margin proximity

    Parameters
    ----------
    inlist : list
        List of either file paths of GeoDataFrame objects to filter
    margin_file : str, geopandas.GeoSeries
        Buffered margin to perform margin proximity filter
    min_area: int, optional
        Threshold area (sq km) to filter by
    outdir : str, optional
        Output directory to write files to
    overwrite : bool, optional
        Flag to overwrite existing file

    Returns
    -------
    filtered : list
        List of filtered GeoDataFrame objects
    """
    
    # Load margin
    margin_buff = load(margin_file)
    
    # Iterate through input list
    count=1
    filtered=[]
    for infile in inlist:
    
        # Load and define name
        if type(infile)==str:
            print("\n"+str(count)+"/"+str(len(inlist)) +
                  ": Filtering vectors in "+str(Path(infile).name))   
            name = str(Path(infile).stem)+"_filtered.gpkg"
            
        else:
            print("\n"+str(count)+"/"+str(len(inlist))) 
            name = "lakes_" + str(count) + "_filtered.gpkg"
        
        vectors = load(infile)

        # Perform filtering steps
        vectors = filter_area(vectors, min_area)
        print(f"{vectors.shape[0]} features over 0.05 sq km")
        
        vectors = filter_margin(vectors, margin_buff)
        print(f"{vectors.shape[0]} features within 500 m of margin")    

        # Retain and save if vectors are present after filtering
        if vectors.shape[0]>0:

            if outdir is not None:
                outfile = Path(outdir).joinpath(name)

                if os.path.isfile(outfile):
                    if overwrite:
                        print("Overwriting existing file...")
                        vectors.tofile(outfile)
                        print("Overwritten file saved to " + str(outfile))
                    else:
                        print("File exists and will not be overwritten. Moving to next file")
                else:
                    print("Writing new file...")
                    vectors.to_file(outfile)
                    print("New file saved to " + str(outfile))

            filtered.append(vectors)

        else:
        	print("No vectors present after filter. Moving to next file.")
        count=count+1

    return filtered
        


if __name__ == "__main__":
    import griml
    import os
    infile1 = "test/test_data/test_filter.gpkg"
    infile2 = "test/test_data/test_icemask.gpkg"
    filter_vectors([infile1], infile2)
