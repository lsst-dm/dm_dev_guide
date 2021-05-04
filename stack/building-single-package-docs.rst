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

Finally, the documentation build uses Documenteer_ and related Sphinx_ documentation packages.
Documenteer_ is already installed if you are using the Rubin Conda environment (part of the usual Science Pipelines installation).
If this is not the case, see the `Documenteer installation documentation <https://documenteer.lsst.io/pipelines/install.html>`__.

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

Further reading
===============

- `Documentation for the package-docs command in Documenteer`_
- Alternative ways to build documentation:

   - :doc:`building-pipelines-lsst-io-locally`
   - :doc:`building-pipelines-lsst-io-with-documenteer-job`

.. _`Documenteer`: https://documenteer.lsst.io
.. _`Documenteer’s documentation for more information about the package-docs command`:
.. _`Documentation for the package-docs command in Documenteer`: https://documenteer.lsst.io/pipelines/package-docs-cli.html
.. _`Documenteer installation documentation`: https://documenteer.lsst.io/pipelines/install.html
.. _`pipelines.lsst.io`: https://pipelines.lsst.io
.. _`pipelines_lsst_io`: https://github.com/lsst/pipelines_lsst_io
.. _`pipe_base`: https://github.com/lsst/pipe_base
.. _`Sphinx`: https://www.sphinx-doc.org/en/master/
