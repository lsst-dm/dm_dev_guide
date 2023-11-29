###################################
Making Your Package pip Installable
###################################

By default a Science Pipelines package will be configured to work with SCons and EUPS but not with ``pip``.
If the package does not include C++ code and does not depend on any of the C++ packages, such as ``afw`` or ``daf_base``, then it is possible to make the package installable with ``pip`` as well as with SCons.

You can discuss with your T/CAM or scientist whether a package should be modified to support building with ``pip``.

.. note::

  C++ packages can be built with ``pip`` but when packages are built this way they can't easily be used as dependencies for C++ code from other packages.
  The `lsst-sphgeom`_ PyPI package is a C++ package but can not be used to build ``afw`` because the include files and standalone shared library are not part of the installation.
  Only the Python interface is available.

Configuring the Package
=======================

All the configuration for a modern Python package lives in a file called ``pyproject.toml``.
There are a number of sections that need to be created for ``pip`` to work properly.

The Build Requirements
----------------------

.. code-block:: toml

  [build-system]
  requires = ["setuptools", "lsst-versions >= 1.3.0"]
  build-backend = "setuptools.build_meta"

This section tells ``pip`` what to install before the build process can even begin.
Usually you will find that a package will use ``setuptools_scm`` to determine the version number.
This doesn't really work for Science Pipeline packages since tags are applied by the pipeline's build procedure and can not be set by the individual package owner.
This means that semantic versions can't be used but it also means that if we want packages to be published on a cadence smaller than every 6 months we can not rely solely on the formal release tags to appear.

.. note::

  One way around the semantic versioning impasse with Science Pipelines tagging is to introduce a new tagging scheme for `PyPI`_ distribution and adjust the tags that are matched by the deployment algorithm.
  This would require modifications to `lsst-versions`_ to understand the new scheme and adding the ability to turn off versioning for weekly tags.
  If we are intending to upload the formal Science Pipelines release versions to `PyPI`_ the resulting version number must be higher than any Pipelines release number we expect to use in the future.
  If you wish to use semantic versioning for your package please discuss your options on ``#dm-arch`` on Slack before finalizing your approach.

The `lsst-versions`_ package is used to work around this restriction by determining version numbers based on the most recent formal version and the current weekly tag.
For example, in ``daf_butler`` the version that was uploaded to `PyPI`_ for tag ``w.2023.42`` was ``26.2023.4200`` (where v26 was the most recent formal release tag at the time).
The trailing ``00`` in the version number is used to allow different version numbers to be determined on ticket branches whilst developing the package between weekly tags and is the number of commits since the most recent weekly.

Project Metadata
----------------

The ``project`` section is used to specify the core metadata for the package.
For example, this is the content for the ``lsst-resources`` package:

.. code-block:: toml

    [project]
    name = "lsst-resources"
    description = "An abstraction layer for reading and writing from URI file resources."
    license = {text = "BSD 3-Clause License"}
    readme = "README.md"
    authors = [
        {name="Rubin Observatory Data Management", email="dm-admin@lists.lsst.org"},
    ]
    classifiers = [
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ]
    keywords = ["lsst"]
    dependencies = [
        "lsst-utils",
        "importlib_resources",
    ]
    dynamic = ["version"]
    requires-python = ">=3.11.0"

The Rubin DM convention is that Science Pipelines packages that are to be distributed on `PyPI`_ should include the ``lsst-`` prefix in the name.
This differs from the EUPS naming convention where the ``lsst`` is implicit.
For example, the ``daf_butler`` EUPS package has a python distribution name of ``lsst-daf-butler``.
Middleware packages use a dual license for distribution, with the `PyPI`_ package declaring the BSD 3-clause license.
Most Science Pipelines packages use the GPLv3 license and for those packages the ``pyproject.toml`` should use:

.. code-block:: toml

    license = {text = "GPLv3+ License"}
    classifiers = [
      "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
    ]

Every Rubin DM Science Pipelines package should be owned by the special DM account and that should always be included in the ``authors`` section.
Additional authors can be included if required.

The ``dependencies`` section can only refer to packages that are available on `PyPI`_ since this is the section that will be read during ``pip install``.
It should include all Python packages that would normally be included as part of the ``rubin-env`` Conda environment.

Do not include optional packages in this list or packages that are only needed to run the test code.
Instead, add a separate item like the following:

.. code-block:: toml

  [project.optional-dependencies]
  test = [
      "pytest >= 3.2",
      "numpy >= 1.17",
      "matplotlib >= 3.0.3",
      "pyarrow >= 0.16",
      "pandas >= 1.0",
  ]

These optional packages would be installed automatically if ``pip`` is called with:

.. code-block:: bash

  $ pip install lsst-yourpackage[test]


Setuptools Configuration
------------------------

For ``setuptools`` builds, the usual default build system for our packages, additional configuration is needed so that the python files and data files can be located.
For example, in ``daf_butler`` there is this configuration:

.. code-block:: toml

    [tool.setuptools.packages.find]
    where = ["python"]

    [tool.setuptools]
    zip-safe = true
    license-files = ["COPYRIGHT", "LICENSE", "bsd_license.txt", "gpl-v3.0.txt"]

    [tool.setuptools.package-data]
    "lsst.daf.butler" = ["py.typed", "configs/*.yaml", "configs/*/*.yaml"]

    [tool.setuptools.dynamic]
    version = { attr = "lsst_versions.get_lsst_version" }

