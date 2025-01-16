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

The `GrIML` Python package is for processing classified water bodies from satellite imagery, and compiling classifications into a standardised inventory. It has been used to produce the Greenland ice-marginal lake inventory series, which maps the presence and extents of water bodies across Greenland that share a margin with the Greenland Ice Sheet and/or the surrounding ice caps and periphery glaciers since 2016 [@How2025a] (\autoref{fig:inventory}). 

![An overview of the Greenland ice-marginal lake inventory series, which maps the number of lakes and their size between the years of 2016 and 2023 [@how_data_2025]. The map shows the location of each lake, with the symbol signifying area change over time, where green circles represent an increase in lake area and yellow squares represent a decrease in lake area. The bar graphs show change in the number of lakes over each region   \label{fig:inventory}](https://github.com/PennyHow/GrIML/blob/main/other/reporting/figures/iml_dataset_overview.png?raw=true)

Initial rasterised binary classifications denoting water bodies can be inputted to `GrIML` to convert, filter and merge into a cohesive ice-marginal lake vector dataset, populated with useful metadata and analysed with relevant statistical information (\autoref{fig:workflow}).

![An overview of the GrIML Python package workflow \label{fig:workflow}](https://github.com/PennyHow/GrIML/blob/main/other/reporting/figures/griml_workflow_without_gee.png?raw=true)


# Statement of need

`GrIML` meets four main needs to users in the remote sensing and cryospheric science communities:

1. Provide a usable workflow for processing rasterised water body classifications
2. Document the criteria for classifying an ice-marginal lake
3. Showcase a transparent workflow that, in turn, produces an open and reproducible ice-marginal lake dataset that adheres to the FAIR principles [@Wilkinson2016]
4. Produce inventories that map the areal extent and abundance of ice-marginal lakes across Greenland, which demonstrate ice-marginal lake evolution under a changing climate

There have been many different approaches to classifying ice-marginal lakes with remote sensing techniques [@Carrivick2014;@Shugar2020;@Andreassen2022;@Rick2022;@How2021;@Domgaard2024]. Packages exist for handling satellite and spatial data, such as GrIML's two key dependencies, Geopandas [@Kelsey2020] and Rasterio [@Gillies2019], as well as others such as SentinelHub [@Sentinelhub2024] and Google Earth Engine [@Gorelick2017]. Remote sensing object classification and post-processing routines are usually available in connection with scientific publications, however, few are available as open, deployable packages. The `GrIML` post-processing Python package addresses this gap, for the benefit of the future generation of ice-marginal lake inventories and for others in the scientific community to adapt and use themselves. For example, it is intended to continue using the `GrIML` package for the production of future additions to the Greenland ice-marginal lake inventory series; in which case a standardised and version-controlled processing pipeline is essential [@How2025a].


## Scientific background and context

The Greenland Ice Sheet and its peripheral glaciers and ice caps (PGICs) are anticipated to be the largest contributors to sea level rise during the 21st century [@AMAP2021]. While projections typically assume meltwater flows directly to the ocean, a significant portion is temporarily stored in ice-marginal lakes along the ice sheet's edges and near PGICs. These lakes form where meltwater is trapped at glacier termini, often exhibiting dynamic behaviours such as sudden drainage events that lead to Glacial Lake Outburst Floods (GLOFs) [@Carrivick2019]. Such events can affect glacier dynamics, sedimentation, and downstream ecosystems [@Grinsted2017;@Kjeldsen2017]. Ice-marginal lakes also drive thermo-mechanical processes, including lacustrine melting and calving, which accelerate ice mass loss [@Sutherland2020]. As glaciers retreat under warming conditions, these lakes are expected to increase in size and prevalence, amplifying proglacial melt rates and GLOF occurrences [@Carrivick2016;@Shugar2020].

The 2016-2023 Greenland ice-marginal lake inventory series was produced as part of the [ESA GrIML project](https://eo4society.esa.int/projects/griml/) (Investigating Greenland's ice-marginal lakes under a changing climate) to address knowledge gaps regarding sea level contribution, and provide an overview of regions where lacustrine ice loss and processes are prominent [@How2025a;@How2025b]. The dataset consists of a series of annual inventories, mapping the presence and extent of ice-contact lakes across Greenland. The annual inventory series spans the entirety of Greenland, including all terrestrial regions. Thus far, there are 8 annual inventories, covering 2016 to 2023, where one inventory represents one year. The dataset is fully documented and described at [@How2025b].


# Overview of Package contents

`GrIML` has 4 main modules for processing from raster classifications to a vectorised inventory:

1. `Convert`: for converting binary raster classifications of water bodies to vectors
2. `Filter`: for filtering vectors by size and proximity to an object (i.e. an ice margin profile)
3. `Merge`: for merging vector classifications into one unified object (for example, when classifications cover a large area that needs to be split over multiple files)
4. `Metadata`: for populating vector classifications with various pieces of information, including identification number, placename, region, classification source and certainty.

These 4 modules represent the 4 processing steps that should be executed in order to produce a standardised ice-marginal lake inventory. Each module contains the functions associated with each step (\autoref{fig:structure}).

![The GrIML Python package structure \label{fig:structure}](https://github.com/PennyHow/GrIML/blob/main/other/reporting/figures/griml_package_structure.png?raw=true)


# Usage
## Installation

The GrIML Python package is compatible with Python 3.10, 3.11 and 3.12, and can be installed using pip:

```
$ pip install griml
```

To install as a developer, a conda environment file is provided that includes all of GrIML's dependencies for a straightforward install:

```
$ git clone git@github.com:GEUS-Glaciology-and-Climate/GrIML.git
$ cd GrIML
$ conda env create --file environment.yml
$ conda activate griml
$ pip install .
```

Full installation instructions are provided at [https://griml.readthedocs.io/en/latest/installation.html](https://griml.readthedocs.io/en/latest/installation.html).


## Tutorials and guides

Two sets of tutorials are provided with `GrIML` for 1) using the processing pipeline ([https://griml.readthedocs.io/en/latest/tutorials-processing.html](https://griml.readthedocs.io/en/latest/tutorials-processing.html)); and 2) handling the produced dataset ([https://griml.readthedocs.io/en/latest/tutorials-data.html](https://griml.readthedocs.io/en/latest/tutorials-data.html)). The processing tutorials guide the user through each processing step from the initial raster classifications to a fully compiled ice-marginal lake dataset. The dataset tutorials provide an overview for how to handle and analyse an ice-marginal lake inventory produced with `GrIML`. This includes examples using the ice-marginal lakes dataset on the GEUS Dataverse [@How2025a], primarily handled with Geopandas [@Kelsey2020] to create spatial plots and time-series (\autoref{fig:tutorial}).

![An example plot output from the dataset tutorial, where the change in the number of lakes across the ice-marginal lake inventory series is visualised. Each bar represents the number of lakes in one inventory year, with each coloured stage indicating the number of lakes for a given region \label{fig:tutorial}](https://github.com/GEUS-Glaciology-and-Climate/GrIML/blob/main/docs/figures/iml_time_series_plot.png?raw=true)


## Usage terms and conditions

If the GrIML package or the Greenland ice marginal lake inventory series are used to support results of any kind then we ask the authors to include references to the applicable publications:

- How, P. et al. (2025) *“Greenland Ice Marginal Lake Inventory annual time-series Edition 1”.* **GEUS Dataverse.** [https://doi.org/10.22008/FK2/MBKW9N](https://doi.org/10.22008/FK2/MBKW9N)
- How, P. et al. (Submitted) *“The Greenland Ice-Marginal Lake Inventory Series from 2016 to 2023”.* **Earth System Science Data.**
- How, P. et al. (2021) *“Greenland-wide inventory of ice marginal lakes using a multi-method approach”*. **Scientific Reports** 11, 4481. [https://doi.org/10.1038/s41598-021-83509-1](https://doi.org/10.1038/s41598-021-83509-1)

And include the following statement in the acknowledgements:

*“Ice marginal lake data provided by the European Space Agency (ESA), and the Programme for Monitoring of the Greenland Ice Sheet (PROMICE) at the Geological Survey of Denmark and Greenland (GEUS) (https://doi.org/10.22008/FK2/MBKW9N).”*


# Acknowledgements

This work is funded by the ESA Living Planet Fellowship (4000136382/21/I-DT-lr) entitled "Examining Greenland's Ice Marginal Lakes under a Changing Climate". Further support was provided by [PROMICE (Programme for Monitoring of the Greenland Ice Sheet)](https://promice.org), which is funded by the Geological Survey of Denmark and Greenland (GEUS) and the Danish Ministry of Climate, Energy and Utilities under the Danish Cooperation for Environment in the Arctic (DANCEA), conducted in collaboration with DTU Space (Technical University of Denmark) and Asiaq Greenland Survey.


# References

