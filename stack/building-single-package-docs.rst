.. _build-package-docs:

#############################################
Building single-package documentation locally
#############################################

While developing a package and its documentation, you’ll probably want to preview what the documentation looks like when built.
The quickest way to do this is with a single-package documentation build.

Keep in mind that a single-package documentation build may have many broken links because package documentation is *meant* to be built in the context of the package stack.
To do a full-stack documentation build, see either:

- :doc:`building-pipelines-lsst-io-locally`
- :doc:`building-pipelines-lsst-io-with-documenteer-job`

Nevertheless, a single-package build is useful for checking formatting and proof-reading your work.
This page describes how to run a single-package documentation build, using `pipe_base`_ as the example.

.. _build-package-docs-prereqs:

Prerequisites
=============

Before starting this tutorial, you’ll need a working ``lsst_distrib`` installation.
This installation should already be set up with a command like :command:`setup lsst_distrib`.

This installation needs to be a recent daily or weekly build since you’ll be compiling the `pipe_base`_ repository from its ``master`` branch.
Working from the tip of the ``master`` branch is the norm for LSST software development.

.. _build-package-docs-documenteer:

Install Documenteer, the documentation tooling
==============================================

Documenteer_ provides tooling to build `pipelines.lsst.io`_.
Since it’s a `PyPI-distributed Python package <https://pypi.org/project/documenteer/>`__, you need to install it separately from the EUPS Stack.
The best way to do this is in a Python virtual environment that’s layered on top of the EUPS Stack’s :file:`site-packages`.
This way it’s easy to delete Documenteer and its dependencies without affecting the Python packages that come with the EUPS Stack.

In a base working directory — not inside a repository directory — create the virtual environment and :command:`pip`-install Documenteer through the :file:`requirements.txt` file for `pipelines_lsst_io`_:

.. code-block:: bash

   python -m venv --system-site-packages --without-pip pyvenv
   source pyvenv/bin/activate
   curl https://bootstrap.pypa.io/get-pip.py | python
   curl -O https://raw.githubusercontent.com/lsst/pipelines_lsst_io/master/requirements.txt
   pyvenv/bin/pip install -r requirements.txt

.. note::

   By using the :file:`requirements.txt` file in the `pipelines_lsst_io`_ repository, you can ensure you’re using the same version of Documenteer_ and its dependencies as in the CI builds of `pipelines.lsst.io`_.

.. tip::

   When you open a new terminal session, you can reactivate the Python virtual environment in the :file:`pyvenv` directory by running:

   .. code-block:: bash

      source pyvenv/bin/activate

   Do this *after* setting up the EUPS Stack.

.. _build-package-docs-setup-package:

Downloading and setting up a package
====================================

You need to clone and build the package locally.
In this example, you’ll be cloning and building `pipe_base`_:

.. code-block:: bash

   git clone https://github.com/lsst/pipe_base
   cd pipe_base
   setup -k -r .
   scons

.. note::

   If you’re actively developing a package, it’s likely that you’ve already cloned and built that package.

.. _build-package-docs-build:

Building the package’s documentation
====================================

You can build the package’s documentation by running:

.. code-block:: bash

   package-docs build

The built HTML is located, relative to the :file:`pipe_base` directory, at :file:`doc/_build/html`.

.. note::

   The page at :file:`doc/_build/html/index.html` is the homepage for single-package builds.
   It never appears in the `pipelines.lsst.io`_ site build but does link to all the package and module documentation directories listed in the package's :ref:`doc/manifest.yaml file <docdir-manifest-yaml>`.

See `Documenteer’s documentation for more information about the package-docs command`_.

.. _build-package-docs-install-delete-build:

Deleting built documentation
============================

Since Sphinx only builds files that have changed, and may not notice updated docstrings, you may need to delete the built documentation to force a clean rebuild.
You can delete this built documentation by running:

.. code-block:: bash

   package-docs clean

.. _build-package-docs-cleanup:

Deactivating the virtual environment and cleaning up Documenteer
================================================================

When you’re done, you can always deactivate the :file:`pyvenv` virtual environment and even delete it.

To deactivate the virtual environment, run:

.. code-block:: bash

   deactivate

To fully delete the :file:`pyvenv` virtual environment, delete it:

.. code-block:: bash

   rm -r pyvenv

Further reading
===============

- `Documentation for the package-docs command in Documenteer`_
- Alternative ways to build documentation:

   - :doc:`building-pipelines-lsst-io-locally`
   - :doc:`building-pipelines-lsst-io-with-documenteer-job`

.. _`Documenteer`: https://documenteer.lsst.io
.. _`Documenteer’s documentation for more information about the package-docs command`:
.. _`Documentation for the package-docs command in Documenteer`: https://documenteer.lsst.io/pipelines/package-docs-cli.html
.. _`pipelines.lsst.io`: https://pipelines.lsst.io
.. _`pipelines_lsst_io`: https://github.com/lsst/pipelines_lsst_io
.. _`pipe_base`: https://github.com/lsst/pipe_base
