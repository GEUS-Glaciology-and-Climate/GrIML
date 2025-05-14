# Dataset tutorials

The GrIML package is used for the production of the Greenland ice-marginal lake inventory series, which is freely available through the [GEUS Dataverse](https://doi.org/10.22008/FK2/MBKW9N). This dataset is a series of annual inventories, mapping the extent and presence of lakes across Greenland that share a margin with the Greenland Ice Sheet and/or the surrounding ice caps and periphery glaciers. 

Here, we will look at how to load and handle the dataset, and provide details on its contents.

```{note}
This tutorial is available as a [jupyter notebook](https://github.com/GEUS-Glaciology-and-Climate/GrIML/blob/main/test/dataset_tutorial.ipynb). We also provide a [Binder environment](https://mybinder.org/v2/gh/GEUS-Glaciology-and-Climate/GrIML/HEAD) within which you can run the notebook (with no need to set up the requirements yourself locally.
```

## Dataset contents

This ice-marginal lake dataset is a series of annual inventories, mapping the extent and presence of lakes across Greenland that share a margin with the Greenland Ice Sheet and/or the surrounding ice caps and periphery glaciers. Specifically, the following files are included in this dataset:

- *\<YYYYMMDD\>-ESA-GRIML-IML-\<version\>.gpkg*: Ice-marginal lake inventory for a specific year, provided as polygon vector features
- *ALL-ESA-GRIML-IML-\<version\>.gpkg*: All classified ice-marginal lakes across the inventory series, which have been merged together and therefore one polygon vector features signifies one lake
- *CURATED-ESA-GRIML-IML-\<version\>.gpkg*: All identified ice-marginal lakes across the inventory series, including manually-classified lakes, and provided as point vector features
- *README-ESA-GRIML-IML-\<version\>.gpkg*: This dataset readme file
  
The annual inventories provide a comprehensive record of all identified ice-marginal lakes, which have been detected using three independent remote sensing techniques:

- DEM sink detection using the ArcticDEM (mosaic version 3)
- SAR backscatter classification from Sentinel-1 imagery
- Multi-spectral indices classification from Sentinel-2 imagery

All data were compiled and filtered in a semi-automated approach, using a modified version of the [MEaSUREs GIMP ice mask](https://nsidc.org/data/NSIDC-0714/versions/1) to clip the dataset to within 1 km of the ice margin. Each detected lake was then verified manually. The methodology is open-source and provided in the associated [Github repository](https://github.com/GEUS-Glaciology-and-Climate/GrIML) for full reproducibility.

The inventory series was created to better understand the impact of ice-marginal lake change on the future sea level budget and the terrestrial and marine landscapes of Greenland, such as its ecosystems and human activities. The dataset is a complete inventory series of Greenland, with no absent data.

### Data format

The detected lakes are presented as polygon vector features in GeoPackage format (.gpkg), with coordinates provided in the WGS NSIDC Sea Ice Polar Stereographic North (EPSG:3413) projected coordinate system.

### Metadata

Each inventory in the inventory series contains the following metadata information:

| Variable name       | Description         | Format | 
|---------------------|---------------------|---------|
| `row_id`  	| Index identifying number for each polygon   | Integer  |
| `lake_id` 	| Identifying number for each unique lake  	| Integer  |
| `lake_name`| Lake placename, as defined by the [Oqaasileriffik (Language Secretariat of Greenland)](https://oqaasileriffik.gl) placename database which is distributed with [QGreenland](https://qgreenland.org/)  | String   |
| `margin`	| Type of margin that the lake is adjacent to (`ICE_SHEET`, `ICE_CAP`)   | String |
| `region`	| Region that lake is located, as defined by Mouginot and Rignot (2019) (`NW`, `NO`, `NE`, `CE`, `SE`, `SW`, `CW`)       	| String |
| `area_sqkm`	| Areal extent of polygon/s in square kilometres  | Float |
| `length_km`	| Length of polygon/s in kilometres         		| Float |
| `centroid`	| Centroid position (x,y) of lake, based on all classifications throughout the inventory series. Coordinates are provided in the WGS NSIDC Sea Ice Polar Stereographic North (EPSG:3413) projected coordinate system | String |
| `temp_aver`	| Average lake surface temperature estimate (in degrees Celsius), derived from the Landsat 8/9 OLI/TIRS Collection 2 Level 2 surface temperature data product  | Float |
| `temp_min`	| Minimum pixel lake surface temperature estimate (in degrees Celsius), derived from the Landsat 8/9 OLI/TIRS Collection 2 Level 2 surface temperature data product  | Float |
| `temp_max`	| Maximum pixel lake surface temperature estimate (in degrees Celsius), derived from the Landsat 8/9 OLI/TIRS Collection 2 Level 2 surface temperature data product  | Float |
| `temp_stdev`	| Average lake surface temperature estimate standard deviation, derived from the Landsat 8/9 OLI/TIRS Collection 2 Level 2 surface temperature data product  | Float |
| `temp_count`	| Number of Landsat 8/9 OLI/TIRS Collection 2 Level 2 scenes that lake surface temperature information were derived from. Scenes are only selected from the month of August  | Integer |
| `temp_date`	| Datetime of all Landsat 8/9 OLI/TIRS Collection 2 Level 2 scene acquisitions that lake surface temperature information are derived from  | String |
| `method`		| Method of classification (`DEM`, `SAR`, `VIS`)  | String |
| `source`     | Image source of classification (`ARCTICDEM`, `S1`, `S2`)    | String  |
| `all_src`     | List of all sources that successfully classified the lake (i.e. all classifications with the same `lake_name` value)  | String         |
| `num_src`          | Number of sources that successfully classified the lake (`1`, `2`, `3`)     | Integer | 
| `certainty`     | Certainty of classification, which is calculated from `all_src` as a score between `0` and `1`          | Float | -                             |
| `start_date` | Start date for classification image filtering 	| String  |
| `end_date` 	| End date for classification image filtering     | String |
| `verified` | Flag to denote if the lake has been manually verified (`Yes`, `No`)   | String |
| `verif_by`  | Author of verification | String  |
| `edited`  | Flag to denote if polygon has been manually edited (`Yes`, `No`)  | String   |
| `edited_by` | Author of manual editing   | String  |

## Getting started

The dataset is available on the [GEUS Dataverse](https://doi.org/10.22008/FK2/MBKW9N), which can be downloaded and unzipped either using wget:

```bash
$ wget -r -e robots=off -nH --cut-dirs=3 --content-disposition "https://dataverse.geus.dk/api/datasets/:persistentId/dirindex?persistentId=doi:10.22008/FK2/MBKW9N"
```

Or with Python:

```python
import wget

# Define urls
urls = ["https://dataverse.geus.dk/api/access/datafile/88448",
        "https://dataverse.geus.dk/api/access/datafile/88440",
        "https://dataverse.geus.dk/api/access/datafile/88442",
        "https://dataverse.geus.dk/api/access/datafile/88447",
        "https://dataverse.geus.dk/api/access/datafile/88446",
        "https://dataverse.geus.dk/api/access/datafile/88443",
        "https://dataverse.geus.dk/api/access/datafile/88445",
        "https://dataverse.geus.dk/api/access/datafile/88449",
        ]

# Download files
for u in urls:
    filename = wget.download(u)
```

One of the inventories in the dataset series can be opened and plotted in Python using geopandas. In this example, let's take the 2023 inventory (version 2):

```python
import geopandas as gpd
iml = gpd.read_file("20230101-ESA-GRIML-IML-fv2.gpkg")
iml.plot(color="red")
```

<img src="https://github.com/GEUS-Glaciology-and-Climate/GrIML/blob/main/docs/figures/iml_basic_plot.png?raw=true" alt="Basic plot example" width="400" align="aligncenter" />

```{important}
Make sure that the file path is correct in order to load the dataset correctly
```
   
Plotting all shapes can be difficult to see without zooming around and exploring the plot. We can dissolve all common lakes and then plot the centroid points of these to get a better overview:
 
```python    
iml_d = iml.dissolve(by="lake_id")
iml_d["centroid"] = iml_d.geometry.centroid
iml_d["centroid"].plot(markersize=0.5)
```

<img src="https://github.com/GEUS-Glaciology-and-Climate/GrIML/blob/main/docs/figures/iml_pt_plot.png?raw=true" alt="Point plot example" width="400" align="aligncenter" />


## Generating statistics

We can extract basic statistics from an ice-marginal lake inventory in the dataset series using simple querying. Let's take the 2022 inventory (version 2) in this example and first determine the number of classified lakes, and then the number of unique lakes:

```python
import geopandas as gpd

# Load inventory 
iml = gpd.read_file("20220101-ESA-GRIML-IML-fv2.gpkg")

# Dissolve by lake id to get all unique lakes as dissolved polygons
iml_d = iml.dissolve(by='lake_id')

# Print counts
print("Total number of detected lakes: " + str(len(iml)))
print("Total number of unique lakes: " + str(len(iml_d)))
```

We can count the number of classifications from each method, where `SAR` denotes classifications from SAR backscatter classification, `VIS` denotes classifications from multi-spectral indices, and `DEM` denotes classifications using sink detection:

```python
# Count lakes by classifications
print(iml['method'].value_counts())
```

Let's say we would like to count the number of ice-marginal lakes that share a margin with the Greenland Ice Sheet and broken down by region. We can do this by first extracting all lakes classified by a common margin with the ice sheet (`ICE_SHEET`) and then count all lakes per region:

```python
# Filter to lakes with an ice sheet margin
iml_d_ice_sheet = iml_d[iml_d['margin'] == 'ICE_SHEET']

# Count lakes by region
print(iml_d_ice_sheet['region'].value_counts())
```

We can also determine the average, minimum and maximum lake size per region:

```python
# Calculate surface area of all unique lakes (dissolved)
iml_d['area_sqkm'] = iml_d.geometry.area/10**6 

# Group lakes by region and determine average, min, max
print(iml_d.groupby(['region'])['area_sqkm'].mean())
print(iml_d.groupby(['region'])['area_sqkm'].min())
print(iml_d.groupby(['region'])['area_sqkm'].max())
```

## Cross inventory comparison

All inventories in the ice-marginal lake inventory series can be treated as time-series to look at change in lake abundance and size over time. Let's take an example where we will generate a time-series of lake abundance change at the margins of Greenland's periphery ice caps and glaciers. First we load all inventories as a series of GeoDataFrames:

```python
import glob
import numpy as np
import geopandas as gpd
import matplotlib.pyplot as plt

# Define directory
in_dir = '*IML-fv2.gpkg'

# Iterate through inventories
gdfs=[]
for f in list(sorted(glob.glob(in_dir))):
    
    # Load inventory and dissolve by unique identifications
    gdf = gpd.read_file(f)
    gdf = gdf.loc[gdf.geometry.is_valid]
    gdf = gdf.dissolve(by='lake_id')
    gdf['area_sqkm'] = gdf.geometry.area/10**6 
    
    # Append to list
    gdfs.append(gdf)
```

Then we count lakes with a shared ice cap/glacier margin from each inventory, splitting counts by region:

```python
# Create empty lists for region counts
b=['NW', 'NO', 'NE', 'CE', 'SE', 'SW', 'CW']
ic_nw=[]
ic_no=[]
ic_ne=[]
ic_ce=[]
ic_se=[]
ic_sw=[]
ic_cw=[]
ice_cap_abun = [ic_nw, ic_no, ic_ne, ic_ce, ic_se, ic_sw, ic_cw]

# Iterate through geodataframes
for g in gdfs:
    
    # Filter by margin type
    icecap = g[g['margin'] == 'ICE_CAP']
    
    # Append regional lake counts
    for i in range(len(b)):
        ice_cap_abun[i].append(icecap['region'].value_counts()[b[i]])
```

We can then plot all of our lake counts as a stacked bar plot:

```python
# Define plotting attributes
years=list(range(2016,2024,1))
col=['#045275', '#089099', '#7CCBA2', '#FCDE9C', '#F0746E', '#DC3977', '#7C1D6F']
bottom=np.zeros(8)

# Prime plotting area
fig, ax = plt.subplots(1, figsize=(10,5))

# Plot lake counts as stacked bar plots
for i in range(len(ice_cap_abun)):
    p = ax.bar(years, ice_cap_abun[i], 0.5, color=col[i], label=b[i], bottom=bottom)
    bottom += ice_cap_abun[i]
    ax.bar_label(p, label_type='center', fontsize=8)

# Add legend
ax.legend(bbox_to_anchor=(1.01,0.7))

# Change plotting aesthetics
ax.set_axisbelow(True)
ax.yaxis.grid(color='gray', linestyle='dashed', linewidth=0.5)
ax.set_facecolor("#f2f2f2")

# Add title
props = dict(boxstyle='round', facecolor='#6CB0D6', alpha=0.3)
ax.text(0.01, 1.05, 'Periphery ice caps/glaciers lake abundance change', 
         fontsize=14, horizontalalignment='left', bbox=props, transform=ax.transAxes)

# Add axis labels
ax.set_xlabel('Year', fontsize=14)
ax.set_ylabel('Lake abundance', fontsize=14)

# Show plot
plt.show()
```

<img src="https://github.com/GEUS-Glaciology-and-Climate/GrIML/blob/main/docs/figures/iml_time_series_plot.png?raw=true" alt="Time-series plot example" width="800" align="aligncenter" />
