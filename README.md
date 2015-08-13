# LSST Stack Documentation Prototype

This repository contains the base source material for LSST's Stack Documentation.
Documentation is built using [Sphinx](http://sphinx-doc.org), which pulls in documentation material from LSST code repositories.

Note that repository is a prototype of the LSST Stack's next-generation documentation platform.
The official Stack documentation is located at https://confluence.lsstcorp.org/display/LSWUG.

## Building the Docs

### Pre-requisites

```
pip install sphinx
```

### Building HTML

Run

```
make html
```

The site will be built in the `_build/` directory.

## Licensing

Copyright 2015 AURA/LSST

Content is licensed Creative Common Non-Commercial Share Alike (CC-NC-SA).
Source code is licensed GPLv2.
