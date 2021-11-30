.. _docdir:

############################
Layout of the doc/ directory
############################

This page describes the layout of :file:`doc/` directories in packages.
By following these guidelines, the documentation content of individual packages can successfully integrate with the build of `pipelines.lsst.io`_.

.. _docdir-template:

The stack_package template
==========================

Use the `stack_package template`_, and its examples, as references for implementing the :file:`doc/` directory of your package.
This page will refer to those templates frequently.

The :file:`doc/` directory structure of the example package looks like this:

.. code-block:: text

   doc
   ├── SConscript
   ├── conf.py
   ├── doxygen.conf.in
   ├── index.rst
   ├── lsst.example
   │   ├── index.rst
   │   │── scripts
   │   └── tasks
   └── manifest.yaml

.. _docdir-manifest-yaml:

The doc/manifest.yaml file
==========================

This YAML file describes the content of the package’s :file:`doc/` directory.
The build process uses the :file:`doc/manifest.yaml` file to symlink documentation content from packages into the :ref:`main documentation repository <stack-docs-system-main-repo>`, `pipelines_lsst_io`_.

The :file:`doc/manifest.yaml` file for a package named `example`_ looks like this:

.. remote-code-block:: https://raw.githubusercontent.com/lsst/templates/main/project_templates/stack_package/example/doc/manifest.yaml
   :language: yaml

.. _docdir-manifest-yaml-modules:

modules field
-------------

The ``modules`` field is a **list** of the public Python modules that the package provides.
For most packages, as is the case for the example above, the package provides just one public Python module (``lsst.example``, for example).

Each item in the ``modules`` list corresponds to a :ref:`module documentation directory <docdir-module-doc-directories>`.

.. note::

   “Modules” here means the major public modules provided by a package, created by  an :file:`__init__.py` files.
   Most packages provide just one major namespace that a Python user can import.

   For example, the ``log`` package provides the ``lsst.log`` namespace.

Some packages provides several major public modules.
For example, the ``afw`` package provides ``lsst.afw.cameraGeom``, ``lsst.afw.coord``, ``lsst.afw.detection``, and so on.
The ``lsst.afw`` module, on its own, isn’t used.
For example, ``afw``\ ’s :file:`manifest.yaml` file looks like this:

.. remote-code-block:: https://raw.githubusercontent.com/lsst/afw/main/doc/manifest.yaml
   :language: yaml

.. _docdir-manifest-yaml-statics:

statics field
-------------

The ``statics`` field lists any :file:`_static` directories included in the package’s ``doc/`` directory.
:file:`_static` directories are a place to include content that’s shipped with the HTML site, but are otherwise unprocessed by Sphinx.

Packages don’t need ``_static`` directories, so this field can be commented out.

.. _docdir-manifest-yaml-package:

package field
-------------

Some packages don't provide Python modules, and thus don't have :ref:`module documentation directories <docdir-module-doc-directories>`.
Instead, these packages are documented with a single :ref:`package documentation directory <docdir-package-doc-directory>`.

To declare a package documentation directory, add a ``package`` field to :file:`manifest.yaml`.
The ``package`` field must match the package’s EUPS name, which also corresponds to the name of the :ref:`package documentation directory <docdir-package-doc-directory>`.

This is an example :file:`manifest.yaml` for the `example_dataonly`_ package:

.. remote-code-block:: https://raw.githubusercontent.com/lsst/templates/main/project_templates/stack_package/example_dataonly/doc/manifest.yaml
   :language: yaml

.. _docdir-conf:

The doc/conf.py file
====================

The :file:`doc/conf.py` file provides Sphinx configurations during a :doc:`single-package build <building-single-package-docs>`.
The :file:`doc/conf.py` file should look like this example:

.. remote-code-block:: https://raw.githubusercontent.com/lsst/templates/main/project_templates/stack_package/example/doc/conf.py
   :language: py

Fill in the ``project_name`` and ``version`` keyword arguments as appropriate.

Be careful not to add customizations to this :file:`conf.py` file since they won’t be used during the build of `pipelines.lsst.io`_ (only the :file:`conf.py` of the `pipelines_lsst_io`_ package is used in that case).

.. _docdir-gitignore:

The doc/.gitignore file
=======================

The :file:`doc/.gitignore` file ensures that documentation build products don’t get accidentally checked into the package’s Git repository.
The file looks like this:

