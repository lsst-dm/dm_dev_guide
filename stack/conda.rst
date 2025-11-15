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

.. _rubin-env-switching-versions:

Switching rubin-env versions
----------------------------

Occasionally, you may need to switch the version of ``rubin-env`` you are using.
Below, you'll find instructions on how to view available versions and switch between them.
You can view the current available env versions `on conda-forge <https://anaconda.org/conda-forge/rubin-env/files>`__.
To see all available ``rubin-env`` in your terminal run the following:

.. code-block:: bash

   conda search -c nodefaults  -c conda-forge rubin-env

This command will print out only production ready ``rubin-env`` versions.
It's best to start from a fresh shell when running bin/deploy to avoid confusion.
To change the ``rubin-env``:

.. code-block:: bash

   conda deactivate # make sure you do not run this inside an existing conda environment
   ./bin/deploy -v 12.0.0 # or any other rubin env
   source bin/envconfig -n lsst-scipipe-12.0.0
   rebuild lsst_apps # This could be any branch or product you want to use


.. _rubin-env-dev-switching-versions:

Using developer rubin-env environments
--------------------------------------

You might also want to switch to ``rubin-env`` versions that are still under development.
To do so, add the label ``conda-forge/label/rubin-env_dev`` as follows:

.. code-block:: bash

   conda search -c nodefaults  -c conda-forge rubin-env -c conda-forge/label/rubin-env_dev

This command will print out all available ``rubin-env`` including ones that are still under development (``rubin-env_dev``).
Again, start from a fresh shell for each bin/deploy to avoid confusion.
To change the ``rubin-env``:

.. code-block:: bash

   conda deactivate # make sure you do not run this inside an existing conda environment
   # adding conda-forge/label/rubin-env_dev allows to install rubin-env_dev
   export LSST_CONDA_CHANNELS="nodefaults conda-forge/label/rubin-env_dev conda-forge"
   ./bin/deploy -v 12.0.0dev # or any other rubin env
   source bin/envconfig -n lsst-scipipe-12.0.0dev
   rebuild lsst_apps # This could be any branch or product you want to use

.. _rubin-env-dependency-versioning:

Dependency versions
-------------------

The package specifications that define ``rubin-env`` typically specify minimum versions.
These provide guarantees so that Science Pipelines developers can rely on features of the packages in their code.
Features newer than the minimum versions for the environment, or for packages that are not directly listed dependencies, should not be relied on.

The use of minimum and not exact versions is intentional so that users can add packages on top of ``rubin-env`` with a minimum of conflicts.
Otherwise, it would frequently be the case that the version requirements of a desired package would conflict with those of ``rubin-env``, preventing both from being present in the same environment.
The main exceptions that have strict constraints are packages that include shared libraries that Science Pipelines C++ code links against which must be constrained for binary compatibility.

The lax constraints naturally mean that different installations of ``rubin-env`` performed at different times may include different dependency versions.
Generally these will be compatible and should cause no difficulty.
If necessary to debug a problem, an "exact" environment that contains the exact versions that were used during the Science Pipelines release process can be installed using ``lsstinstall -X {release tag}``.

On occasion, a change in a dependency will break Rubin code.
This cost is accepted to allow the benefit of combining ``rubin-env`` with other packages.
The breakage is typically detected in the Jenkins nightly "clean" builds that reinstall the conda environment from scratch.
The problem is resolved in three phases:

- The dependency version is pinned to be less than the failing version in a new build of the current release of ``rubin-env``, and a notation is made in the `DM Third Party Software Confluence page <https://confluence.lsstcorp.org/display/DM/DM+Third+Party+Software>`__.  This solves the immediate problem.
- At a later date, the relevant Science Pipelines code is modified to be compatible with both the older and newer versions of the dependency.  This makes the pin eligible for release, which is marked on the Confluence page.
- In the next major rubin-env release, the version constraint is removed.

If the dependency change is generally acknowledged to be a bug and is rapidly fixed upstream, a ``!=`` version constraint can be used without releasing a new version of ``rubin-env``.

If a dependency frequently breaks Rubin code when it is updated, its version can be constrained at increasingly stringent levels (e.g. major version, minor version, or even specific patch version).

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

.. _rubin-env-updating:

Updating ``rubin-env``
----------------------

When updating rubin-env, the following procedure should be followed:

