# Greenland Ice-Marginal Lake Inventory annual time-series Edition 1

Data available at [GEUS Dataverse](https://doi.org/10.22008/FK2/MBKW9N).

Contact [pho@geus.dk](mailto:pho@geus.dk).

## Table of contents

- [Dataset Contents](#dataset-contents)
	+ [Data format](#data-format)
	+ [Metadata](#metadata)
- [Terms of use](#terms-of-use)
- [Acknowledgements](#acknowledgements)
- [Relevant links](#relevant-links)

## Dataset contents

This ice-marginal lake dataset is a series of annual inventories, mapping the extent and presence of lakes across Greenland that share a margin with the Greenland Ice Sheet and/or the surrounding ice caps and periphery glaciers. Specifically, the following files are included in this dataset:

- *ALL-ESA-GRIML-IML-\<version\>.gpkg*: The overview dataset of all ice-marginal lakes across the inventory series, where one polygon vector features signifies one lake
- *\<YYYYMMDD\>-ESA-GRIML-IML-\<version\>.gpkg*: Automatic classifications of ice-marginal lakes for a specific year, provided as polygon vector features
- *README-ESA-GRIML-IML-\<version\>.gpkg*: This dataset readme file

**We recommend looking at the overview dataset (*ALL-ESA-GRIML-IML-\<version\>.gpkg*) first**, as this consists of all automatic classifications and other collected outlines which have been curated to provide the most complete dataset. Data sources for these outlines comprise of:

1. SAR backscatter automatic classification from Sentinel-1 imagery
2. Multi-spectral indices automatic classification from Sentinel-2 imagery
3. DEM sink detection using the ArcticDEM (mosaic version 4)
4. Digitised outlines from the [Åbent Land Grønland (Open Country Greenland) vector dataset](https://dataforsyningen.dk/data/4771) (2024, version 3.1) provided by Klimadatastyrelsen (Danish Climate Data Agency)

The annual inventory files (*\<YYYYMMDD\>-ESA-GRIML-IML-\<version\>.gpkg*) provide a comprehensive record of all automatically classified ice-marginal lakes for each year, which have been detected using the SAR backscatter and the multi-spectral indices classification methods outlined previously.

All data were compiled and filtered in a semi-automated approach. Data was filtered to within 1 km of the ice margin using a mask provided as part of [Klimadatastyrelsen Åbent Land Grønland vector dataset](https://dataforsyningen.dk/data/4771). Each detected lake was then verified manually. The methodology is open-source and provided in the associated [Github repository](https://github.com/GEUS-Glaciology-and-Climate/GrIML) for full reproducibility.

The inventory series was created to better understand the impact of ice-marginal lake change on the future sea level budget and the terrestrial and marine landscapes of Greenland, such as its ecosystems and human activities. The dataset is a complete inventory series of Greenland, with no absent data.

### Data format

The detected lakes are presented as polygon vector features in GeoPackage format (.gpkg), with coordinates provided in the WGS NSIDC Sea Ice Polar Stereographic North (EPSG:3413) projected coordinate system.

### Metadata

The overview dataset file (*ALL-ESA-GRIML-IML-\<version\>.gpkg*) contains the following metadata information:

| Variable name       | Description         | Format | 
|---------------------|---------------------|---------|
| `row_id`  	| Index identifying number for each polygon   | Integer  |
| `lake_id` 	| Identifying number for each unique lake  	| Integer  |
| `lake_name`| Lake placename, as defined by the [Oqaasileriffik (Language Secretariat of Greenland)](https://oqaasileriffik.gl) placename database which is distributed with [QGreenland](https://qgreenland.org/)  | String   |
| `margin`	| Type of margin that the lake is adjacent to (`ICE_SHEET`, `ICE_CAP`)   | String |
| `region`	| Region that lake is located, as defined by [Mouginot and Rignot (2019)](https://doi.org/10.7280/D1WT11) (`NW`, `NO`, `NE`, `CE`, `SE`, `SW`, `CW`)       	| String |
| `area_all`	| Areal extent from all classifications, in square kilometres  | Float |
| `area_<year>`	| Areal extent from automatic classifications for each year (`area_2016`, `area_2017`, `area_2018`...), in square kilometres  | Float |
| `attached_up_to`	| Year that lake was attached up until  | String |
| `length_km`	| Length of polygon/s in kilometres         		| Float |
| `centroid`	| Centroid position (x,y) of lake, based on all classifications throughout the inventory series. Coordinates are provided in the WGS NSIDC Sea Ice Polar Stereographic North (EPSG:3413) projected coordinate system | String |
| `glof_lake`	| Flag to signify whether the lake is a known GLOF (Glacial Lake Outburst Flood) lake, where `Yes` signifies it is a known GLOF lake and `No` signifies that it has not been known as a GLOF lake. GLOF information is provided by [Dømgaard et al. (2024)](https://doi.org/10.22008/FK2/K1CM4K) | String |
| `drain_yrs`	| List of years of known GLOF events, provided if `glof_lake == yes`. GLOF information is provided by [Dømgaard et al. (2024)](https://doi.org/10.22008/FK2/K1CM4K) | String |
| `t_aver_<year>`	| Average lake surface temperature estimate (in degrees Celsius) for each year (`t_aver_2016`, `t_aver_2017`, `t_aver_2018`...), derived from the Landsat 8/9 OLI/TIRS Collection 2 Level 2 surface temperature data product  | Float |
| `t_max_<year>`	| Maximum pixel lake surface temperature estimate (in degrees Celsius) for each year, derived from the Landsat 8/9 OLI/TIRS Collection 2 Level 2 surface temperature data product  | Float |
| `t_min_<year>`	| Minimum pixel lake surface temperature estimate (in degrees Celsius) for each year, derived from the Landsat 8/9 OLI/TIRS Collection 2 Level 2 surface temperature data product  | Float |
| `t_stdev_<year>`	| Average lake surface temperature estimate standard deviation for each year, derived from the Landsat 8/9 OLI/TIRS Collection 2 Level 2 surface temperature data product  | Float |
| `t_count_<year>`	| Number of Landsat 8/9 OLI/TIRS Collection 2 Level 2 scenes that lake surface temperature information were derived from. Scenes are only selected from the month of August for each inventory year  | Integer |
| `t_date_<year>`	| Datetime of all Landsat 8/9 OLI/TIRS Collection 2 Level 2 scene acquisitions that lake surface temperature information are derived from for each inventory year  | String |
| `start_date` | Start date for classification image filtering 	| String  |
| `end_date` 	| End date for classification image filtering     | String |
| `method`		| Method of classification (`Automatic`, `DEM sink detection`, `Digitisation`)  | String |
| `source`     | Image source of classification (`Sentinel-1, Sentinel-2`, `ArcticDEM (v4)`, `Klimadatastyrelsen Open Land Greenland vector dataset (v3.1)`)    | String  |
| `verified` | Flag to denote if the lake has been manually verified (`Yes`, `No`)   | String |
| `verif_by`  | Author of verification | String  |
| `edited`  | Flag to denote if polygon has been manually edited (`Yes`, `No`)  | String   |
| `edited_by` | Author of manual editing   | String  |


Dataset files containing annual automatic classifications (*\<YYYYMMDD\>-ESA-GRIML-IML-\<version\>.gpkg*) contain the following metadata information:

| Variable name       | Description         | Format | 
|---------------------|---------------------|---------|
| `row_id`  	| Index identifying number for each polygon   | Integer  |
| `lake_id` 	| Identifying number for each unique lake  	| Integer  |
| `lake_name`| Lake placename, as defined by the [Oqaasileriffik (Language Secretariat of Greenland)](https://oqaasileriffik.gl) placename database which is distributed with [QGreenland](https://qgreenland.org/)  | String   |
| `margin`	| Type of margin that the lake is adjacent to (`ICE_SHEET`, `ICE_CAP`)   | String |
| `region`	| Region that lake is located, as defined by [Mouginot and Rignot (2019)](https://doi.org/10.7280/D1WT11) (`NW`, `NO`, `NE`, `CE`, `SE`, `SW`, `CW`)       	| String |
| `area_sqkm`	| Areal extent of polygon/s in square kilometres  | Float |
| `length_km`	| Length of polygon/s in kilometres         		| Float |
| `t_aver`	| Average lake surface temperature estimate (in degrees Celsius), derived from the Landsat 8/9 OLI/TIRS Collection 2 Level 2 surface temperature data product  | Float |
| `t_min`	| Minimum pixel lake surface temperature estimate (in degrees Celsius), derived from the Landsat 8/9 OLI/TIRS Collection 2 Level 2 surface temperature data product  | Float |
| `t_max`	| Maximum pixel lake surface temperature estimate (in degrees Celsius), derived from the Landsat 8/9 OLI/TIRS Collection 2 Level 2 surface temperature data product  | Float |
| `t_stdev`	| Average lake surface temperature estimate standard deviation, derived from the Landsat 8/9 OLI/TIRS Collection 2 Level 2 surface temperature data product  | Float |
| `t_count`	| Number of Landsat 8/9 OLI/TIRS Collection 2 Level 2 scenes that lake surface temperature information were derived from. Scenes are only selected from the month of August  | Integer |
| `t_date`	| Datetime of all Landsat 8/9 OLI/TIRS Collection 2 Level 2 scene acquisitions that lake surface temperature information are derived from  | String |
| `method`		| Method of classification (`SAR`, `VIS`)  | String |
| `source`     | Image source of classification (`S1`, `S2`)    | String  |
| `num_src`          | Number of automatic classification methods that successfully classified the lake (`1`, `2`)     | Integer |
| `start_date` | Start date for classification image filtering 	| String  |
| `end_date` 	| End date for classification image filtering     | String |
| `verified` | Flag to denote if the lake has been manually verified (`Yes`, `No`)   | String |
| `verif_by`  | Author of verification | String  |
| `edited`  | Flag to denote if polygon has been manually edited (`Yes`, `No`)  | String   |
| `edited_by` | Author of manual editing   | String  |

## Terms of use

If the data are presented or used to support results of any kind, please include references to the applicable publications:

- *How, P. et al. (2025) The Greenland Ice-Marginal Lake Inventory Series from 2016 to 2023, Earth Syst. Sci. Data, 17, 6331–6351, [doi:10.5194/essd-17-6331-2025](https://doi.org/10.5194/essd-17-6331-2025)*
- *How, P. et al. (2025) "Greenland Ice-Marginal Lake Inventory annual time-series Edition 1". GEUS Dataverse. [doi:10.22008/FK2/MBKW9N](https://doi.org/10.22008/FK2/MBKW9N)*
- *How, P. (2025). "GrIML: A Python package for investigating Greenland's ice-marginal lakes under a changing climate". J. Open Source Software 10(111), 7927, [doi:10.21105/joss.07927](https://doi.org/10.21105/joss.07927)*
- *How, P. et al. (2021) "Greenland-wide inventory of ice marginal lakes using a multi-method approach". Sci. Rep. 11, 4481. [doi:10.1038/s41598-021-83509-1](https://doi.org/10.1038/s41598-021-83509-1)*

And include the following statement in the acknowledgements:

*"Ice-marginal lake data provided by the European Space Agency (ESA) and the Programme for Monitoring of the Greenland Ice Sheet (PROMICE) at the Geological Survey of Denmark and Greenland (GEUS) ([https://doi.org/10.22008/FK2/MBKW9N](https://doi.org/10.22008/FK2/MBKW9N))."*

## Acknowledgements

The inventory series of ice-marginal lakes in Greenland has been produced as part of the European Space Agency (ESA) Living Planet Fellowship project "Examining GReenland’s Ice Marginal Lakes under a changing climate (GrIML)", which is a follow-on effort to the 2017 inventory of ice-marginal lakes created under the European Space Agency (ESA) Climate Change Initiative (CCI) in Option 6 of the Glaciers_cci project (4000109873/14/I-NB). 

Upkeep and continuation of the inventory series is supported by PROMICE, funded by the Geological Survey of Denmark and Greenland (GEUS) and the Danish Ministry of Climate, Energy and Utilities, conducted in collaboration with DTU Space (Technical University of Denmark) and Asiaq Greenland Survey.

## Relevant links

- The GrIML code repository on [Github](https://github.com/GEUS-Glaciology-and-Climate/GrIML) and the code readme on [readthedocs](https://griml.readthedocs.io)
- The ESA GrIML [project outline](https://eo4society.esa.int/projects/griml/) and [fellow information](https://eo4society.esa.int/lpf/penelope-how/)
- Information about the [ESA Living Planet Fellowship](https://eo4society.esa.int/communities/scientists/living-planet-fellowship/)
- The GrIML [project description](https://pennyhow.github.io/blog/investigating-griml/)
- The original 2017 ice-marginal lake inventory [Scientific Reports paper](https://www.nature.com/articles/s41598-021-83509-1) and [dataset](https://catalogue.ceda.ac.uk/uuid/7ea7540135f441369716ef867d217519)
- The Danish Climate Agency Open Country Greenland vector dataset ([Klimatdatastyrelsen Åbent Land Grønland vektordata](https://dataforsyningen.dk/data/4771))
- GLOF lake water level changes from [Dømgaard et al. (2024)](https://doi.org/10.1038/s43247-024-01522-4) and the [dataset](https://doi.org/10.22008/FK2/K1CM4K)
- Greenland Ice Sheet catchments/basins dataset from [Mouginot and Rignot (2019)](https://doi.org/10.7280/D1WT11)
- The [Oqaasileriffik placename database](https://asiaq.maps.arcgis.com/apps/View/index.html?appid=c5c7d9d52a264980a24911d7d33914b5)
- QGreenland v3.0.0 dataset reference, [Moon et al. (2023)](https://doi.org/10.5281/zenodo.12823307)
