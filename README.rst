##################################
LSST Stack Documentation Prototype
##################################

This repository contains the base source material for LSST's Stack Documentation.
Documentation is built using `Sphinx`_, which pulls in documentation material from LSST code repositories.

.. _Sphinx: http://sphinx-doc.org

Note that this repository is a prototype of the LSST Stack's next-generation documentation platform.
The official Stack documentation is located at https://confluence.lsstcorp.org/display/LSWUG.

Build the Docs
==============

The full docs can only be built in conjunction with `lsstsw`_.

.. _lsstsw: https://github.com/lsst/lsstsw

In a terminal session where lsstsw has been installed, setup *and* built, set ``$LSSTSW_BUILD_DIR`` as the full path to the directory where ``lsstsw/build/`` is located::

    export LSSTSW_BUILD_DIR=/path/to/lsstsw/build

Clone this doc repository along side, *but not in*, the lsstsw directory and install Python requirements::

    pip install -r requirements.txt

From within this doc repository, you can compile the documentation HTML by running::

   make html

The site will be built in the `_build/html/` directory.

Licensing
=========

.. image:: https://cdn.rawgit.com/lsst-sqre/lsst_stack_docs/master/_static/cc-by_large.svg?raw=true

LSST Stack Handbook by The LSST Project is licensed under a `Creative Commons Attribution 4.0 International License <http://creativecommons.org/licenses/by/4.0/>`_.

Copyright 2015 AURA/LSST