#. Experiment with changes by building and testing the Science Pipelines stack using lsstsw with a custom conda environment.
   This should turn up problems with dependency conflicts or with Pipelines code (such as use of deprecated, now-gone interfaces).
   Fix these (or give up on the problematic rubin-env change for now).
#. Modify the ``dev`` branch in ``rubinenv-feedstock`` to match the custom experimental environment, including any new dependencies, removing any unneeded dependencies, and updating versions of existing dependencies.
   Ensure that it solves and builds on all platforms.
   Add selectors to ``rubin-env-extras`` (e.g. to express conditions based on particular platforms or Python versions) or version pins to ``rubin-env`` if necessary to allow building.
#. Test the current Science Pipelines stack using the ``dev`` environment (install using the ``conda-forge/label/rubin-env_dev`` channel).
#. Test pip installation of `RSP dependencies <https://github.com/lsst-sqre/sciplat-lab/blob/main/stage3-py.sh>`__ into the ``dev`` environment.
#. Create a ticket branch from ``dev`` to adjust the version number (from ``dev`` suffix to plain release) and build number (to 0).
#. Rebase the new branch on main.
   This may involve some merge conflict resolution.
   Don't forget to request rerendering.
   After successful checks and PR review, merge to ``main``.
#. Wait for the new metapackage to be available in the conda-forge channel.
#. Test Jenkins with the ``stack-os-matrix`` job using the new rubin-env version (by specifying an explicit ``SPLENV_REF`` parameter) on at least ``lsst_ci`` and ideally all the ``ci_*`` products (``ci_cpp``, ``ci_hsc``, ``ci_imsim``, and ``ci_middleware``).
#. In parallel, create PRs to update the default versions in `lsst <https://github.com/lsst/lsst/blob/main/scripts/newinstall.sh>`__, `lsstsw <https://github.com/lsst/lsstsw/blob/main/etc/settings.cfg.sh>`__, and `jenkins-dm-jobs <https://github.com/lsst-dm/jenkins-dm-jobs/blob/main/etc/scipipe/build_matrix.yaml>`__.
   Ensure that all GitHub Actions tests pass; they will not if the metapackage is not available.
#. Merge the lsst+lsstsw+jenkins-dm-jobs PRs and announce the update on community.lsst.org.
#. Merge the ``main`` branch into the ``dev`` branch to allow it to start the next update cycle with the latest definitions.

.. _conda-shared-stack:

Shared stack
------------

A shared Science Pipelines stack is maintained in the ``/software/lsstsw`` directory on the LDF development cluster.
This stack is accessible to all login, development/head/submit, and batch nodes.
It is maintained by a ``cron`` job (running under user ``lsstsw``) that executes a script from ``lsst-dm/shared-stack``.
This script automatically installs new weekly releases from source.
It also augments the standard ``rubin-env`` conda environment with additional packages useful for developers (but not needed in production) using the ``rubin-env-developer`` metapackage.
Requests for additions to ``rubin-env-developer`` should be made via RFC.

``rubin-env-developer`` currently uses the same version number as the underlying ``rubin-env``.
New builds of ``rubin-env`` (without updating its version) can generally be used to update the packages that are in ``rubin-env-developer`` and not ``rubin-env``.
If a new or updated ``rubin-env-developer`` package somehow breaks compatibility with old versions of Science Pipelines code, then a new version of ``rubin-env`` itself may be necessary.

.. _conda-rsp-notebooks:

Rubin Science Platform notebooks
--------------------------------

Rubin Science Platform notebooks use a container that is built from each release.
As part of the container build process, additional packages useful in the notebook environment are added to the conda environment using the ``rubin-env-rsp`` metapackage.
``rubin-env-rsp`` differs from ``rubin-env-developer`` in being user-focused and including packages specific for the JupyterHub/JupyterLab platform.
Requests for additions to ``rubin-env-rsp`` should be made via RFC.

``rubin-env-rsp`` currently uses the same version number as the underlying ``rubin-env``.
New builds of ``rubin-env`` (without updating its version) can always be used to update the packages that are in ``rubin-env-rsp`` and not ``rubin-env``.

.. _conda-exact-environments:

"Exact" environments
--------------------

The conda environments used by Jenkins to build nightly, weekly, and official release tarballs are preserved as ``conda list --explicit`` outputs in ``eups.lsst.cloud``.
These can be used in place of the ``rubin-env`` metapackage to exactly reproduce a build for consistency in production or for debugging.
Both ``newinstall`` and ``lsstsw`` allow specification of an eups tag to retrieve the exact environment used when that tag was published.
