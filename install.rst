#########################
Installing the LSST Stack
#########################

This page will guide you through installing the LSST Stack from source to use for data processing.
Developers should follow :doc:`/development/getting_started` instead.

We are working on methods for binary installation and Docker distribution.
In the meantime, Fabio Hernandez of IN2P3 has kindly arranged to make `binary distributions of versions v9_2 and v10_1-rc3 available via CernVM FS <https://github.com/airnandez/lsst-cvmfs>`_.
Scientific Linux 6, Scientific Linux 7, CentOS 7, Ubuntu 14.04 and Mac OS X 10.10 are supported with the CernVM FS-based distribution.
If this binary distribution does not suit your needs, please read on to install the LSST Stack from source.

*************
Prerequisites
*************

The LSST Stack is officially tested against CentOS 6.6, however stack developers regularly use `a variety of Linux and Mac OS X operating systems <https://docs.google.com/spreadsheets/d/10HKv4s0xY6VlldauR_6_vgwRlvZwSw9bIshoUx7iark/edit#gid=960512304>`_. The following sections detail how to install pre-requisite software for your Debian/Ubuntu-based, RedHat/CentOS-based, or Mac OS X system.

The listed pre-requisites are known to work for v10.1.

.. todo::

   Provision the pre-req lists dynamically from the Puppet file. Even better, allow the user to select the platform and pre-filter the page to show only the needed information. See https://github.com/lsst-sqre/puppet-lsststack/blob/master/manifests/params.pp.

Debian/Ubuntu
=============

Debian/Ubuntu systems use ``apt-get`` to install packages.
This ``apt-get`` command will provision Debian-type systems for the LSST Stack
(prepend the command with ``sudo`` if necessary)::

    apt-get install bison cmake curl flex g++ gettext git \
    libbz2-dev libcurl4-openssl-dev libfontconfig1 libglib2.0-dev \
    libncurses5-dev libreadline6-dev libx11-dev \
    libxrender1 libxt-dev m4 make openjdk-7-jre \
    perl-modules zlib1g-dev -y

The Stack also requires Python 2.7.
If your system doesn't come with a recent version of Python 2.7, you can elect to allow the stack to install Python locally via Anaconda for you later in the process.

RedHat/CentOS
=============

RedHat/CentOS systems use ``yum`` to install packages.
This ``yum`` command will provision RedHat-type systems for the LSST Stack
(prepend the command with ``sudo`` if necessary)::

    yum install blas bison bzip2 bzip2-devel cmake curl flex \
    fontconfig freetype-devel gcc-c++ gcc-gfortran gettext git \
    glib2-devel libXext libXrender libXt-devel libcurl-devel \
    libuuid-devel make ncurses-devel openssl-devel patch perl \
    perl-ExtUtils-MakeMaker readline-devel zlib-devel

The Stack also requires Python 2.7.
If your system doesn't come with a recent version of Python 2.7, you can elect to allow the stack to install Python locally via Anaconda for you later in the process.

Mac OS X
========

We have tested the stack on Mavericks (10.9) and Yosemite (10.10).

You will need to install developer tools, which we recommend you obtain with Apple's Xcode command line tools package.
To do this, run from the command line (e.g. ``Terminal.app`` or similar)::

    xcode-select --install

and follow the on-screen instructions.
You can verify where the tools are installed by running::

    xcode-select -p

.. todo::

   Provide pre-req installation procedures for OS X.
   Should Homebrew be the defacto way to install all pre-requisites?

Optional Dependencies
=====================

Although not required, we recommend you install the `matplotlib <http://matplotlib.org>`_ and `scipy <http://scipy.org>`_ Python packages::

    pip install -U matplotlib scipy

Note these are included by default in `Anaconda <https://store.continuum.io/cshop/anaconda/>`_, which the LSST Stack *can* install for you.

We also use `SAOImage DS9 <http://ds9.si.edu/site/Home.html>`_ to display images for debugging.

**********************
Installing from Source
**********************

This section will guide you through installing the *current* release of the LSST Stack from source given that prerequisites have been installed.

Choose an Installation Directory
================================

First, choose where you want to install the LSST Stack.
We'll use ``$HOME/lsst_stack`` in this example.
Create and change into that directory::

    mkdir -p $HOME/lsst_stack
    cd $HOME/lsst_stack

.. note::

   **Installation for Groups.**
   
   Those in a system administration role, who are installing a writable stack for multiple users, will likely want to establish a separate group (perhaps lsst) with a umask of 002 (all access permissions for the group; allow other users to read+execute).
   The installation directory must be owned by the group, have the SGID (2000) bit set, and allow group read/write/execute: that is, mode 2775.
   Individual users who install a personal Stack on their own machine need not worry about this.

Unset Environment Variables
===========================

If you've been running the LSST Stack previously, you may have conflicting environment variables setup.
To be safe, run::

    unset LSST_HOME EUPS_PATH LSST_DEVEL EUPS_PKGROOT REPOSITORY_PATH

Installation Set-up
===================

Download and run the installation setup script, which installs the basic packages required to install other packages::

    curl -OL https://sw.lsstcorp.org/eupspkg/newinstall.sh
    bash newinstall.sh

