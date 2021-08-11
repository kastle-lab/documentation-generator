# Documenation-Generator

## Installation
* Requires Python 3.7+ 
* Requires [RDFlib](https://github.com/RDFLib/rdflib) 

## Execution
* Ensure desired, _annotated_ OWL files are in the `./patterns` directory
* Run `python documentation-generator.py` from command line

## Repository Structure

### Source
This is found under the `./documentation-generator/` directory.

### Input
The input for this program is expected to be in two folders:
* `./patterns` where the input OWL files are expected.
* `./schema-diagrams` where any resource that the annotations in the OWL file will be expected.

### Output
This is found under the `./documentation/` directory