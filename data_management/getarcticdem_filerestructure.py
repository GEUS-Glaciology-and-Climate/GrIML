# -*- coding: utf-8 -*-
"""
Quick fix for changing file structure for ADEM files

@author: HOW
"""
from pathlib import Path
from urllib.parse import urlparse
from urllib.request import HTTPError
import sys, os
from datetime import datetime
import tarfile
import shutil

#------------------------------------------------------------------------------

def getFolders(rootdirectory, datatype, version, resolution):
    '''Get scene folder directories, based on tile name.
    Args
    scenes (str):           Folder directory where scenes are located.
    
    Returns
    tiles (list):           List of folder directories with specified tiles
    '''
    
    #Create path object from string
    root = Path(rootdirectory)
    
    #Reformat inputs if needed
    if datatype in ['mosaic', 'MOSAIC']:
        datatype='MOSAIC'
    elif datatype in ['strip', 'STRIP']:
        datatype='STRIP'
    else:
        sys.exit('Invalid datatype variable: ' + str(datatype))
    
    if version in ['3.0', '3', 'v3.0', 'v3']:
        version='v3.0'
    elif version in ['2.0', '2', 'v2.0', 'v2']:
        version='v2.0'
    elif version in ['1.0', '1', 'v1.0', 'v1']:
        version='v1.0'
    else:
        sys.exit('Invalid version variable: ' + str(version))

    if resolution in ['2','2m']:
        resolution = '2m'
    elif resolution in ['10','10m']:
        resolution = '10m'
    elif resolution in ['32','32m']:
        resolution = '32m'
    elif resolution in ['100','100m']:
        resolution = '100m'
    elif resolution in ['500','500m']:
        resolution = '500m'
    elif resolution in ['1000','1000m','1km']:
        resolution = '1km'
    else:
        sys.exit('Invalid resolution variable: ' + str(resolution))
        
    #Merge tile name with directory and check if it exists
    tilepath = root.joinpath('ArcticDEM', datatype, version)
           
    #Get all directories in tile folder and append to output
    pathlist1 = list(tilepath.glob('*'))

    #Append resolution to each path
    pathlist2=[]
    for p in pathlist1:
        pathlist2.append(p.joinpath(resolution))
     
    #Return list of folder directories with specified tiles
    return pathlist2

#------------------------------------------------------------------------------

def extractTar(pathout1, pathout2, remove=False):    
    '''Extract all elements from a .tar.gz file to a given file directory. 
    Files are structured as the .tif file in the upper level of the directory,
    then all other files stored in a folder called "ADEM".
    
    Variables 
    pathout1 (str):             Folder path to intended location of extracted 
                                files
    pathout2 (str):             Filepath to zipped files
    remove (bool):              Flag denoting whether zipped filed should be
                                deleted after extraction is complete
    '''
    #Extract all elements from tar folder       
    if str(pathout2.suffix) in ['.tar','.gz']:
        tf=tarfile.open(pathout2, 'r')
        for member in tf.getmembers():
            pathname = Path(member.name)          
            if pathname.suffix=='.tif':
                tarpath = member.name
            else:
                tarpath = Path('ADEM').joinpath(str(member.name))            
            member.path = str(tarpath)           
            tf.extract(member, pathout1)       
        tf.close()
    
        #Print statement to check output
        print('Unzipped to ' + str(pathout1))    
              
    #Remove zip file
    if remove is True:
        print('Removing ' + str(pathout2))
        try:
            os.remove(str(pathout2))
            print('File successfully removed\n')  
        except:
            print('File could not be removed, check permissions\n') 
            
#------------------------------------------------------------------------------

def createINFO(filepath, pathout, product, release):
    '''Function to generate INFO.txt file for ArcticDEM data.
    
    Variables
    filepath (str):             Filepath to downloaded .tar.gz ArcticDEM file
    pathout (str):              Location for INFO.txt file
    '''
    #Change file directories to Path objects
    filepath=Path(filepath)
    pathout=Path(pathout)
    info = str(filepath.name).split('_')
    
    #Construct text file   
    f=open(pathout.joinpath('INFO.txt'), 'w')
    f.write('SCENE INFORMATION\n\n')
    f.write('Original file location: ' + str(filepath) + '\n')
#    f.write('Unzipped on ' + str(datetime.now()) + ' by ' + str(os.getlogin()) 
#            + '\n\n')  
    f.write('Moved from external hard drive E:/ArcticDEM/mosaic/v3.0/2m/ on ' 
            + str(datetime.now()) + ' by ' + str(os.getlogin()) + '\n\n') 

    #Write appropriate info based on product type (mosaic or strip)  
    if product in 'mosaic':    
        if len(info)>6:        
            meta1 = ['Tile identifier (100 km x 100 km): ', 
                     'Tile identifier (50 km x 50 km): ','Resolution: ', 
                     'Version: ']
            f.write('Data type: ArcticDEM mosaic\n') 
            meta2 = [str(info[0])+'_'+str(info[1]), str(info[2])+'_'+str(info[3]), 
                     info[4], str(info[5]).split('.')[0]+' ('+str(release)+')']
        
        else: 
            meta1 = ['Tile identifier (100 km x 100 km): ', 'Resolution: ', 
                     'Version: ']
            f.write('Data type: ArcticDEM mosaic\n') 
            meta2 = [str(info[0])+'_'+str(info[1]), info[2], 
                     info[3]+' ('+str(release)+')']
        
        for m1,m2 in zip(meta1, meta2):
            f.write(m1 + m2 + '\n')
    