This installs the ``loadLSST.*`` scripts, which you should source to ensure that LSST tools (e.g., the eups command) are included in your path.

The install script will check your system to ensure that appropriate versions of critical packages are installed on your system, to enable bootstrapping the Stack, including ``git``, and ``python``.
If these packages are not available, the script will offer to install them for you (using the Anaconda Python distribution for the latter packages). 

Allowing the installation of these core packages will not replace or modify any other version of these packages that may be installed on your system.
If you do not choose the Anaconda Python install, and subsequent package build steps fail, you can do one of two things:

* Report the problem to `community.lsst.org <community.lsst.org>`_. Include your OS, a description of the problem, plus any error messages. Community members will provide assistance.
* Consider removing all contents of the install directory and start from scratch, and accepting the Anaconda Python installation option.

Once ``newinstall.sh`` has finished, source the LSST environment to continue the installation::

    source $LSST_INSTALL_DIR/loadLSST.bash # for bash users
    source $LSST_INSTALL_DIR/loadLSST.csh  # for csh users
    source $LSST_INSTALL_DIR/loadLSST.ksh  # for ksh users
    source $LSST_INSTALL_DIR/loadLSST.zsh  # for zsh users

where ``$LSST_INSTALL_DIR`` is expanded to your installation directory.

Install Packages
================

Finally, build/install any other components of the LSST Stack that are relevant for your work.
Many users will want to make use of the pipelines or applications code.
A simple way to ensure that you have a fairly complete set of packages for this need is to install ``lsst_apps``.
The dependency tree for ``lsst_apps`` ensures that many other packages (about 70, including e.g., ``pipe_tasks``) are also installed. 

Installing ``lsst_apps`` may take a little while (about 1.2 hr on a 2014-era iMac with 32 GB of memory and 8 cores)::

    eups distrib install -t v10_1 lsst_apps

After this initial setup, it is a good idea to test the installation.
See :ref:`testing-your-installation`.

Load the LSST Environment in Each Terminal Session
==================================================

Whenever you want to run the install LSST Stack in a new terminal session, be sure to load the appropriate ``loadLSST.{bash,csh,ksh,zsh}`` script.

.. _testing-your-installation:

*************************
Testing Your Installation
*************************

Choose a directory to install demo data into.
We'll call this directory ``$DEMO_DATA``.
The directory where you installed the stack is ``$LSST_INSTALL_DIR``.
Then run:

::

    source $LSST_INSTALL_DIR/loadLSST.sh
    mkdir -p $DEMO_DATA
    cd $DEMO_DATA
    curl -L https://github.com/lsst/lsst_dm_stack_demo/archive/10.1.tar.gz | tar xvzf -
    cd lsst_dm_stack_demo-10.1

The demo repository consumes roughly 41 MB, contains input images, reference data, and configuration files.
The demo script will process SDSS images from two fields in Stripe 82, as shown in the following table (filters in parentheses are not processed if run with the ``--small`` option):

==== ====== ===== =========
run  camcol field filters
==== ====== ===== =========
4192 4      300   *(ur)giz*
6377 4      399   *(gz)uri*
==== ====== ===== =========

Now setup the processing package and run the demo:

::

    setup obs_sdss
    ./bin/demo.sh # --small to process a subset of images

For each input image the script performs the following operations:

* generate a subset of basic image characterization (e.g., determine photometric zero-point, detect sources, and measures positions, shapes, brightness with a variety of techniques)
* creates a ``./output`` subdirectory containing subdirectories of configuration files, processing metadata, calibrated images, FITS tables of detected sources. These "raw" outputs are readable by other parts of the LSST pipeline
* generates a master comparison catalog in the working directory from the band-specific source catalogs in the ``output/sci-results/`` subdirectories.

The demo will take a minute or two to execute (depending upon your machine), and will generate a large number of status messages.
Upon successful completion, the top-level directory will contain an output ASCII table that can be compared to the expected results from a reference run.
This table is for convenience only, and would not ordinarily be produced by the production LSST pipelines.  

=============== ========================== ===================================
Demo Invocation Demo Output                Reference output
=============== ========================== ===================================
demo.sh         detected-sources.txt       detected-sources.txt.expected
demo.sh --small detected-sources_small.txt detected-sources_small.txt.expected
=============== ========================== ===================================

The demo output may not be identical to the reference output due to minor variation in numerical routines between operating systems (see `DM-1086 <https://jira.lsstcorp.org/browse/DM-1086>`_ for details).
The ``bin/compare`` script will check whether the output matches the reference to within expected tolerances:

::

    bin/compare detected-sources.txt.expected detected-sources.txt

The script will print "``Ok``" if the demo ran correctly.

For more information about the processing done by the demo, refer to `its README on GitHub <https://github.com/lsst/lsst_dm_stack_demo>`_.

.. todo::

   I'm leaving out all the stuff about interpreting the demo data.
   Folks should learn from tutorials instead.

.. todo::
   
   We should have a straight-forward script that runs the demo and runs a comparison to verify the reproducibility of the stack.
