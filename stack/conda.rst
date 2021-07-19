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

``rubin-env`` is intended to be the minimal set of dependencies required to build and execute all packages of ``lsst_distrib`` in production.
It does not necessarily include dependencies useful for developers to modify existing packages or add new packages.
It also does not necessarily include dependencies useful for science users to analyze, visualize, or otherwise work with raw Science Pipelines inputs or output data products.

In the future, an expanded ``rubin-env-plus`` may be created that would include additional dependencies for convenience and to ensure that compatible versions of all packages can be determined.
``rubin-env`` would then become a subset of this environment.

Requests for additions to ``rubin-env`` should be made via RFC.
The DM-CCB must approve such requests.

.. _rubin-env-versioning:

Versioning ``rubin-env``
------------------------

``rubin-env`` has a standard semantic version number with major, minor, and patch components, in addition to a conda-internal build number.
These components are updated as follows:

* Build: increment when adding a ``<`` pin for an existing dependency, as this preserves compatibility with previous builds of the environment.
* Patch: increment when adding a ``>`` pin for an existing dependency that is compatible with old code (no major version update) or when adding a ``<`` pin that is earlier than the previous pin.
* Minor: increment when adding a new dependency.
* Major: increment when removing a dependency, or when removing a pin, or when changing a dependency major version

.. _conda-shared-stack:

Shared stack
------------

A shared Science Pipelines stack is maintained in the ``/software/lsstsw`` directory on the LDF development cluster.
This stack is accessible to all login, development/head/submit, and batch nodes.
It is maintained by a ``cron`` job (running under user ``lsstsw``) that executes a script from ``lsst-dm/shared-stack``.
This script automatically installs new weekly releases from source.
It also augments the standard ``rubin-env`` conda environment with additional packages useful for developers (but not needed in production).
Requests for additions to this list should be made via RFC.

.. _conda-rsp-notebooks:

Rubin Science Platform notebooks
--------------------------------

Rubin Science Platform notebooks use a container that is built from each release.
As part of the container build process, additional packages useful in the notebook environment are added to the conda environment.
The list of packages is maintained in ``lsst-sqre/nublado2``; requests for additions to this list should be made via RFC.

.. _conda-exact-environments:

"Exact" environments
--------------------

The conda environments used by Jenkins to build nightly, weekly, and official releases are preserved as ``conda list --explicit`` outputs in ``eups.lsst.codes``.
These can be used in place of the ``rubin-env`` metapackage to exactly reproduce a build for consistency in production or for debugging.
Both ``newinstall`` and ``lsstsw`` allow specification of an eups tag to retrieve the exact environment used when that tag was published.