This tells ``setuptools`` that the python files are in a ``python/`` directory and what additional non-python files should be included in the distribution.

The license-files section should reflect the specific needs of your package.

When making a `PyPI`_ distribution, the package should work without relying on the EUPS ``$PACKAGE_DIR`` variable being set.
This means that any supplementary data such as those that would go in a ``config/`` or ``policy/`` directory should instead be included inside the ``python/`` directory and be accessed using the standard package resources APIs (such as `importlib.resources` or ``lsst.resources.ResourcePath``).
These files must then be listed explicitly in the ``package-data`` section of the configuration file, as can be shown in the above example.

.. warning::

  Currently ``pex_config`` does not understand how to read a config from a package using package resources.
  If configs are to be read they can not be read using the usual ``lsst.utils.getPackageDir`` API and must instead use `importlib.resources` APIs directly.
  We are planning to make this simpler by adding native support into ``pex_config``.

Using GitHub Actions
====================

If a package is pip-installable it is likely that you will want to build the package in a GitHub action and run the associated tests.
If your package depends on other Science Pipelines packages you will want to install those directly from GitHub from the ``main`` branch since there is no guarantee that `PyPI`_ will have the right version.
The easiest way to do this is to write a ``requirements.txt`` file which has the direct dependencies that should be installed by the build script.
This file is a simple text file listing packages and versions, and will likely duplicate information found in the ``pyproject.toml`` file.

For example, the ``requirements.txt`` in the ``daf_relation`` package looks like:

.. code-block::

  git+https://github.com/lsst/utils@main#egg=lsst-utils
  sqlalchemy >= 1.4

The first line tells ``pip`` to install the dependency directly from GitHub.
The second line is a standard `PyPI`_ dependency.
These can be installed by running:

.. code-block:: bash

  $ pip install -r requirements.txt

and then the package can be installed with:

.. code-block:: bash

  $ pip install --no-deps .

Where this will skip the dependency check and install the package directly.
When developing multiple packages at the same time it is possible to change the ``requirements.txt`` file to point at a specific ticket branch rather than ``main``.
There are checkers available that can block merging if such a change has been made; an example can be found in the ``daf_butler`` repository named `do_not_merge.yaml`_.

If you want the version number of the build to be determined correctly the code must be checked out on GitHub with the full history included:

.. code-block:: yaml

    steps:
      - uses: actions/checkout@v3
        with:
          # Need to clone everything for the git tags.
          fetch-depth: 0

Once a package is pip-installable the package can be tested in the GitHub action.
If ``pytest`` is configured with code coverage enabled the results can be uploaded to CodeCov and reported on the pull request.
This would look something like:

.. code-block:: yaml

    - name: Build and install
      run: |
        python -m pip install --no-deps -v -e .

    - name: Run tests
      run: |
        pytest -r a -v -n 3 --open-files --cov=lsst.resources\
                --cov=tests --cov-report=xml --cov-report=term --cov-branch

    - name: Upload coverage to codecov
      uses: codecov/codecov-action@v2
      with:
        file: ./coverage.xml



Distributing the Package on PyPI
================================

Once the package supports ``pip install`` it is a small configuration change to allow it to be distributed on `PyPI`_.
One caveat is that all the required dependencies listed in the ``pyproject.toml`` file must exist on `PyPI`_.

The recommended process is for a GitHub action to trigger when the package is tagged.
This action will then build the package and trigger the upload to `PyPI`_.
All Science Pipeline packages on `PyPI`_ must be owned by the Rubin DM `PyPI`_ account attached to ``dm-admin@lists.lsst.org``.

The `PyPI`_ upload can be configured in the same GitHub action that builds the package and tests it.
Usually it will block on the successful completion of that phase and then only trigger if a tag is being added.

A full example can be seen below:

.. code-block:: yaml

  pypi:

    runs-on: ubuntu-latest
    needs: [build_and_test]
    if: startsWith(github.ref, 'refs/tags/')
    permissions:
      id-token: write

    steps:
      - uses: actions/checkout@v3
        with:
          # Need to clone everything to embed the version.
          fetch-depth: 0

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: "3.11"

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install --upgrade setuptools wheel build

      - name: Build and create distribution
        run: |
          python -m build --skip-dependency-check

      - name: Upload
        uses: pypa/gh-action-pypi-publish@release/v1

For the upload to work `PyPI`_ must be preconfigured to expect uploads from this specific GitHub action using a `trusted publisher`_ mechanism.
When you get to this part of the process please ask for help on ``#dm-arch`` on Slack.

.. _PyPI: https://pypi.org
.. _lsst-sphgeom: https://pypi.org/project/lsst-sphgeom/
.. _lsst-versions: https://pypi.org/project/lsst-versions/
.. _trusted publisher: https://docs.pypi.org/trusted-publishers/
.. _do_not_merge.yaml: https://github.com/lsst/daf_butler/blob/main/.github/workflows/do_not_merge.yaml
