###################
Supported Platforms
###################

Introduction
============

The Science Pipelines are required to be portable across many compute platforms ranging from high-performance computing centers to laptops (refer to DMS-REQ-0308 in :lse:`61`).
The software will likely work on any Unix-like systems but we limit our testing and support to a fixed set of platforms.
Patches may be accepted from developers who test on other operating systems.

.. _platforms-baseline:

Platforms
=========

We have a baseline platform which is what we are using for integration testing and deployments.
For each product, we also have a number of other platforms which are regularly tested by our continuous integration system to enhance portability.

The baseline platform is currently CentOS 7 on Intel x86_64.

.. note ::
    We aim to stay current with CentOS 7 minor releases, updating within 6 months of their release.

We regularly test the following platforms in addition to the baseline platform:

* macOS Mojave (10.14);
* macOS High Sierra (10.13).

See https://ci.lsst.codes for the current list of regularly-tested platforms.
(The "osx" platform there for the "stack-os-matrix" job randomly chooses a Mojave or High Sierra machine for each execution to limit load.)

.. _platforms-environment:

Environment
===========

On each of these platforms, we rely on `Conda`_ and `conda-forge`_ to provide our build- and run-time dependencies, including compilers and the Python interpreter.
The Conda environment for Science Pipelines is available in the `scipipe_conda_env`_ repository.
This defines the environment within which our code must execute: all code must be compatible with the contents of this environment when it is written; compatibility with older or newer environments is not guaranteed.
The Conda environment is periodically updated to pull in newer versions of third party packages.
To request such an update, or to request that a new package be added to the environment, please :doc:`file an RFC </communications/rfc>`.

.. _Conda: https://conda.io
.. _conda-forge: https://conda-forge.org/
.. _scipipe_conda_env: https://github.com/lsst/scipipe_conda_env
