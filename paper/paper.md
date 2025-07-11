---
title: "GrIML: A Python package for investigating Greenland's ice-marginal lakes under a changing climate"
tags:
  - python
  - glaciology
  - remote sensing
  - greenland
  - kalaallit nunaat
authors:
  - name: Penelope R. How
    orcid: 0000-0002-8088-8497
    corresponding: true
    affiliation: 1
affiliations:
 - name: Department of Glaciology and Climate, Geological Survey of Denmark and Greenland (GEUS), Nuuk, Greenland
   index: 1

date: 15 January 2025
bibliography: paper.bib

---


# Summary

The `GrIML` Python package is for processing classified water bodies from satellite imagery, and compiling classifications into a standardised inventory. It has been used to produce the Greenland ice-marginal lake inventory series, which maps the presence and extent of water bodies across Greenland that share a margin with the Greenland Ice Sheet and/or the surrounding ice caps and periphery glaciers since 2016 [@How2025a]. 

![An overview of the GrIML Python package workflow for generating ice-marginal lake inventories. The boxes refer to the four main modules and processing stages (reading from left to right), the coloured circles represent intermediary results to each processing stage, and the grey circles represent additional inputs. \label{fig:workflow}](https://github.com/GEUS-Glaciology-and-Climate/GrIML/blob/main/docs/figures/griml_workflow_without_gee.png?raw=true){ width=95% height=95% }


Initial rasterised binary classifications denoting water bodies can be inputted to `GrIML` to convert, filter, and merge into a unified ice-marginal lake vector dataset, populated with useful metadata and analysed with relevant statistical information (\autoref{fig:workflow}). The workflow to produce the rasterised binary classifications is provided with the `GrIML` [Github repository](https://github.com/GEUS-Glaciology-and-Climate/GrIML/tree/main/gee_scripts) as both Javascript and Python scripts, which are run with Google Earth Engine.

# Statement of need

`GrIML` meets four main needs of users in the remote sensing and cryospheric science communities:

1. Provide a usable workflow for processing rasterised water body classifications
2. Document the criteria for classifying an ice-marginal lake
3. Showcase a transparent workflow that, in turn, produces an open and reproducible ice-marginal lake dataset that adheres to the FAIR principles [@Wilkinson2016]
4. Produce inventories that map the areal extent and abundance of ice-marginal lakes across Greenland, which demonstrate ice-marginal lake evolution under a changing climate

There have been many different approaches to classifying ice-marginal lakes with remote sensing techniques [@How2021;@Chen2021;@Andreassen2022;@Rick2022;@Wieczorek2023;@Domgaard2024]. Packages exist for handling satellite and spatial data, such as GrIML's two key dependencies, Geopandas [@Geopandas2024] and Rasterio [@Gillies2019], as well as others such as SentinelHub [@Sentinelhub2024] and Google Earth Engine [@Gorelick2017]. Remote sensing object classification and post-processing routines are usually available in connection with scientific publications, however, few are available as open, deployable packages. The `GrIML` Python package addresses this gap, for the benefit of the future generation of ice-marginal lake inventories and for others in the scientific community to adapt and use themselves. 

The 2016-2023 Greenland ice-marginal lake inventory series was produced with the `GrIML` Python package to address knowledge gaps regarding sea level contribution, and provide an overview of regions where lacustrine ice loss and processes are prominent [@How2025a;@How2025b]. The dataset consists of a series of annual inventories, mapping the presence and extent of ice-contact lakes across Greenland (\autoref{fig:inventory}). The annual inventory series spans the entirety of Greenland, including all terrestrial regions. Thus far, there are 8 annual inventories, covering 2016 to 2023, with one inventory for each year. The `GrIML` package will continue to be used to produce future additions to the Greenland ice-marginal lake inventory series; in which case a standardised and version-controlled processing pipeline is essential [@How2025a].

![An overview of the Greenland ice-marginal lake inventory series, which maps the number of lakes and their size between the years of 2016 and 2023 [@How2025a]. The map shows the location of each lake, with the symbol signifying area change over time, where green circles represent an increase in lake area, yellow squares represent a decrease in lake area, and white triangles represent an unchanged lake area. Crosshair points denote lakes where no area information is provided. The bar graphs show the change in number of lakes in each region. Base maps are provided by @Moon2023 and region outlines are as defined by @Mouginot2019. \label{fig:inventory}](https://github.com/GEUS-Glaciology-and-Climate/GrIML/blob/main/docs/figures/iml_dataset_overview.png?raw=true){ width=75% height=75% }


# Overview of package contents

`GrIML` has 4 main modules for processing from raster classifications to a vectorised inventory:

1. `Convert`: for converting binary raster classifications of water bodies to vectors
2. `Filter`: for filtering vectors by size and proximity to an object (i.e. an ice margin profile)
3. `Merge`: for merging vector classifications into one unified object (for example, when classifications cover a large area that needs to be split over multiple files)
4. `Metadata`: for populating vector classifications with various pieces of information, including identification number, placename, region, classification source, and certainty.

These 4 modules represent the 4 processing steps that should be executed in order to produce a standardised ice-marginal lake inventory. Each module contains the functions associated with each step (see \autoref{fig:structure}).

![The GrIML Python package structure, including modules (blue), key module functions (orange), classes (green) and dependencies (yellow). Arrows between modules represent module dependencies, where the direction of the arrow indicates the dependency source (at the end of the arrow) and target (at the head of the arrow). \label{fig:structure}](https://github.com/GEUS-Glaciology-and-Climate/GrIML/blob/main/docs/figures/griml_package_structure.png?raw=true){ width=75% height=75% }


# Usage
## Installation

The `GrIML` Python package is compatible with Python 3.10, 3.11, and 3.12, and can be installed using pip:

```
$ pip install griml
```

Full installation instructions are provided at [https://griml.readthedocs.io/en/stable/installation.html](https://griml.readthedocs.io/en/stable/installation.html).


## Tutorials and guides

Two sets of tutorials are provided with `GrIML` for: 
1) Using the processing pipeline ([https://griml.readthedocs.io/en/stable/tutorials/process_with_test_data.html](https://griml.readthedocs.io/en/stable/tutorials/process_with_test_data.html))
2) Handling the produced dataset ([https://griml.readthedocs.io/en/stable/tutorials/dataset_tutorial.html](https://griml.readthedocs.io/en/stable/tutorials-data.html))
3) Inputting custom datasets ([https://griml.readthedocs.io/en/stable/tutorials/using_custom_input_data.html](https://griml.readthedocs.io/en/stable/tutorials/using_custom_input_data.html))

The processing and custom input data tutorials guide the user through each processing step from the initial raster classifications to a fully compiled ice-marginal lake dataset. The dataset tutorials provide an overview for how to handle and analyse an ice-marginal lake inventory produced with `GrIML`. This includes examples using the ice-marginal lakes dataset on the GEUS Dataverse [@How2025a], primarily handled with Geopandas [@Geopandas2024] to create spatial plots and time-series (see \autoref{fig:tutorial}).

![An example plot output from the dataset tutorial, where the change in the number of lakes across the ice-marginal lake inventory series is visualised. Each bar represents the number of lakes in one inventory year, with each coloured stage indicating the number of lakes for a given region. \label{fig:tutorial}](https://github.com/GEUS-Glaciology-and-Climate/GrIML/blob/main/docs/figures/iml_time_series_plot.png?raw=true)


## Usage terms and conditions

If the `GrIML` package or the Greenland ice marginal lake inventory series are used to support results of any kind then we ask the authors to include references to the applicable publications:

- How, P. et al. (2025) *“Greenland Ice Marginal Lake Inventory annual time-series Edition 1”.* **GEUS Dataverse.** [https://doi.org/10.22008/FK2/MBKW9N](https://doi.org/10.22008/FK2/MBKW9N)
- How, P. et al. (In Review) *“The Greenland Ice-Marginal Lake Inventory Series from 2016 to 2023”.* **Earth System Science Data. Discuss**[https://doi.org/10.5194/essd-2025-18](https://doi.org/10.5194/essd-2025-18)
- How, P. et al. (2021) *“Greenland-wide inventory of ice marginal lakes using a multi-method approach”*. **Scientific Reports** 11, 4481. [https://doi.org/10.1038/s41598-021-83509-1](https://doi.org/10.1038/s41598-021-83509-1)

And include the following statement in the acknowledgements:

*“Ice marginal lake data provided by the European Space Agency (ESA), and the Programme for Monitoring of the Greenland Ice Sheet (PROMICE) at the Geological Survey of Denmark and Greenland (GEUS) [https://doi.org/10.22008/FK2/MBKW9N](https://doi.org/10.22008/FK2/MBKW9N).”*


# Acknowledgements

This work is funded by the ESA Living Planet Fellowship (4000136382/21/I-DT-lr) entitled "Examining Greenland's Ice Marginal Lakes under a Changing Climate". Further support was provided by [PROMICE (Programme for Monitoring of the Greenland Ice Sheet) and GC-Net (Greenland Climate Network)](https://promice.org), which is funded by the Geological Survey of Denmark and Greenland (GEUS) within the Danish Ministry of Climate, Energy and Utilities. The Danish Finance Law currently supports GEUS for the continuation of PROMICE and GC-Net field and data activities. PROMICE and GC-Net are conducted in collaboration with DTU Space (Technical University of Denmark) and ASIAQ Greenland Survey.



# References

