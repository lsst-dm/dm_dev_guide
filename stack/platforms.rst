###################
Supported Platforms
###################

Introduction
============

The Science Pipelines are required to be portable across many compute platforms ranging from high-performance computing centers to laptops (refer to DMS-REQ-0308 in :lse:`61`).
The software will likely work on any Unix-like systems but we limit our testing and support to a fixed set of platforms.
Patches may be accepted from developers who test on other operating systems.

Platforms
=========

We have a baseline platform which is what we are using for integration testing and deployments.
For each product, we also have a number of other platforms which are regularly tested by our continuous integration system to enhance portability.

The baseline system is currently CentOS 7 on Intel x86_64 with gcc 8.3.1 from devtoolset-8 and Python 3.7.

.. note ::
    We aim to stay current with CentOS 7 minor releases, updating within 6 months of their release.

We regularly test the following platforms in addition to the baseline platform:

* CentOS 6 with devtoolset-8
* macOS Mojave (10.14) with Apple clang compilers
* macOS High Sierra (10.13) with Apple clang compilers

See https://ci.lsst.codes for the current list of regularly-tested platforms.
(The "osx" platform there for the "stack-os-matrix" job randomly chooses a Mojave or High Sierra machine for each execution to limit load.)
