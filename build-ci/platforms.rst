###################
Supported Platforms
###################

Introduction
============

The LSST Data Management software is required to be portable across many compute platforms ranging from high-performance computing centers to laptops (DMS-REQ-0308).
The software will likely work on any Unix-like systems but we limit our testing and support to a fixed set of platforms.

Patches may be accepted from developers who test on other operating systems.

Platforms
=========

We have a baseline platform which is what we are using for integration testing and deployments.
For each product, we also have a number of other platforms which are regularly tested by our continuous integration system to enhance portability.

The baseline system is currently CentOS 7 on Intel x86_64 with gcc 6.3.1 from devtoolset-6 and Python 3.6.

We regularly-test the following platforms in addition to the baseline platform:

* CentOS 6 with devtoolset-6
* macOS Sierra with Apple clang compilers
* macOS High Sierra with Apple clang compilers

See https://ci.lsst.codes for the current list of regularly-tested platforms.
