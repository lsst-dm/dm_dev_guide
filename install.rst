#####################################
Installing the LSST Science Pipelines
#####################################

This page will guide you through installing the LSST Science Pipelines from source for data processing.

The LSST Science Pipelines are officially tested against CentOS 7, however developers regularly use `a variety of Linux and Mac OS X operating systems <https://ls.st/faq>`_.

We are working on methods for binary installation and Docker distribution.
In the meantime, Fabio Hernandez of IN2P3 has kindly arranged to make `binary distributions of releases available via CernVM FS <https://github.com/airnandez/lsst-cvmfs>`_.
Scientific Linux 6, Scientific Linux 7, CentOS 7, Ubuntu 14.04 and Mac OS X 10.10 are supported with the CernVM FS-based distribution.
If this binary distribution does not suit your needs, please read on to install the LSST Science Pipelines from source.

Developers should follow :doc:`/development/lsstsw_tutorial` instead.

If you have difficulty installing LSST software, reach out on the `Support forum at community.lsst.org <community.lsst.org/c/qa>`_.

.. _source-install-prereqs:

Prerequisites
=============

**New for 11.0**: The minimum gcc version required to compile the Stack is **gcc 4.8.**
If you using our previous factory platform, RedHat/CentOS 6, and you are unable to upgrade to version 7 (which comes with gcc 4.8 as default) consult :ref:`the section below on upgrading compilers in legacy Linux. <source-install-redhat-legacy>`.

.. FIXME add section link above

..
   Provision the pre-req lists dynamically from the Puppet file. Even better, allow the user to select the platform and pre-filter the page to show only the needed information. See https://github.com/lsst-sqre/puppet-lsststack/blob/master/manifests/params.pp.

.. _source-install-mac-prereqs:

Mac OS X
--------

We have tested the Science Pipelines on OS X Yosemite (10.10).

The Science Pipelines are not currently supported on OS X El Capitan (10.11).
See :doc:`Known Issues for v11.0 </releases/v11_0/known>`.
Versions prior to OS X 10.9 and earlier have not been tested recently and may not work.

You will need to install developer tools, which we recommend you obtain with Apple's Xcode command line tools package.
To do this, run from the command line (e.g. ``Terminal.app`` or similar):

.. code-block:: bash

   xcode-select --install

and follow the on-screen instructions.
You can verify where the tools are installed by running:

.. code-block:: bash

   xcode-select -p

.. _source-install-debian-prereqs:

Debian / Ubuntu
---------------

.. code-block:: bash

   apt-get install make bison curl ca-certificates flex \
       g++ git libbz2-dev libreadline6-dev libx11-dev \
       libxt-dev m4 zlib1g-dev libxrender1 libfontconfig1 \
       libncurses5-dev cmake libglib2.0-dev openjdk-7-jre \
       gettext libcurl4-openssl-dev perl-modules -y

Prefix the ``apt-get`` command with ``sudo`` if necessary.

.. _source-install-redhat-prereqs:

RedHat / CentOS
---------------

.. code-block:: bash

   yum install bison curl blas bzip2-devel bzip2 flex fontconfig \
       freetype-devel gcc-c++ gcc-gfortran git libuuid-devel \
       libXext libXrender libXt-devel make openssl-devel patch perl \
       readline-devel tar zlib-devel ncurses-devel cmake glib2-devel \
       java-1.8.0-openjdk gettext libcurl-devel \
       perl-ExtUtils-MakeMaker

Prefix the ``yum`` command with ``sudo`` if necessary.

.. _source-install-redhat-legacy:

Upgrading compilers for legacy RedHat / CentOS 6
------------------------------------------------

The minimum gcc version required to compile the Stack is gcc 4.8.
This comes as standard in the LSST "factory" platform, Red Hat / CentOS 7.

