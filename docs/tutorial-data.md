# Dataset tutorials

The GrIML package is used for the production of the Greenland ice marginal lake inventory series, which is freely available through the [GEUS Dataverse](https://doi.org/10.22008/FK2/MBKW9N). This dataset is a series of annual inventories, mapping the extent and presence of lakes across Greenland that share a margin with the Greenland Ice Sheet and/or the surrounding ice caps and periphery glaciers. 

Here, we will look at how to load and handle the dataset, and provide details on its contents.

## Dataset contents

This ice marginal lake dataset is a series of annual inventories, mapping the extent and presence of lakes across Greenland that share a margin with the Greenland Ice Sheet and/or the surrounding ice caps and periphery glaciers. The annual inventories provide a comprehensive record of all identified ice marginal lakes, which have been detected using three independent remote sensing techniques:

- DEM sink detection using the ArcticDEM (mosaic version 3)
- SAR backscatter classification from Sentinel-1 imagery
- Multi-spectral indices classification from Sentinel-2 imagery

All data were compiled and filtered in a semi-automated approach, using a modified version of the [MEaSUREs GIMP ice mask](https://nsidc.org/data/NSIDC-0714/versions/1) to clip the dataset to within 1 km of the ice margin. Each detected lake was then verified manually. The methodology is open-source and provided in the associated [Github repository](https://github.com/GEUS-Glaciology-and-Climate/GrIML) for full reproducibility.

The inventory series was created to better understand the impact of ice marginal lake change on the future sea level budget and the terrestrial and marine landscapes of Greenland, such as its ecosystems and human activities. The dataset is a complete inventory series of Greenland, with no absent data.

### Data format

The detected lakes are presented as polygon vector features in shapefile format (.shp), with coordinates provided in the WGS NSIDC Sea Ice Polar Stereographic North (EPSG:3413) projected coordinate system.

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
| `temp_aver`	| Average lake surface temperature estimate (in degrees Celsius), derived from the Landsat 8/9 OLI/TIRS Collection 2 Level 2 surface temperature data product  | Float |
| `temp_min`	| Minimum pixel lake surface temperature estimate (in degrees Celsius), derived from the Landsat 8/9 OLI/TIRS Collection 2 Level 2 surface temperature data product  | Float |
| `temp_max`	| Maximum pixel lake surface temperature estimate (in degrees Celsius), derived from the Landsat 8/9 OLI/TIRS Collection 2 Level 2 surface temperature data product  | Float |
| `temp_stdev`	| Average lake surface temperature estimate standard deviation, derived from the Landsat 8/9 OLI/TIRS Collection 2 Level 2 surface temperature data product  | Float |
| `method`		| Method of classification (`DEM`, `SAR`, `VIS`)  | String |
| `source`     | Image source of classification (`ARCTICDEM`, `S1`, `S2`)    | String  |
| `all_src`     | List of all sources that successfully classified the lake (i.e. all classifications with the same `lake_name` value)  | String         |
| `num_src`          | Number of sources that successfully classified the lake (`1`, `2`, `3`)     | String | 
| `certainty`     | Certainty of classification, which is calculated from `all_src` as a score between `0` and `1`          | Float | -                             |
| `start_date` | Start date for classification image filtering 	| String  |
| `end_date` 	| End date for classification image filtering     | String |
| `verified` | Flag to denote if the lake has been manually verified (`Yes`, `No`)   | String |
| `verif_by`  | Author of verification | String  |
| `edited`  | Flag to denote if polygon has been manually edited (`Yes`, `No`)  | String   |
| `edited_by` | Author of manual editing   | String  |

## Getting started

Loading the dataset: Data available at [GEUS Dataverse](https://doi.org/10.22008/FK2/MBKW9N).

Quicklook plotting of the dataset


## Generating statistics

Extracting statistics
