#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__all__ = ['dissolve_by_id']

def dissolve_by_id(gdf):
    gdf['idx'] = gdf['lake_id']
    gdf['method2'] = gdf['method']
    gdf_dissolve = gdf.dissolve(by=['idx', 'method2'])
    gdf_dissolve = gdf_dissolve.sort_values(by='lake_id')

    gdf_dissolve['area_sqkm'] = [g.area / 10 ** 6 for g in list(gdf_dissolve['geometry'])]
    gdf_dissolve['length_km'] = [g.length / 1000 for g in list(gdf_dissolve['geometry'])]

    centroids = gdf_dissolve['geometry'].centroid
    centroids_xy = [str(c.x) + ', ' + str(c.y) for c in centroids]
    gdf_dissolve['centroid'] = centroids_xy

    return gdf_dissolve
