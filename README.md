# GrIML - Investigating Greenland's ice-marginal lakes under a changing climate

[![PyPI version](https://badge.fury.io/py/griml.svg)](https://badge.fury.io/py/griml) [![DOI](https://zenodo.org/badge/444752900.svg)](https://zenodo.org/badge/latestdoi/444752900) [![JOSS](https://joss.theoj.org/papers/a2e10775df44b89f26b0ac9dbf8bc9e3/status.svg)](https://joss.theoj.org/papers/a2e10775df44b89f26b0ac9dbf8bc9e3) [![Documentation Status](https://readthedocs.org/projects/griml/badge/?version=latest)](https://griml.readthedocs.io/en/latest/?badge=latest) [![Build Status](https://img.shields.io/endpoint.svg?url=https%3A%2F%2Factions-badge.atrox.dev%2FPennyHow%2FGrIML%2Fbadge%3Fref%3Dmain&style=flat)](https://actions-badge.atrox.dev/PennyHow/GrIML/goto?ref=main) [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/GEUS-Glaciology-and-Climate/GrIML/HEAD?urlpath=%2Fdoc%2Ftree%2Ftutorials%2Fdataset_tutorial.ipynb)

The **GrIML** (Investigating Greenland's ice marginal lakes under a changing climate) processing package for classifying water bodies from satellite imagery using a multi-sensor, multi-method remote sensing approach. This workflow is used for the production of the [Greenland ice-marginal lake inventory series](https://doi.org/10.22008/FK2/MBKW9N), as part of the [ESA GrIML project](https://eo4society.esa.int/projects/griml/). This repository also holds all project-related materials.


## Installation

The GrIML Python package can be installed using pip: 

```
$ pip install griml
```

Or cloned from the Github repository: 

```
$ git clone git@github.com:GEUS-Glaciology-and-Climate/GrIML.git
$ cd GrIML
$ pip install .
```

Full documentation and tutorials are available at GrIML's [readthedocs](https://griml.readthedocs.io)


## Workflow outline

<img src="https://github.com/GEUS-Glaciology-and-Climate/GrIML/blob/main/docs/figures/griml_workflow_with_gee.png?raw=true" alt="The GrIML workflow." width="1500" align="aligncenter" />

**GrIML** proposes to examine ice marginal lake changes across Greenland using a multi-sensor and multi-method remote sensing approach to better address their influence on sea level contribution forecasting.

Ice-marginal lakes are detected using a remote sensing approach, based on offline workflows developed within the [ESA Glaciers CCI](https://catalogue.ceda.ac.uk/uuid/7ea7540135f441369716ef867d217519") (Option 6, An Inventory of Ice-Marginal Lakes in Greenland) ([How et al., 2021](https://www.nature.com/articles/s41598-021-83509-1)). Initial classifications are performed using Google Earth Engine, with the scripts available [here](https://github.com/GEUS-Glaciology-and-Climate/GrIML/tree/main/gee_scripts). Lake extents are defined through a multi-sensor approach using:

- Multi-spectral indices classification from Sentinel-2 optical imagery
- Backscatter classification from Sentinel-1 SAR (synthetic aperture radar) imagery
- Sink detection from ArcticDEM digital elevation models 

Post-processing of these classifications is performed using the **GrIML** Python package, including raster-to-vector conversion, filtering, merging, metadata population, and statistical analysis.


## Terms of use

If the workflow or data are presented or used to support results of any kind, please include an acknowledgement and references to the applicable publications:

*How, P. et al. (2025) "Greenland Ice-Marginal Lake Inventory annual time-series Edition 1". GEUS Dataverse. [https://doi.org/10.22008/FK2/MBKW9N](https://doi.org/10.22008/FK2/MBKW9N)*

*How, P. et al. (In Review) "The Greenland Ice-Marginal Lake Inventory Series from 2016 to 2023". Earth Syst. Sci. Data Discuss. [https://doi.org/10.5194/essd-2025-18](https://doi.org/10.5194/essd-2025-18)*

*How, P. (2025) PennyHow/GrIML v1.0.0, Zenodo, [https://doi.org/10.5281/zenodo.14718898](https://doi.org/10.5281/zenodo.14718898)*

*How, P. et al. (2021) "Greenland-wide inventory of ice marginal lakes using a multi-method approach". Sci. Rep. 11, 4481. [https://doi.org/10.1038/s41598-021-83509-1](https://doi.org/10.1038/s41598-021-83509-1)*


## Project links

- [The Greenland ice-marginal lake inventory series](https://doi.org/10.22008/FK2/MBKW9N), available through the [GEUS Dataverse](https://dataverse.geus.dk/)

- ESA [project outline](https://eo4society.esa.int/projects/griml/) and [fellow information](https://eo4society.esa.int/lpf/penelope-how/)

- [GrIML project description](https://pennyhow.github.io/blog/investigating-griml/)

- Information about the [ESA Living Planet Fellowship](https://eo4society.esa.int/communities/scientists/living-planet-fellowship/)

- 2017 ice marginal lake inventory [Scientific Reports paper](https://www.nature.com/articles/s41598-021-83509-1) and [dataset](https://catalogue.ceda.ac.uk/uuid/7ea7540135f441369716ef867d217519)
