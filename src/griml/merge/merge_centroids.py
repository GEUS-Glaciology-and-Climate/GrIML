#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import geopandas as gpd
import pandas as pd
import glob


def merge_centroids(infile, centroid_file, outfile):
    # Open file as geodataframe
    gdf = gpd.read_file(infile)

    # Open point file and add centroid xy positions
    gdf_centroids = gpd.read_file(centroid_file)
    gdf_centroids = gdf_centroids.sort_values(by='lake_id')
    centroids_xy = [str(c.x)+', '+str(c.y) for c in list(gdf_centroids['geometry'])]
    gdf_centroids['centroid'] = centroids_xy
    print(gdf_centroids.crs)
    gdf_centroids = gdf_centroids[['lake_id', 'centroid']]
    print(gdf_centroids.columns)

    # Merge centroids attributes based on lake_id
    gdf_merged = gdf.merge(gdf_centroids, on='lake_id', how='left')
    print(gdf_merged.columns)

    # Reorder columns and index
    gdf_merged = gdf_merged[['geometry',
                     'lake_id',
                     'lake_name',
                     'margin',
                     'region',
                     'area_sqkm',
                     'length_km',
                     'centroid',
                     'temp_aver',
                     'temp_min',
                     'temp_max',
                     'temp_stdev',
                     'temp_count',
                     'temp_date',
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

    # Save to file
    print('Saving merged geometry to file...')
    gdf_merged.to_file(outfile)

if __name__ == "__main__":
    from pathlib import Path
    indir = "/home/pho/python_workspace/GrIML/misc/iml_2016-2023/final/with_lake_temps_100m_buffer/"
    centroid_file = "/home/pho/python_workspace/GrIML/misc/iml_2016-2023/final/with_lake_temps_100m_buffer_and_centroids/ALL-ESA-GRIML-IML-MERGED-centroids-fv1.gpkg"
    outdir = "/home/pho/python_workspace/GrIML/misc/iml_2016-2023/final/with_lake_temps_100m_buffer_and_centroids/"
    for infile in sorted(glob.glob(indir+'*IML-fv1.gpkg')):
        outfile = outdir + str(Path(infile).name)
        merge_centroids(infile, centroid_file, outfile)