#    elif product in 'strip': 
#        meta1 = ['Tile identifier (100 km x 100 km): ', 
#                 'Tile identifier (50 km x 50 km): ', 'Resolution: ',
#                 'Version: ']
#        f.write('Data type: ArcticDEM strip \n')  
#       
#        meta2 = [str(info[0])+'_'+str(info[1]), 
#                           str(info[2])+'_'+str(info[3]), info[4], info[5]]
#
#        
#        for m1,m2 in zip(meta1, meta2):
#            f.write(m1 + m2 + '\n')
               
    #Print statement to check output directory
    f.close()
    print('Textfile saved to ' + str(pathout))
    
#------------------------------------------------------------------------------
    
#Directory to unzip files to
rootdirectory=Path('E:/ArcticDEM/mosaic/v3.0/2m/')

#Output directory
#outdirectory = Path('D:/sat/')
outdirectory = Path('G:/Satellitdata/ArcticDEM/')


#Map output directory structure
roots = ['ArcticDEM','MOSAIC','v3.0','2m']
for r in roots:
    outdirectory = outdirectory.joinpath(r)
    if os.path.exists(str(outdirectory)) is False:
        os.makedirs(str(outdirectory))
print(outdirectory)


count=1


##COPYING AND EXTRACTING 
##Iterate through folders
#for r in list(rootdirectory.glob('*')):
#    
#    #If name is tile id
#    if len(str(r.name))==5:
#        print('\n\n' + str(count) + '. Copying files from ' + str(r))
#        
#        #Iterate through subfolders
#        for s in list(r.glob('*')):
#            if str(s.suffix) in ['.tar','.gz']:
#                print('\nExtracting ' + str(s))
#                tileid1 = str(s.name).split('_')[0]+'_'+str(s.name).split('_')[1]                
#                tileid2 = str(s.name).split('_')[2]+'_'+str(s.name).split('_')[3]
#                out = outdirectory
#                for path in [tileid1, tileid2]:
#                    out = out.joinpath(path)
#                    if os.path.exists(str(out)) is False:
#                        os.makedirs(str(out))
#                if len(os.listdir(str(out)))==0: 
#                    extractTar(out, s, remove=False)   
#                    createINFO(str(s), str(out), 'mosaic', 'release 4')
#                else:
#                    print('Files already exist in at ' + str(out))
#                    print('Moving to next file')  
#        count=count+1


##COPY ADEM TIF WITH ALL METADATA
#count=1
#for i in list(rootdirectory.glob('*')):
#    print(str(count) + '. Copying file from ' + str(i))
#    out = outdirectory
#
#    if os.path.isfile(str(i)) is True:
#        if str(i.suffix) in ['.tif', '.TIF']:
#            parts1 = str(i.name).split('_')
#            parts2 = [parts1[0]+'_'+parts1[1], parts1[2]+'_'+parts1[3]]
#            for p in parts2:
#                out = out.joinpath(p)
#                if os.path.exists(str(out)) is False:
#                    os.mkdir(str(out))            
#            shutil.copyfile(str(i), str(out.joinpath(str(i.name))))
#            
#
#        elif str(i.suffix) in ['.txt', '.TXT']:
#            parts1 = str(i.name).split('_')
#            out = out.joinpath(parts1[0]+'_'+parts1[1])
#            if os.path.exists(str(out)) is False:
#                os.mkdir(str(out))            
#            dirlist=['1_1','1_2','2_1','2_2']
#            for d in dirlist:
#                new_out=out
#                parts2=[d, 'ADEM']
#                for p in parts2:                    
#                    new_out = new_out.joinpath(p)
#                    if os.path.exists(str(new_out)) is False:
#                        os.mkdir(str(new_out))                        
#                shutil.copyfile(str(i), str(new_out.joinpath(str(i.name))))
#                
#                
#    else:
#        for j in list(i.glob('*')):
#            parts1 = str(j.name).split('_')
#            new_out = out
#            parts2 = [parts1[0]+'_'+parts1[1], parts1[2]+'_'+parts1[3], 'ADEM']
#            for p in parts2:                    
#                new_out = new_out.joinpath(p)
#                if os.path.exists(str(new_out)) is False:
#                    os.mkdir(str(new_out))
#            shutil.copyfile(str(j), str(new_out.joinpath(str(j.name))))
#    
#    count=count+1
       

#COPY ADEM TIF WITH NO METADATA
count=1
for i in list(rootdirectory.glob('*')):
    print(str(count) + '. Copying file from ' + str(i))
    for f in list(i.glob('*')):
        out = outdirectory
        if str(f.suffix) in ['.tif', '.TIF']:
            parts1 = str(f.name).split('_')
            parts2 = [parts1[0]+'_'+parts1[1], parts1[2]+'_'+parts1[3]]
            for p in parts2:
                out = out.joinpath(p)
                if os.path.exists(str(out)) is False:
                    os.makedirs(str(out))
            if os.path.isfile(str(out.joinpath(str(f.name)))) is False:
                print('Copying file ' + str(f.name))
                shutil.copyfile(str(f), str(out.joinpath(str(f.name))))
            else:
                print(str(f.name) + ' already exists')
    count=count+1
            

for i in outdirectory.glob('*/*'):
    filepath = list(i.glob('*.tif'))[0]
    print(filepath)    
    createINFO(filepath, i, 'mosaic', 'release 7')