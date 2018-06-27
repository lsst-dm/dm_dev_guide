.. _local-pipelines-lsst-io-build:

###########################################
Building the pipelines.lsst.io site locally
###########################################

You can build the full `pipelines.lsst.io`_ site on your own computer.
Although this is slightly more complicated than :doc:`building documentation for a single package <building-single-package-docs>`, it’s the best way to ensure that cross-package links work properly.

Alternatively, you can also build and publish a development version of `pipelines.lsst.io`_ with the `sqre/infrastructure/documenteer`_ Jenkins CI job.
That Jenkins job only accepts development branches of the `pipelines_lsst_io`_ repository --- not development branches of packages.
The method described on this page is currently the only way to build documentation for development branches of packages with the full LSST Science Pipelines stack.

.. _local-pipelines-lsst-io-build-prereqs:

Prerequisites
=============

Before starting, you’ll need a working ``lsst_distrib`` installation.

This installation needs to be a recent daily or weekly build so that any in-development packages will compile with the Stack. Working from the tip of the ``master`` branch is the norm for LSST software development.

.. _local-pipelines-lsst-io-build-clone:

Clone and set up the pipelines\_lsst\_io repository
===================================================

`pipelines_lsst_io`_ is the main documentation repository for the `pipelines.lsst.io`_ site.
It contains project-wide content, like installation guides and release notes, and also provides the structure for gathering documentation content from individual packages in the LSST Science Pipelines package stack.

Clone the repository:

.. code-block:: bash

   git clone https://github.com/lsst/pipelines_lsst_io

.. important::

   During this initial phase, ``tickets/DM-11216`` is the integration branch for multi-package builds of `pipelines_lsst_io`_.
   For now you need to check out that branch:

   .. code-block:: bash

      cd pipelines_lsst_io
      git checkout tickets/DM-11216
      cd ..

Then set up the `pipelines_lsst_io`_ package with EUPS:

.. code:: bash

   setup -r pipelines_lsst_io

.. warning::

   If you’ve already set up packages, you might need to unset-up them before setting up ``pipelines_lsst_io``.

   `pipelines_lsst_io`_ acts as a top-level EUPS package, and its table file defines what packages are included in the `pipelines.lsst.io`_ documentation site.

.. _local-pipelines-lsst-io-build-documenteer:

Install Documenteer, the documentation tooling
==============================================

Documenteer_ provides tooling to build `pipelines.lsst.io`_.
Since it’s a `PyPI-distributed Python package <https://pypi.org/project/documenteer/>`__, you need to install it separately from the EUPS Stack.
The best way to do this is in a Python virtual environment that’s layered on top of the EUPS Stack’s ``site-packages``.
This way it’s easy to delete Documenteer_ and its dependencies without affecting the Python packages that come with the EUPS Stack.

In the base working directory (that also contains the :file:`pipelines_lsst_io` clone), create the virtual environment and :command:`pip`-install Documenteer_ through the :file:`requirements.txt` file for `pipelines_lsst_io`_:

.. code-block:: bash

   python -m venv --system-site-packages --without-pip pyvenv
   source pyvenv/bin/activate
   curl https://bootstrap.pypa.io/get-pip.py | python
   pyvenv/bin/pip install -r pipelines_lsst_io/requirements.txt

.. note::

   By using the :file:`requirements.txt` file in the `pipelines_lsst_io`_ repository, you can ensure you’re using the same version of Documenteer_ and its dependencies as in the CI builds of `pipelines.lsst.io`_.

.. tip:: When you open a new terminal session, you can reactivate the Python virtual environment in the :file:`pyvenv` directory by running:

   .. code-block:: bash

      source pyvenv/bin/activate

Do this *after* setting up the EUPS Stack.

.. _local-pipelines-lsst-io-build-build:

Building the pipelines\_lsst\_io site
=====================================

Move into the :file:`pipelines_lsst_io` directory:

.. code-block:: bash

   cd pipelines_lsst_io

Then use the `stack-docs command-line app`_ from Documenteer_ to build the documentation:

.. code-block:: bash

   stack-docs build

The built site is located in the :file:`_build/html` directory.

.. _local-pipelines-lsst-io-build-clean:

Cleaning up built documentation
===============================

You can clean up the built documentation and intermediate artifacts by running:

.. code-block:: bash

   stack-docs clean

Cleaning up the build is useful if you need to force a rebuild of the documentation either because a previous build failed, or a docstring changed.
Sphinx does not automatically invalidate its cache when docstrings change.

.. _local-pipelines-lsst-io-build-package-setup:

Adding a locally-developed package to the pipelines_lsst\_io build
==================================================================

The `pipelines_lsst_io`_ build works by symlinking the :doc:`doc/ directory <layout-of-doc-directory>` contents of packages that are set up by EUPS.
This means that by setting up a package, you can add it to your local `pipelines_lsst_io`_ build.

For this tutorial, you’ll use the `pipe_base`_ package as an example.

First, move out of the :file:`pipelines_lsst_io` directory and clone `pipe_base`_:

.. code-block:: bash

   cd ..
   git clone https://github.com/lsst/pipe_base

Then set up and compile `pipe_base`_, while keeping other packages set up (the ``-k`` option):

.. code-block:: bash

   cd pipe_base
   setup -k -r .
   scons

Then clean and build the `pipelines_lsst_io`_ documentation:

.. code-block:: bash

   stack-docs -d ../pipelines_lsst_io clean
   stack-docs -d ../pipelines_lsst_io build

.. _local-pipelines-lsst-io-build-package-deactivate:

Deactivating the virtual environment and cleaning up Documenteer
================================================================

When you’re done, you can always deactivate the :file:`pyvenv` virtual environment and even delete it.

To deactivate the virtual environment, run:

.. code-block:: bash

   deactivate

To fully delete the :file:`pyvenv` virtual environment, change to the directory containing :file:`pyvenv` and delete it:

.. code-block:: bash

   rm -r pyvenv

Further reading
===============

- `Documentation for the stack-docs command in Documenteer`_
- Alternative ways to build documentation:

   - :doc:`building-single-package-docs`
   - Building pipelines.lsst.io with Jenkins CI

.. _`Documenteer`: https://documenteer.lsst.io/v/DM-14852/
.. _`Documentation for the stack-docs command in Documenteer`:
.. _`stack-docs command-line app`: https://documenteer.lsst.io/v/DM-14852/pipelines/stack-docs-cli.html
.. _`sqre/infrastructure/documenteer`: https://ci.lsst.codes/blue/organizations/jenkins/sqre%2Finfrastructure%2Fdocumenteer/activity
.. _`pipelines.lsst.io`: https://pipelines.lsst.io
.. _`pipelines_lsst_io`: https://github.com/lsst/pipelines_lsst_io
.. _`pipe_base`: https://github.com/lsst/pipe_base
