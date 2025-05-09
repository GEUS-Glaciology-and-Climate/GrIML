#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import geopandas as gp
import glob
from pathlib import Path


def inventory_general_stats(file1, outfile=None): 
    '''Calculate general statistics on a lake inventory file
    
    Parameters
    ----------
    geofile : gpd.str
        File path to lake dataframe
    outfile : str
        Outputted file name for general statistics
    '''
    print('Retrieving lake data...') 
    geofile = gp.read_file(file1)
    geofile = geofile.sort_values('region')    
    uniquebasin = list(geofile['region'].unique())
    uniquesource = list(geofile['source'].unique())
    
    print('Aggregating lake data...')
    agg_geofile = geofile.dissolve(by='lake_id')
    agg_geofile['area_sqkm']=[g.area/10**6 for g in list(agg_geofile['geometry'])]
    agg_geofile['length_km']=[g.length/1000 for g in list(agg_geofile['geometry'])]
    agg_geofile.sort_values('region')  

    print('\nStarting general statistics...')    
    readout=''
    readout=readout+'Total number of detected lakes: ' + str(len(list(geofile['lake_id']))) + '\n'
    readout=readout+'Total number of unique lakes: ' + str(geofile['lake_id'].max()) + '\n\n'

    # Total lake count for each ice sheet sector
    geofile_icesheet = geofile[geofile['margin'] == 'ICE_SHEET']
    agggeofile_icesheet = agg_geofile[agg_geofile['margin'] == 'ICE_SHEET']
    readout=readout+'Ice Sheet total lake count\n' 
    for i in uniquebasin:
        readout=readout+i + ' total lake count: ' + str(geofile_icesheet['region'].value_counts()[i]) + '\n'
    readout=readout+'Ice sheet total lake count: ' + str(len(geofile_icesheet))
    readout=readout+'\n\n'
    
    # Unique lake count for each ice sheet sector
    readout=readout+'Ice Sheet unique lake count\n' 
    for i in uniquebasin:
        readout=readout+i + ' unique lake count: ' + str(agggeofile_icesheet['region'].value_counts()[i]) + '\n'
    readout=readout+'Ice sheet total unique lake count: ' + str(len(agggeofile_icesheet ))
    readout=readout+'\n\n'

    # Total lake count for each ice cap sector
    geofile_icecap = geofile[geofile['margin'] == 'ICE_CAP']
    agggeofile_icecap = agg_geofile[agg_geofile['margin'] == 'ICE_CAP']
    readout=readout+'Ice Cap total lake count\n'
    for i in uniquebasin:
        readout=readout+i + ' total lake count: ' + str(geofile_icecap['region'].value_counts()[i]) + '\n'
    readout=readout+'Ice cap total lake count: ' + str(len(geofile_icecap))
    readout=readout+'\n\n'
    
    # Unique lake count for each ice cap sector
    readout=readout+'Ice Cap unique lake count\n' 
    for i in uniquebasin:
        readout=readout+i+ ' unique lake count: ' + str(agggeofile_icecap['region'].value_counts()[i]) + '\n'
    readout=readout+'Ice cap total unique lake count: ' + str(len(agggeofile_icecap))
    readout=readout+'\n\n'

    # Source count
    for i in uniquesource:
        readout=readout+'Lakes detected using ' + i + ': ' + str(geofile['source'].value_counts()[i]) + '\n'
    readout=readout+'\n'
    
    # Min, max and average lake area
    readout=readout+'Min. lake area (km): ' + str(agg_geofile['area_sqkm'].min()) + '\n'
    readout=readout+'Max. lake area (km): ' + str(agg_geofile['area_sqkm'].max()) + '\n'
    readout=readout+'Average lake area (km): ' + str(agg_geofile['area_sqkm'].max()) + '\n\n'
 
    # Min, max and average uncertainty
    readout=readout+'Min. uncertainty: ' + str(agg_geofile['certainty'].min()) + '\n'
    readout=readout+'Max. uncertainty: ' + str(agg_geofile['certainty'].max()) + '\n'
    readout=readout+'Average uncertainty: ' + str(agg_geofile['certainty'].mean()) + '\n\n'

    print(readout)
                  
    # Open stats file   
    if outfile is not None:
        print('Writing general stats file...')
        f = open(outfile, 'w+')
        f.write(readout)    
        f.close()
    
    return readout

if __name__ == "__main__": 
 
    workspace1 = '*IML-fv2.shp'
    out_dir = 'stats/'
    for f in list(glob.glob(workspace1)):
        name = str(Path(f).stem)
        year = str(Path(f).stem)[0:4]
        out_file = str(Path(out_dir).joinpath(name+'_general_stats.txt'))
        
        print('\n\n'+str(Path(f).stem))
        readout = inventory_general_stats(f, out_file)
        