On our previous factory platform, Red Hat / CentOS 6, you will need to use a more current version of gcc that what is available with your system.
If you can go to Red Hat 7, we recommend that you do; if you cannot, we recommend that you use a newer gcc version for the stack by using a Software Collection (SCL) with a different version of devtoolset.
This will enable you to safely use a different version of gcc (4.9) for the stack than that used by your operating system (4.4).

First, install ``devtoolset-3`` (after the :ref:`installing the standard pre-requisites (above) <source-install-redhat-prereqs>`):

.. code-block:: bash

   sudo yum install -y https://dl.fedoraproject.org/pub/epel/epel-release-latest-6.noarch.rpm
   sudo yum install -y https://www.softwarecollections.org/en/scls/rhscl/rh-java-common/epel-6-x86_64/download/rhscl-rh-java-common-epel-6-x86_64.noarch.rpm
   sudo yum install -y https://www.softwarecollections.org/en/scls/rhscl/devtoolset-3/epel-6-x86_64/download/rhscl-devtoolset-3-epel-6-x86_64.noarch.rpm
   sudo yum install -y scl-utils
   sudo yum install -y devtoolset-3

Then enable ``devtoolset-3`` by including this line in your :file:`~/.bash_profile`:

.. code-block:: bash

   scl enable devtoolset-3 bash

.. _source-install-py-deps:

Python dependencies
-------------------

You can use your own Python 2.7.\* install or let ``newinstall.sh`` install `Anaconda <https://www.continuum.io/downloads>`_ in your local directory.

.. _source-install-optional-deps:

Optional dependencies
---------------------

Although not required, we recommend you install the `matplotlib <http://matplotlib.org>`_ and `scipy <http://scipy.org>`_ Python packages:

.. prompt:: bash

   pip install -U matplotlib scipy

Note these are included by default in `Anaconda <https://store.continuum.io/cshop/anaconda/>`_, which ``newinstall.sh`` *can* obtain for you.

We also use `SAOImage DS9 <http://ds9.si.edu/site/Home.html>`_ to display images for debugging.

.. _install-from-source:

Installing from Source with newinstall.sh
=========================================

This section will guide you through installing the *current* release of the LSST Science Pipelines from source given that prerequisites have been installed.

.. _install-from-source-dir:

1. Choose an installation directory
-----------------------------------

First, choose where you want to install the LSST Science Pipelines.
We'll use ``$HOME/lsst_stack`` in this example.
Create and change into that directory:

.. prompt:: bash

   mkdir -p $HOME/lsst_stack
   cd $HOME/lsst_stack

Installation for groups
^^^^^^^^^^^^^^^^^^^^^^^
   
Those in a system administration role, who are installing a writable stack for multiple users, will likely want to establish a separate group (perhaps lsst) with a umask of 002 (all access permissions for the group; allow other users to read+execute).
The installation directory must be owned by the group, have the SGID (2000) bit set, and allow group read/write/execute: that is, mode 2775.
Individual users who install a personal Stack on their own machine need not worry about this.

.. _install-from-source-envvar:

2. Unset environment variables
------------------------------

If you've run the LSST Science Pipelines previously, you may have conflicting environment variables setup.
To be safe, run:

.. code-block:: bash

   unset LSST_HOME EUPS_PATH LSST_DEVEL EUPS_PKGROOT REPOSITORY_PATH

.. _install-from-source-setup:

3. Installation set-up
----------------------

Download and run the installation setup script, which installs the basic packages required to install other packages:

.. code-block:: bash

   curl -OL https://sw.lsstcorp.org/eupspkg/newinstall.sh
   bash newinstall.sh

This installs the ``loadLSST.*`` scripts, which you should source to ensure that LSST tools (e.g., the eups command) are included in your path.

The install script will check your system to ensure that appropriate versions of critical packages are installed on your system, to enable bootstrapping the Science Pipelines, including ``git``, and ``python``.
If these packages are not available, the script will offer to install them for you (using the Anaconda Python distribution for the latter packages). 

