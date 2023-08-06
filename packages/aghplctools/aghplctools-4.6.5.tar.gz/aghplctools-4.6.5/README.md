# Agilent HPLC tools

This package contains methods and classes designed to facilitate automation processes which incorporate Agilent HPLC 
instruments. The code was written and is maintained by the [Hein Group](https://groups.chem.ubc.ca/jhein/) at the 
University of British Columbia and is not an Agilent product. 

## General overview 

Data classes may be found in the `data` and `ingestion` subpackages for processing results in single or batch processes. 
Currently supported file formats include: 

- `*.UV` files (raw 3D spectrum)
- `Report.txt` files (reports generated post-run with integration reports)
- several metadata sources for extraction of sample context

Indirect monitoring of a sampling sequence is facilitated by the `local_paths` module. These tools may be used to 
passively monitor for the currently acquiring sample so that it may be processed in a live-manner rather than post-processed. 
Paths may be specified manually or automatically determined from the ChemStation configuration file which appears 
on computers with ChemStation installed. 

## Authors and contributors 

Lars Yunker 
Henry Situ