.. remote-code-block:: https://raw.githubusercontent.com/lsst/templates/main/project_templates/stack_package/example/doc/.gitignore

.. _docdir-index:

The doc/index.rst file
======================

The :file:`doc/index.rst` file is the **development homepage** for the package.
This page doesn’t appear in `pipelines.lsst.io`_.
Instead, it’s a temporary stand-in for `pipelines_lsst_io`_\ ’s :file:`index.rst` file during :doc:`single-package documentation builds <building-single-package-docs>` that links to the package and module homepages described in :ref:`doc/manifest.yaml <docdir-manifest-yaml-package>`.

The :file:`doc/index.rst` file for an example package looks like this:

.. remote-code-block:: https://raw.githubusercontent.com/lsst/templates/main/project_templates/stack_package/example/doc/index.rst
   :language: rst

Customize the title and the entries in the ``toctree`` directive for your own package.

.. _docdir-doxygen-conf:

The doc/doxygen.conf.in file
============================

If your package has C++ code, it needs to have Doxygen run on it.
Add this *empty* file called :file:`doc/doxygen.conf.in`.

.. _docdir-sconscript:

The doc/SConscript file
=======================

If your package has C++ code, it needs to have Doxygen run on it.
Add this standardized :file:`doc/SConcript` file:

.. remote-code-block:: https://raw.githubusercontent.com/lsst/templates/main/project_templates/stack_package/example/doc/SConscript

.. _docdir-module-doc-directories:

Module documentation directories
================================

:file:`doc/` directories contain a module documentation directory for each major public Python namespace provided by the package.
These directories correspond to the modules listed in the :ref:`modules field <docdir-manifest-yaml-modules>` in the :ref:`manifest.yaml file <docdir-manifest-yaml>`.
Each module documentation directory provides a place to document the corresponding Python and C++ APIs.

The :file:`index.rst` file contained in this directory follows the :doc:`module topic type <module-homepage-topic-type>`.

There are two standard **subdirectories** that a module documentation directory may have:

:file:`tasks/`
    For :doc:`task <task-topic-type>` and :doc:`config <config-topic-type>` topic pages.

:file:`scripts/`
    For :doc:`script topic <script-topic-type>` (or :doc:`argparse-script-topic-type`) pages.

.. _docdir-package-doc-directory:

Package documentation directory
===============================

This directory is only present for packages that **do not** have :ref:`module documentation directories <docdir-module-doc-directories>`.
In such cases, the package documentation directory provides a place to document the EUPS package itself.
The :file:`index.rst` file in this directory (see :doc:`package-homepage-topic-type`) provides links to the package’s GitHub repo and Jira component, for example.

The package documentation directory is a subdirectory of :file:`doc/` that is named after the EUPS package itself.
For the package called ``example_dataonly``, this directory is :file:`doc/example_dataonly`.
This directory corresponds to the :ref:`package field <docdir-manifest-yaml-package>` in the :ref:`doc/manifest.yaml file <docdir-manifest-yaml>`.

For a full example, see the `example_dataonly`_ example of the stack\_package template.

**Remember, most packages will not have a package documentation directory.**

.. _docdir-static-directory:

\_static/ directory
===================

The “static” directory is a place to put files that are included in the HTML deployment, but are not otherwise processed by Sphinx.
Most packages don’t need the static directory at all.
Static files, like PDFs and small data files, can just be included alongside the ``rst`` files in the module and package documentation directories.

.. note::

   In early development, the :file:`doc/_static` directory was required.
   This is no longer the case.

If a package does need a static directory, any content should be put in a subdirectory of ``doc/_static`` that is named after the package.
For example, if the package name is ``afw``, the static directory should be :file:`doc/_static/afw`.
At build time, it’s the :file:`doc/_static/afw` directory that will be linked into the :ref:`main documentation repository <stack-docs-system-main-repo>`.

When linking to content in the :file:`_static` directory, use an absolute URL, starting with ``/``.
For example:

.. code-block:: rst

   :download:`/_static/afw/document.pdf`

.. _pipelines.lsst.io: https://pipelines.lsst.io
.. _`stack_package template`: https://github.com/lsst/templates/tree/main/project_templates/stack_package
.. _`pipelines_lsst_io`: https://github.com/lsst/pipelines_lsst_io
.. _`example`: https://github.com/lsst/templates/tree/main/project_templates/stack_package/example
.. _`example_dataonly`: https://github.com/lsst/templates/tree/main/project_templates/stack_package/example_dataonly
