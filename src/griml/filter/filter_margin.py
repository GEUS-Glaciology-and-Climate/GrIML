#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import geopandas as gpd

#try:
#    import dask_geopandas as dg
#except ImportError as e:
#    raise ImportError(
#        "The optional dependency 'dask_geopandas is required for parallelization "
#        "functionality. To use, please install with "
#        "`conda install dask_geopandas -c conda-forge`"
#    )

__all__ = ["filter_margin"]
#           "filter_margin_with_dask"]


def filter_margin(iml, margin_buffer):
    """Filter vectors by polygon (such as a margin buffer) using a spatial join
    
    Parameters
    ----------
    iml : geopandas.GeoDataframe
        Vector object to filter by area
    margin_buffer: geopandas.GeoSeries
        Vector shape which will be used to filter
    
    Returns
    -------
    iml : geopandas.GeoDataframe
        Filtered vector object
    """
    if len(margin_buffer)==1:
        geom = margin_buffer.geometry.iloc[0]
    else:
        geom = margin_buffer.unary_union

#    iml = gpd.sjoin(iml, margin_buffer, how="left")
#    iml = iml[iml["index_right"]==0]
#    iml = iml.drop(columns="index_right")

    iml = iml[iml.intersects(geom)]

    # Calculate geometry info
    iml.reset_index(inplace=True, drop=True)
    return iml


#def filter_margin_with_dask(iml, margin_buffer):
#    """Filter vectors by polygon (such as a margin buffer) using a spatial join in parallel
#    using dask-geopandas
#
#    Parameters
#    ----------
#    iml : geopandas.GeoDataframe
#        Vector object to filter by area
#    margin_buffer: geopandas.GeoSeries
#        Vector shape which will be used to filter
#
#    Returns
#    -------
#    iml : geopandas.GeoDataframe
#        Filtered vector object
#    """
#    iml_d = dg.from_geopandas(iml, npartitions=4)
#    iml_d = iml_d.spatial_shuffle(by="hilbert")
#    iml_d = dg.sjoin(iml_d, margin_buffer, how="inner").compute()
#    iml_d = iml_d.reset_index(drop=True)
#
#    return iml_d