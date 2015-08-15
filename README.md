# LSST Stack Documentation Prototype

This repository contains the base source material for LSST's Stack Documentation.
Documentation is built using [Sphinx](http://sphinx-doc.org), which pulls in documentation material from LSST code repositories.

Note that this repository is a prototype of the LSST Stack's next-generation documentation platform.
The official Stack documentation is located at https://confluence.lsstcorp.org/display/LSWUG.

## Build the Docs

Create a [Python virtual environment](http://docs.python-guide.org/en/latest/dev/virtualenvs/) for this project using your tool of choice: [virtualenvwrapper](http://virtualenvwrapper.readthedocs.org/en/latest/) or [pyvenv](https://docs.python.org/3.5/library/venv.html) (for Python 3).

Install the Python dependencies by running

```
pip install -r requirements.txt
```

Compile the HTML by running

```
make html
```

The site will be built in the `_build/` directory.

## Licensing

Copyright 2015 AURA/LSST

Content is licensed Creative Common Non-Commercial Share Alike (CC-NC-SA).
Source code is licensed GPLv3.