Allowing the installation of these core packages will not replace or modify any other version of these packages that may be installed on your system.
If you do not choose the Anaconda Python install, and subsequent package build steps fail, you can do one of two things:

* Report the problem to `community.lsst.org <community.lsst.org>`_. Include your OS, a description of the problem, plus any error messages. Community members will provide assistance.
* Consider removing all contents of the install directory and start from scratch, and accepting the Anaconda Python installation option.

Once ``newinstall.sh`` has finished, source the LSST environment to continue the installation by running the appropriate command for your shell:

.. code-block:: bash

   source $LSST_INSTALL_DIR/loadLSST.bash # for bash users
   source $LSST_INSTALL_DIR/loadLSST.csh  # for csh users
   source $LSST_INSTALL_DIR/loadLSST.ksh  # for ksh users
   source $LSST_INSTALL_DIR/loadLSST.zsh  # for zsh users

where ``$LSST_INSTALL_DIR`` is expanded to your installation directory.

.. _install-from-source-packages:

4. Install packages
-------------------

Finally, build/install any other components of the LSST Science Pipelines that are relevant for your work.
A simple way to ensure that you have a fairly complete set of packages for this need is to install ``lsst_apps``.
The dependency tree for ``lsst_apps`` ensures that many other packages (about 70, including e.g., ``pipe_tasks``) are also installed. 

Installing ``lsst_apps`` may take a little while (about 1.2 hr on a 2014-era iMac with 32 GB of memory and 8 cores):

.. code-block:: bash

   eups distrib install -t v11_0 lsst_apps

After this initial setup, it is a good idea to test the installation.
See :ref:`source-install-testing-your-installation`.

.. _install-from-source-loadlsst:

5. Source the LSST environment in each shell session
----------------------------------------------------

Whenever you want to run the installed LSST Science Pipelines in a new terminal session, be sure to ``source`` the appropriate ``loadLSST.{bash,csh,ksh,zsh}`` script.

.. _source-install-testing-your-installation:

Testing Your Installation
=========================

Choose a directory to install demo data into.
We'll call this directory ``$DEMO_DATA``.
The directory where you installed the stack is ``$LSST_INSTALL_DIR``.
Then run:

.. code-block:: bash

   source $LSST_INSTALL_DIR/loadLSST.sh
   mkdir -p $DEMO_DATA
   cd $DEMO_DATA
   curl -L https://github.com/lsst/lsst_dm_stack_demo/archive/11.0.tar.gz | tar xvzf -
   cd lsst_dm_stack_demo-11.0

The demo repository consumes roughly 41 MB, contains input images, reference data, and configuration files.
The demo script will process SDSS images from two fields in Stripe 82, as shown in the following table (filters in parentheses are not processed if run with the ``--small`` option):

==== ====== ===== =========
run  camcol field filters
==== ====== ===== =========
4192 4      300   *(ur)giz*
6377 4      399   *(gz)uri*
==== ====== ===== =========

Now setup the processing package and run the demo:

.. code-block:: bash

   setup obs_sdss
   ./bin/demo.sh # --small to process a subset of images

For each input image the script performs the following operations:

* generate a subset of basic image characterization (e.g., determine photometric zero-point, detect sources, and measures positions, shapes, brightness with a variety of techniques),
* creates a ``./output`` subdirectory containing subdirectories of configuration files, processing metadata, calibrated images, FITS tables of detected sources. These "raw" outputs are readable by other parts of the LSST pipeline, and
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

.. prompt:: bash

   bin/compare detected-sources.txt.expected detected-sources.txt

The script will print "``Ok``" if the demo ran correctly.

For more information about the processing done by the demo, refer to `its README on GitHub <https://github.com/lsst/lsst_dm_stack_demo>`_.

..
   I'm leaving out all the stuff about interpreting the demo data.
   Folks should learn from tutorials instead.
