# Janis - Unix

[![Documentation Status](https://readthedocs.org/projects/janis/badge/?version=latest)](https://janis.readthedocs.io/en/latest/tools/unix/index.html)
[![Build Status](https://travis-ci.org/PMCC-BioinformaticsCore/janis-unix.svg?branch=master)](https://travis-ci.org/PMCC-BioinformaticsCore/janis-unix)
[![PyPI version](https://badge.fury.io/py/janis-pipelines.unix.svg)](https://badge.fury.io/py/janis-pipelines.unix)

This repository contains common unix tools and data types for [Janis](https://github.com/PMCC-BioinformaticsCore/janis).

Refer to the [documentation](https://janis.readthedocs.io/en/latest/tools/bioinformatics/index.html).


## Data types

The data types are a way of encapsulating information about a particular input or output.
Some common unix data types are `CSV`, `TSV` or `TarFile`. Visit the documentation for a full list.

## Documentation

Documentation is generated on [Janis](https://github.com/PMCC-BioinformaticsCore/janis). 
To generate new documentation you will need to: 
1. Commit your changes here,
2. Update the submodule pointer on Janis,
3. Checkout Janis (recursively),
4. Run the regenerate script `janis/docs/regeneratedocumentation.py`,
5. Commit these changes and the documentation will autobuild on ReadTheDocs.
