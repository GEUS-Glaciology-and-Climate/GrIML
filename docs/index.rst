.. GrIML documentation master file, created by
   sphinx-quickstart on Tue Apr 26 16:51:31 2022.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

GrIML
=====

The **GrIML** (Investigating Greenland's ice marginal lakes under a changing climate) processing package is for classifying water bodies from satellite imagery using a multi-sensor, multi-method remote sensing approach. It meets four main needs of users in the remote sensing and cryospheric science communities:

- Provide a usable workflow for processing rasterised water body classifications
- Document the criteria for classifying an ice-marginal lake
- Showcase a transparent workflow that, in turn, produces an open and reproducible ice-marginal lake dataset that adheres to the FAIR principles
- Produce inventories that map the areal extent and abundance of ice-marginal lakes across Greenland, which demonstrate ice-marginal lake evolution under a changing climate

The package needs a satellite (or aerial) binary raster image, or a set of binary raster images, as an input to produce a merged, curated vector file of polygon outlines denoting the locations of ice-marginal lakes. It has been used to produce the Greenland ice-marginal lake inventory series, which maps the presence and extents of water bodies across Greenland that share a margin with the Greenland Ice Sheet and/or the surrounding ice caps and periphery glaciers since 2016. 

The documentation pages provided with GrIML guide users through: 1) running the lake classification code and 2) provides examples of working with the Greenland dataset produced from this package.

If the GrIML package or the Greenland ice marginal lake inventory series are presented or used to support results of any kind, please include references to the applicable publications:

- **How, P. et al. (2025) "Greenland Ice-Marginal Lake Inventory annual time-series Edition 1". GEUS Dataverse. https://doi.org/10.22008/FK2/MBKW9N**
- **How, P. et al. (In Review) "The Greenland Ice-Marginal Lake Inventory Series from 2016 to 2023". Earth Syst. Sci. Data Discuss. https://doi.org/10.5194/essd-2025-18**
- **How, P. (In Review) "A Python package for investigating Greenland's ice marginal lakes under a changing climate". JOSS.**
- **How, P. et al. (2021) "Greenland-wide inventory of ice marginal lakes using a multi-method approach". Sci. Rep. 11, 4481. https://doi.org/10.1038/s41598-021-83509-1**

And include the following statement in the acknowledgements:

*"Ice-marginal lake data provided by the European Space Agency (ESA), and the Programme for Monitoring of the Greenland Ice Sheet (PROMICE) at the Geological Survey of Denmark and Greenland (GEUS) (https://doi.org/10.22008/FK2/MBKW9N)."*


.. toctree::
   :maxdepth: 2
   :caption: Contents:
   
   installation
   background/index
   tutorials/index
   contributing
   acknowledgements
   modules



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
