import geopandas as gpd
import glob

def add_area_change(gdf_all, gdfs):
    """Add area from geodataframe series to master geodataframe"""
    gdf_all = gdf_all.sort_values(by="lake_id")

    for g in gdfs:
        year = list(g["startdate"])[0][0:4]
        col_name = "area_"+str(year)
        g[col_name] = g["area_sqkm"]
        gdf_all = gdf_all.merge(
            g[["lake_id", col_name]],
            on='lake_id',
            how='left'
        )

    return gdf_all
