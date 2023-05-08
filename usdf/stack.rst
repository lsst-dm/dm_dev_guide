############
Stack Access
############

This document describes access to nightly, weekly, and release versions of the
LSST Science Pipelines "stack" available at the USDF.

Release and Weekly
==================

Access to self-contained release and weekly versions is available via cvmfs (e.g. ``v24.0.0`` or ``w_2023_01``).
Each version is available in three variants: a Conda environment with minimal dependencies for processing data, an extended Conda environment with packages appropriate for code developers, and an Apptainer container with the minimal environment.

Minimal processing Conda environment:

.. code-block:: bash

   source /cvmfs/sw.lsst.eu/linux-x86_64/lsst_distrib/w_2023_01/loadLSST.bash

Developer-friendly Conda environment:

.. code-block:: bash

   source /cvmfs/sw.lsst.eu/linux-x86_64/lsst_distrib/w_2023_01/loadLSST-ext.bash

Minimal processing Apptainer:

.. code-block:: bash

   apptainer run-help /cvmfs/sw.lsst.eu/containers/apptainer/lsst_distrib/w_2023_01.sif

provides more information.

You can see which versions are available by:
``ls /cvmfs/sw.lsst.eu/linux-x86_64/lsst_distrib/``
and
``ls /cvmfs/sw.lsst.eu/containers/apptainer/lsst_distrib/``

Shared Stack
============

A "shared stack" of stack installations is available at ``/sdf/group/rubin/sw/``.
These installations share base Conda environments when possible, making it simpler to switch between versions using ``eups`` alone.
The ``rubin-rsp-developer`` metapackage containing packages appropriate for code developers (or its equivalent for earlier 2022 versions) has been installed in the Conda environment.

To get the latest weekly environment and its compatible stack versions:

.. code-block:: bash

   source /sdf/group/rubin/sw/w_latest/loadLSST.sh

To get the bleeding-edge latest daily environment (often the same as the latest weekly but sometimes more advanced) and its compatible stack versions:

.. code-block:: bash

   source /sdf/group/rubin/sw/d_latest/loadLSST.sh

To get the environment for a specific version:

.. code-block:: bash

   source /sdf/group/rubin/sw/tag/w_2023_01/loadLSST.sh

The last 24 daily releases and the last 26 weekly releases, as well as all official releases and release candidates after v23_0_2 are intended to be available.

Note that you can access ``conda`` from the stack install; SDF does not provide a central ``conda`` install.

After initializing the environment as above, you can use the EUPS ``setup`` command (e.g. ``setup lsst_distrib`` or ``setup lsst_sitcom``) to choose a compatible version of the Science Pipelines packages.
By default, ``setup`` will use the *latest* weekly that is compatible with the environment you chose, regardless of how you got that environment, as that is the version that is tagged with ``current``.

If you need a specific version, you should use ``source /sdf/group/rubin/sw/tag/{version}/loadLSST.sh; setup -t {version} {package}`` where ``{package}`` is ``lsst_distrib`` or ``lsst_sitcom`` or any other Science Pipelines package.
