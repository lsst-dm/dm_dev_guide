===================
Conda and rubin-env
===================

The Science Pipelines stack uses ``conda`` as its primary package manager for obtaining third-party Python and C++ dependencies.
In particular, the ``conda-forge`` distribution channel is used, as it provides a wide selection of community-maintained but rigorously verified packages.

.. _rubin-env-metapackage:

``rubin-env``
-------------

The list of required dependencies is maintained in a ``conda-forge`` metapackage named ``rubin-env``.
Use of a metapackage rather than an environment specification allows for simple installation and environment creation by end users.

``rubin-env`` is intended to be the minimal set of dependencies required to build and execute all packages of ``lsst_distrib`` in batch production.
It does not necessarily include dependencies useful for developers to modify existing packages or add new packages.
It also does not necessarily include dependencies useful for science users to analyze, visualize, or otherwise work with raw Science Pipelines inputs or output data products.

An expanded ``rubin-env-extras`` has been created that includes additional dependencies commonly used with the Science Pipelines to ensure that compatible versions of all packages can be determined.
These additional dependencies are used in the Rubin Science Platform, in the "shared stack" deployed on the Rubin development platforms at the NCSA LDF and the SLAC USDF, and in the rubin-sim metapackage.
Note that each of these other environments is maintained separately; see below.

Requests for additions to ``rubin-env`` should be made via RFC.
The DM-CCB must approve such requests.

.. _rubin-env-versioning:

Versioning ``rubin-env``
------------------------

``rubin-env`` has a standard semantic version number with major, minor, and patch components, in addition to a conda-internal build number.
These components are updated as follows:

* Build: increment when adding a ``<`` or ``!=`` pin for an existing dependency, as this preserves compatibility with previous builds of the environment.
* Patch: increment when adding a ``>`` pin for an existing dependency that is compatible with old code (no major version update) or when adding a ``<`` pin that is earlier than the previous pin.
* Minor: increment when adding a new dependency.
* Major: increment when removing a dependency, or when removing a pin, or when changing a dependency major version

Because of the way that conda-forge works, adding a build or patch or minor version increment to a *past* rubin-env release requires creating a new branch in the `rubinenv-feedstock <https://github.com/conda-forge/rubinenv-feedstock/>`__ repository.
For current releases, the ``main`` branch is used, of course.
The tip of each branch is built and published by the conda-forge automation (and of course older versions on each branch were published when they were the tip).

When updating rubin-env, the following procedure should be followed:

#. Update the dev branch in rubinenv-feedstock and ensure that it solves and builds.
   Add selectors to ``rubin-env-extras`` or pins to ``rubin-env`` if necessary to allow building.
#. Test the current Science Pipelines stack using the dev environment (install using the ``conda-forge/label/rubin-env_dev`` channel).
#. Test pip installation of `RSP dependencies <https://github.com/lsst-sqre/sciplat-lab/blob/prod/stage3-py.sh>`__ into the dev environment.
#. Create a ticket branch from dev to adjust the version number (from ``dev`` suffix to plain release) and build number (to 0).
#. Rebase the new branch on main.
   This may involve some merge conflict resolution.
   Don't forget to request rerendering.
   After successful checks and PR review, merge to main.
#. Wait for the new metapackage to be available in the conda-forge channel.
#. Create PRs to update the default versions in `lsst <https://github.com/lsst/lsst/blob/main/scripts/newinstall.sh>`__, `lsstsw <https://github.com/lsst/lsstsw/blob/main/etc/settings.cfg.sh>`__, and `jenkins-dm-jobs <https://github.com/lsst-dm/jenkins-dm-jobs/blob/main/etc/scipipe/build_matrix.yaml>`__.
   GitHub Actions tests of these PRs will not succeed if the metapackage is not available.
#. Test Jenkins with the ``stack-os-matrix`` job using the new rubin-env version on at least ``lsst_ci`` and ideally also ``ci_hsc`` and ``ci_imsim``.
#. Merge the lsst+lsstsw+jenkins-dm-jobs PRs and announce the update on community.lsst.org.

.. _conda-shared-stack:

Shared stack
------------

A shared Science Pipelines stack is maintained in the ``/software/lsstsw`` directory on the LDF development cluster.
This stack is accessible to all login, development/head/submit, and batch nodes.
It is maintained by a ``cron`` job (running under user ``lsstsw``) that executes a script from ``lsst-dm/shared-stack``.
This script automatically installs new weekly releases from source.
It also augments the standard ``rubin-env`` conda environment with additional packages useful for developers (but not needed in production) using the ``rubin-env-developer`` metapackage.
Requests for additions to ``rubin-env-developer`` should be made via RFC.

``rubin-env-developer`` versioning follows ``rubin-env``.
New builds of ``rubin-env`` can be used to update the packages that are in ``rubin-env-developer`` and not ``rubin-env``.

.. _conda-rsp-notebooks:

Rubin Science Platform notebooks
--------------------------------

Rubin Science Platform notebooks use a container that is built from each release.
As part of the container build process, additional packages useful in the notebook environment are added to the conda environment using the ``rubin-env-rsp`` metapackage.
``rubin-env-rsp`` differs from ``rubin-env-developer`` in being user-focused and including packages specific for the JupyterHub/JupyterLab platform.
Requests for additions to ``rubin-env-rsp`` should be made via RFC.

``rubin-env-rsp`` versioning follows ``rubin-env``.
New builds of ``rubin-env`` can be used to update the packages that are in ``rubin-env-rsp`` and not ``rubin-env``.

.. _conda-exact-environments:

"Exact" environments
--------------------

The conda environments used by Jenkins to build nightly, weekly, and official release tarballs are preserved as ``conda list --explicit`` outputs in ``eups.lsst.codes``.
These can be used in place of the ``rubin-env`` metapackage to exactly reproduce a build for consistency in production or for debugging.
Both ``newinstall`` and ``lsstsw`` allow specification of an eups tag to retrieve the exact environment used when that tag was published.
