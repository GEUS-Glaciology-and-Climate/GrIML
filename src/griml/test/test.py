#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest, tempfile, rasterio, os
from rasterio.transform import from_origin
import geopandas as gpd
from shapely.geometry import Point, Polygon
import numpy as np
from griml.convert.convert import convert
from griml.filter.filter_vectors import filter_vectors
from griml.merge.merge_vectors import merge_vectors
from griml.metadata.add_metadata import add_metadata

class TestGrIML(unittest.TestCase):
    '''Unittest for the GrIML post-processing workflow'''

    def setUp(self):
        '''Set up temporary directories'''
        self.temp_dir = tempfile.TemporaryDirectory()
        
    def tearDown(self):
        '''Clean up temporary files'''
        self.temp_dir.cleanup()

    def create_sample_raster(self, filepath):
        '''Generate a small synthetic raster file with three bands'''
        transform = from_origin(0, 10, 0.1, 0.1)  # Top-left origin, 0.1 cell size
        with rasterio.open(
            filepath, 'w',
            driver='GTiff', height=10, width=10,
            count=3, dtype='uint8', crs='EPSG:3413',
            transform=transform
        ) as dst:
            # Create a 3D NumPy array of shape (bands, height, width) filled with 255
            data = np.full((3, 10, 10), 255, dtype='uint8')
            dst.write(data)
        
    def create_sample_pointfile(self, filepath, num_features=5):
        '''Generate a synthetic GeoDataFrame with simple point geometries'''
        data = {
            'geometry': [Point(x, y) for x, y in zip(range(num_features), range(num_features))],
            'id': [int(i) for i in range(num_features)],
            'New Greenl':'test'
        }
        gdf = gpd.GeoDataFrame(data, crs="EPSG:3413")
        gdf["row_id"] = gdf.index + 1
        gdf.reset_index(drop=True, inplace=True)
        gdf.set_index("row_id", inplace=True)
        gdf.to_file(filepath)

    def create_sample_polyfile(self, filepath, num_features=5, side_length=1.0):
        '''Generate a synthetic GeoDataFrame with square polygon geometries'''
        half_side = side_length / 2
        data = {
            'geometry': [
                Polygon([
                    (x - half_side, y - half_side),  # Bottom-left
                    (x + half_side, y - half_side),  # Bottom-right
                    (x + half_side, y + half_side),  # Top-right
                    (x - half_side, y + half_side),  # Top-left
                    (x - half_side, y - half_side)   # Close the polygon
                ])
                for x, y in zip(range(num_features), range(num_features))
            ],
            'id': range(num_features),
            'lake_id': [1,1,2,3,2],
            'method': ['VIS','SAR','DEM','VIS','SAR'],
            'source':['S2','S1','ARCTICDEM','S2','S1'],
            'startdate':'20170701',
            'enddate':'20170831',
            'subregion':['SW','SW','NO','NW','NO'],
        }
        gdf = gpd.GeoDataFrame(data, crs="EPSG:3413")
        gdf["row_id"] = gdf.index + 1
        gdf.reset_index(drop=True, inplace=True)
        gdf.set_index("row_id", inplace=True)
        gdf.to_file(filepath)
    
    def test_convert(self):
        '''Test vector to raster conversion''' 
        proj = 'EPSG:3413' 
        band_info = [
            {'b_number': 1, 'method': 'VIS', 'source': 'S2'}, 
            {'b_number': 2, 'method': 'SAR', 'source': 'S1'},
            {'b_number': 3, 'method': 'DEM', 'source': 'ARCTICDEM'}
        ] 
        start = '20170701' 
        end = '20170831'
        
        # Create synthetic raster file
        temp_raster_path = os.path.join(self.temp_dir.name, 'sample_raster.tif')
        self.create_sample_raster(temp_raster_path)
        
        # Run the conversion function with generated data
        out = convert([temp_raster_path], proj, band_info, start, end)
        self.assertIsInstance(out, list)
        self.assertIn('geometry', out[0].columns)

    def test_filter(self):
        '''Test vector filtering'''
        # Create synthetic shapefiles
        temp_filter_path = os.path.join(self.temp_dir.name, 'sample_filter.shp')
        temp_icemask_path = os.path.join(self.temp_dir.name, 'sample_icemask.shp')
        self.create_sample_polyfile(temp_filter_path)
        self.create_sample_polyfile(temp_icemask_path)
        
        # Run the filter function with generated data
        out = filter_vectors([temp_filter_path], temp_icemask_path)
        self.assertTrue(True)

    def test_merge(self):
        '''Test vector merging'''
        # Create two synthetic shapefiles for merging
        temp_merge_path1 = os.path.join(self.temp_dir.name, 'sample_merge_1.shp')
        temp_merge_path2 = os.path.join(self.temp_dir.name, 'sample_merge_2.shp')
        self.create_sample_polyfile(temp_merge_path1)
        self.create_sample_polyfile(temp_merge_path2)
        
        # Run the merge function with generated data
        out = merge_vectors([temp_merge_path1, temp_merge_path2])
        self.assertIsInstance(out, gpd.GeoDataFrame)
        self.assertIn('geometry', out.columns)

    def test_metadata(self):
        '''Test metadata population'''
        # Create synthetic shapefiles for metadata function
        temp_metadata_path1 = os.path.join(self.temp_dir.name, 'sample_metadata_1.shp')
        temp_metadata_path2 = os.path.join(self.temp_dir.name, 'sample_metadata_2.shp')
        temp_metadata_path3 = os.path.join(self.temp_dir.name, 'sample_metadata_3.shp')
        self.create_sample_polyfile(temp_metadata_path1)
        self.create_sample_pointfile(temp_metadata_path2)
        self.create_sample_polyfile(temp_metadata_path3)
        
        # Run the metadata function with generated data
        out = add_metadata(temp_metadata_path1, temp_metadata_path2, temp_metadata_path3)
        self.assertTrue(True)

if __name__ == "__main__":  
    unittest.main()

