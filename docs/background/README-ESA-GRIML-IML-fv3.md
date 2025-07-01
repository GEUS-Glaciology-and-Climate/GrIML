# Greenland Ice-Marginal Lake Inventory annual time-series Edition 1

Data available at [GEUS Dataverse](https://doi.org/10.22008/FK2/MBKW9N).

Contact [pho@geus.dk](mailto:pho@geus.dk).

## Table of contents

- [Terms of use](#terms-of-use)
- [Dataset Contents](#dataset-contents)
	+ [Data format](#data-format)
	+ [Metadata](#metadata)
- [Acknowledgements](#acknowledgements)
- [Relevant links](#relevant-links)

## Terms of use

If the data are presented or used to support results of any kind, please include references to the applicable publications:

- *How, P. et al. (2025) "Greenland Ice-Marginal Lake Inventory annual time-series Edition 1". GEUS Dataverse. [https://doi.org/10.22008/FK2/MBKW9N](https://doi.org/10.22008/FK2/MBKW9N)*
- *How, P. et al. (2021) "Greenland-wide inventory of ice marginal lakes using a multi-method approach". Sci. Rep. 11, 4481. [https://doi.org/10.1038/s41598-021-83509-1](https://doi.org/10.1038/s41598-021-83509-1)*
- *How, P. et al. (In Review) "Greenland ice-marginal lake inventory series from 2016 to 2023". Earth Syst. Sci. Data Discuss. [https://doi.org/10.5194/essd-2025-18](https://doi.org/10.5194/essd-2025-18)*
- *How, P. (In Review) "GrIML: A Python package for investigating Greenland's ice-marginal lakes under a changing climate". J. Open Source Software. [https://joss.theoj.org/papers/a2e10775df44b89f26b0ac9dbf8bc9e3](https://joss.theoj.org/papers/a2e10775df44b89f26b0ac9dbf8bc9e3)*

And include the following statement in the acknowledgements:

*"Ice-marginal lake data provided by the European Space Agency (ESA) and the Programme for Monitoring of the Greenland Ice Sheet (PROMICE) at the Geological Survey of Denmark and Greenland (GEUS) ([https://doi.org/10.22008/FK2/MBKW9N](https://doi.org/10.22008/FK2/MBKW9N))."*

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

## Acknowledgements

The inventory series of ice-marginal lakes in Greenland has been produced as part of the European Space Agency (ESA) Living Planet Fellowship project "Examining GReenland’s Ice Marginal Lakes under a changing climate (GrIML)", which is a follow-on effort to the 2017 inventory of ice-marginal lakes created under the European Space Agency (ESA) Climate Change Initiative (CCI) in Option 6 of the Glaciers_cci project (4000109873/14/I-NB). 

Upkeep and continuation of the inventory series is supported by PROMICE, funded by the Geological Survey of Denmark and Greenland (GEUS) and the Danish Ministry of Climate, Energy and Utilities, conducted in collaboration with DTU Space (Technical University of Denmark) and Asiaq Greenland Survey.

## Relevant links

- The GrIML code repository on [Github](https://github.com/GEUS-Glaciology-and-Climate/GrIML) and the code readme on [readthedocs](https://griml.readthedocs.io)
- The ESA GrIML [project outline](https://eo4society.esa.int/projects/griml/) and [fellow information](https://eo4society.esa.int/lpf/penelope-how/)
- Information about the [ESA Living Planet Fellowship](https://eo4society.esa.int/communities/scientists/living-planet-fellowship/)
- The GrIML [project description](https://pennyhow.github.io/blog/investigating-griml/)
- The original 2017 ice-marginal lake inventory [Scientific Reports paper](https://www.nature.com/articles/s41598-021-83509-1) and [dataset](https://catalogue.ceda.ac.uk/uuid/7ea7540135f441369716ef867d217519)
- The [MEaSUREs GIMP ice mask](https://nsidc.org/data/NSIDC-0714/versions/1) and associated publications, [Howat (2017)](https://doi.org/10.5067/B8X58MQBFUPA) and [Howat, Negrete and Smith (2014)](https://doi.org/10.5194/tc-8-1509-2014)
- The [Oqaasileriffik placename database](https://asiaq.maps.arcgis.com/apps/View/index.html?appid=c5c7d9d52a264980a24911d7d33914b5)
- QGreenland v3.0.0 dataset reference, [Moon et al. (2023)](https://doi.org/10.5281/zenodo.12823307)
