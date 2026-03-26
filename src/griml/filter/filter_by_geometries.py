#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__all__ = ["filter_by_geometries"]

def filter_by_geometries(gdf1, gdf2):
    """Assign unique identification numbers from file (a file containing
    points/polygons with baseline identifications)

    Parameters
    ----------
    gdf1 : geopandas.GeoDataFrame
        Vectors to assign identification numbers to
    gdf2 : geopandas.GeoDataFrame
        Vectors to assign identification numbers from

    Returns
    -------
    gdf_out : geopandas.GeoDataFrame
        Vectors with assigned identification numbers
    """
    gdf1_corr = gdf1[gdf1.geometry.notnull()]
    gdf2_corr = gdf2[gdf2.geometry.notnull()]
    print(f"Dropped invalid geometries from gdf1: {len(gdf1)-len(gdf1_corr)}")
    print(f"Dropped invalid geometries from gdf2: {len(gdf2)-len(gdf2_corr)}")

    # Ensure same CRS
    if gdf1_corr.crs != gdf2_corr.crs:
        gdf2_corr = gdf2_corr.to_crs(gdf1_corr.crs)

    # Use spatial join with intersects predicate
    print(f"Number of geometries before filtering: {len(gdf1_corr)}")

    result = gdf1_corr.sjoin(
        gdf2_corr[['geometry']],
        predicate="intersects",
        how="inner"
    )
    print(f"Remaining geometries after filtering: {len(result)}")

    # Remove join index
    return result.drop(columns="index_right")