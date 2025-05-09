#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import numpy as np
import geopandas as gp
from scipy import stats


def region_stats_with_basin_info(infile1, infile2, infile3, outtxt):           
    '''Calculate region statistics on a lake inventory file, including basin 
    information such as basin margin length
    
    Parameters
    ----------
    infile1 : str
        File path to lake geodataframe
    infile2 : str
        File path to basin (as polygons) geodataframe
    infile2 : str
        File path to basin (as lines) geodataframe
    outfile : str
        Outputted file name for general statistics
    '''
    
    print('\nLoading geodataframes...')    

    #Read file as geopandas index
    geofile = gp.read_file(infile1)
    basinfile = gp.read_file(infile2)
    extfile = gp.read_file(infile3)
    agg_geofile = geofile.dissolve(by='lake_id')


    print('\nRetrieving lake data...')

    #Get data from columns
    geofile = geofile.sort_values('region')
    geofile_basin = geofile['region'].tolist()          #Get lake location

    geofile['area'] = geofile['geometry'].area/10**6
    geofile_area = geofile['area'].tolist() 

    #Get all lake data for basins
    geofile_SW=[]
    geofile_NE=[]
    geofile_SE=[]
    geofile_CW=[]
    geofile_CE=[]
    geofile_NO=[]
    geofile_NW=[]
    label=['CW', 'CE', 'NE', 'NO', 'NW', 'SE', 'SW']
    geofile_arealist=[geofile_CW,geofile_CE,geofile_NE,geofile_NO,geofile_NW,
                       geofile_SE,geofile_SW]

    for i in range(len(geofile_basin)):
        for l in range(len(label)):
            if label[l] in geofile_basin[i]:
                geofile_arealist[l].append(geofile_area[i])


    print('\nRetrieving basin area data...')

    #Get basin info        
    basinfile.sort_values('Subregion')
    basinfile['area'] = basinfile['geometry'].area/10**6
    basinfile['total_perimeter'] = basinfile['geometry'].length

    basinfile["row_id"] = basinfile.index + 1
    basinfile.reset_index(drop=True, inplace=True)
    basinfile.set_index("row_id", inplace = True)                       
    basinfile_area = basinfile['area'].tolist()  
    basinfile_name = basinfile['Subregion'].tolist()

    print(basinfile_name)
    print(basinfile_area)

    basinfile['total_perimeter'] = basinfile['geometry'].length


    print('\nRetrieving basin perimeter data...')

    extfile=extfile.sort_values('Subregion') 
    extfile = extfile.dissolve(by='Subregion')         
    extfile['LENGTH'] = extfile['geometry'].length/1000
    perimfile_length = extfile['LENGTH'].tolist()  


    print('\nAggregating lake data...')

    #Get data from columns
    agg_geofile['area'] = geofile['geometry'].area
    agg_geofile['length'] = geofile['geometry'].length
    agg_geofile.sort_values('region')  
    aggfile_basin = agg_geofile['region'].tolist()    #Get lake location
    aggfile_area = agg_geofile['area'].tolist()           #Get lake area

    aggfile_areakm = []
    for i in aggfile_area:
        aggfile_areakm.append(i/10**6)

    #Get all lake data for basins
    aggfile_CW=[]
    aggfile_CE=[]
    aggfile_NE=[]
    aggfile_NO=[]
    aggfile_NW=[]
    aggfile_SE=[]
    aggfile_SW=[]
    label=['CW', 'CE', 'NE', 'NO', 'NW', 'SE', 'SW']
    aggfile_arealist=[aggfile_CW,aggfile_CE,aggfile_NE,aggfile_NO,aggfile_NW,
                       aggfile_SE,aggfile_SW]
    for i in range(len(aggfile_basin)):
        for l in range(len(label)):
            if label[l] in aggfile_basin[i]:
                aggfile_arealist[l].append(aggfile_areakm[i])


    #Get all lake data for basins, rounded
    aggfiler_CW = [round(n, 2) for n in aggfile_CW]
    aggfiler_NE = [round(n, 2) for n in aggfile_NE]
    aggfiler_NO = [round(n, 2) for n in aggfile_NO]
    aggfiler_NW = [round(n, 2) for n in aggfile_NW]
    aggfiler_SE = [round(n, 2) for n in aggfile_SE]
    aggfiler_SW = [round(n, 2) for n in aggfile_SW]
    aggfile_arealist_round=[aggfiler_CW,aggfiler_NE,aggfiler_NO,aggfiler_NW,
                            aggfiler_SE,aggfiler_SW]              

    print('Writing detailed stats file...')
    
    #Open stats file    
    f = open(outtxt, 'w+')
    
    f.write('Basin, Basin area, Basin perimeter, Number of lakes, Total lake area (km),' + 
            'Average lake area (km), Median lake area (km), Mode lake area (w/ count), Standard deviation, ' +
            ' % basin area covered by lakes, Lake frequency (average dist. btwn lakes)' + '\n')
    
    for i in range(len(basinfile_name)):
        f.write(str(basinfile_name[i]) + ',' +                                     #Basin name
                str(basinfile_area[i]) + ',' +                                     #Basin area
                str(perimfile_length[i]) + ',' +                                   #Basin perimeter
                str(aggfile_basin.count(label[i])) + ',' +                         #Unique lakes
                str(sum(aggfile_arealist[i])) + ',' +                              #Total lake area
                str(np.average(aggfile_arealist[i])) + ',' +                       #Aver. lake area
                str(np.median(aggfile_arealist[i])) + ',' +                        #Median lake area
                str(stats.mode(aggfile_arealist_round[i]).mode[0]) + ' (' + 
                str(stats.mode(aggfile_arealist_round[i]).count[0]) + '),' +       #Mode lake area
                str(np.std(aggfile_arealist[i])) + ',' +                           #Standard deviation
                str((sum(aggfile_arealist[i])/basinfile_area[i])*100) + ',' +      #% basin covered by lakes
                str(perimfile_length[i]/len(aggfile_arealist[i])) +                #Lake frequency along perimeter
                '\n')
    
    f.close()  

if __name__ == "__main__":  
    file1 = '20230101-ESA-GRIML-IML-fv2.gpkg'
    file2 = 'greenland_basins_polarstereo.shp'
    file3 = 'greenland_basins_polarstereo_lines.shp'
    
    outtxt = 'basin_stats.csv'
    
    region_stats_with_basin_info(file1, file2, file3, outtxt)
