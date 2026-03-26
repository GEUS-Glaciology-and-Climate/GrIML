import geopandas as gpd
__all__ = ["assign_attributes_from_dataframe"]

def assign_attributes_from_dataframe(gdf1, gdf2):
    """Assign attributes based on those of overlapping
     polygons from another geodataframe

    Parameters
    ----------
    gdf1 : geopandas.GeoDataFrame
        Vectors to assign attributes to
    gdf2 : geopandas.GeoDataFrame
        Vectors to assign attributes from

    Returns
    -------
    gdf_out : geopandas.GeoDataFrame
        Vectors with new attributes
    """

    # Make sure both are in the same CRS
    gdf2 = gdf2.to_crs(gdf1.crs)

    # Spatial join: attributes from gdf2 → gdf1
    joined = gpd.sjoin(
        gdf1,
        gdf2,
        how="left",
        predicate="intersects"  # or 'within', 'contains', etc.
    )

#    joined = joined.dissolve(by=[col_name])
    return joined