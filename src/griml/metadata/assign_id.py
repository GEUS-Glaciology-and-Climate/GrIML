#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from scipy.sparse.csgraph import connected_components
import geopandas as gpd

__all__ = ["assign_id",
           "assign_id_from_geometries",
]

def assign_id(gdf, col_name="lake_id"):
    """Assign unique identification numbers to non-overlapping geometries in
    geodataframe
    
    Parameters
    ----------
    gdf : geopandas.GeoDataFrame
        Vectors to assign identification numbers to
    col_name : str
        Column name to assign ID from
    
    Returns
    -------
    gdf : geopandas.GeoDataFrame
        Vectors with assigned IDs
    """
    # Find overlapping geometries
    geoms = gdf["geometry"]
    geoms.reset_index(inplace=True, drop=True)        
    overlap_matrix = geoms.apply(lambda x: geoms.overlaps(x)).values.astype(int)
    
    # Get unique ids for non-overlapping geometries
    n, ids = connected_components(overlap_matrix)
    ids=ids+1
    
    # Assign ids and realign geodataframe index 
    gdf[col_name]=ids
    gdf = gdf.sort_values(col_name)
    gdf.reset_index(inplace=True, drop=True) 
    return gdf


def assign_id_from_geometries(gdf1, gdf2, col_name="lake_id"):
    """Assign unique identification numbers based on identifications from
    a set of geometries

    Parameters
    ----------
    gdf1 : geopandas.GeoDataFrame
        Vectors to assign identification numbers to
    gdf2 : geopandas.GeoDataFrame
        Vectors to assign identification numbers from
    col_name : str
        Column name to assign ID from and to

    Returns
    -------
    gdf_out : geopandas.GeoDataFrame
        Vectors with assigned IDs
    """

    # Make sure both are in the same CRS
    gdf2 = gdf2.to_crs(gdf1.crs)

    # Spatial join: attributes from gdf2 → gdf1
    joined = gpd.sjoin(
        gdf1,
        gdf2[[col_name, "geometry"]],
        how="left",
        predicate="intersects"  # or 'within', 'contains', etc.
    )

#    joined = joined.dissolve(by=[col_name])
    return joined