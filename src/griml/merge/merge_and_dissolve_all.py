#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import geopandas as gpd
import pandas as pd
import glob
from pathlib import Path

def merge_and_dissolve_all(indir, outdir):
    
    gdfs=[]
    for g in sorted(list(glob.glob(indir+'*IML-fv1.shp'))):
        print(g)
        gdf = gpd.read_file(g)
        year = str(Path(g).name)[0:4]
        col_name = 'temp_'+year
        gdf[col_name] = gdf['temp_aver']
        gdfs.append(gdf)
    
    all_gdf = pd.concat(gdfs)

    # Update geometry metadata
    print('Dissolving geometries...')
    all_gdf['idx'] = all_gdf['lake_id']    
    gdf_dissolve = all_gdf.dissolve(by='idx')
    gdf_dissolve = gdf_dissolve.sort_values(by='lake_id')
    gdf_dissolve['area_sqkm']=[g.area/10**6 for g in list(gdf_dissolve['geometry'])]
    gdf_dissolve['length_km']=[g.length/1000 for g in list(gdf_dissolve['geometry'])]
    gdf_dissolve['temp_all']= gdf_dissolve[['temp_2016', 'temp_2017', 'temp_2018',
                                             'temp_2019', 'temp_2020', 'temp_2021',
                                             'temp_2022', 'temp_2023']].mean(axis=1, skipna=True)

    # Add centroid position
    centroids = gdf_dissolve['geometry'].centroid
    centroids_xy = [str(c.x)+', '+str(c.y) for c in centroids]
    gdf_dissolve['centroid'] = centroids_xy

    # Reorder columns and index
    gdf_dissolve = gdf_dissolve[['geometry',
                   'lake_id',
                   'lake_name',
                   'margin',
                   'region',
                   'area_sqkm',
                   'length_km',
                   'centroid',
                   'temp_2016',
                   'temp_2017',
                   'temp_2018',
                   'temp_2019',
                   'temp_2020',
                   'temp_2021',
                   'temp_2022',
                   'temp_2023',
                   'temp_all',
                   'verified',
                   'verif_by',
                   'edited',
                   'edited_by']]

    # Save to file
    print('Saving merged geometries to file...')
    gdf_dissolve.to_file(outdir+'ALL-ESA-GRIML-IML-MERGED-fv1.gpkg')
    
    # Add centroid position
    print('Saving centroid geometries to file...')
    gdf_dissolve['geometry'] = gdf_dissolve['geometry'].centroid
    gdf_dissolve.to_file(outdir+'ALL-ESA-GRIML-IML-MERGED-centroids-fv1.gpkg')

    return gdf_dissolve

#if __name__ == "__main__":
#    indir = "."
#    outdir = indir
#    merge_and_dissolve_all(indir, outdir)
