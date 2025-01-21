# Datasets used for the GrIML Greenland ice-marginal lake inventory series generation

## Area of Interest (AOI) masks

These files are polygons and grids representing the AOI around the ice margins and terrestrial regions of Greenland. These are used for satellite scene filtering in the initial raster classification of water bodies. The files have been created manually.

## Drainage basins

The drainage basins are the catchment regions of the Greenland Ice Sheet which are used for defining the regional locations of ice-marginal lakes. The basins are from [Mouginot and Rignot (2019)](https://doi.org/10.7280/D1WT11), as used in [Howat, Negrete and Smith (2014)](https://doi.org/10.5194/tc-8-1509-2014) as part of the [Greenland Ice Mapping Project (GIMP)](https://nsidc.org/grimp). The drainage basins have been reprojected into a polar stereographic projection (i.e. the working projection of the ice-marginal lake inventory series). 

## Ice margin

The ice margin mask is used to filter out water bodies disconnected from the ice margins around Greenland. The line mask file is provided, along with the polygon mask file which is computed with a 1 km buffer around the line mask. The ice margin mask is from the GIMP 15 m ice mask, which has been projected into a polar stereographic projection ([Howat, 2017](https://doi.org/10.5067/B8X58MQBFUPA)), as used in [Howat, Negrete and Smith (2014)](https://doi.org/10.5194/tc-8-1509-2014).

## Placenames

Lake names are assigned to each classified ice-marginal lake in instances where a name is available, with preference to West Greenlandic (Kalaallisut) placenames followed by Old Greenlandic and alternative foreign placenames. Placenames are provided by [Oqaasileriffik (the Language Secretariat of Greenland)](https://oqaasileriffik.gl/) placename database ([https://nunataqqi.gl/](https://nunataqqi.gl/)), which is distributed with [QGreenland v3.0](https://qgreenland.org/) ([Moon et al., 2023](https://doi.org/10.5281/zenodo.12823307)). Here, the dataset has been reprojected into a polar stereographic projection.
