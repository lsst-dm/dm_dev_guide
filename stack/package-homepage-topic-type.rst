.. _package-homepage:

###########################
Package homepage topic type
###########################

The package homepage is the :file:`index.rst` file located at the root of each :ref:`package documentation directory <docdir-package-doc-directory>`.
The purpose of the package homepage is to provide summary information about a package and a table of contents for additional topics in the package documentation directory.

.. _package-homepage-template:

Starter template
================

The `stack_package`_ project template includes the `Jinja-formatted template for the package homepage <https://raw.githubusercontent.com/lsst/templates/master/project_templates/stack_package/%7B%7Bcookiecutter.package_name%7D%7D/doc/%7B%7Bcookiecutter.package_name%7D%7D/index.rst>`_.

For an example package named ``example``, the rendered template looks like this:

.. remote-code-block:: https://raw.githubusercontent.com/lsst/templates/master/project_templates/stack_package/example_dataonly/doc/example_dataonly/index.rst
   :language: rst

The next sections describe the key components of the package homepage.

.. _package-homepage-filename:

File name and location
======================

This file must be named :file:`index.rst` and must be located in a :ref:`package documentation directory <docdir-package-doc-directory>` within a package.
For example, if the package’s name is ``example``, the full path for the file is :file:`doc/example/index.rst`.

.. _package-homepage-title:

Title
=====

The title (top-level header) of the package homepage is the packages’s name, without any special formatting (like code literals).

.. note::

   In the future we might include a brief descriptive phrase after the package’s name.
   There is no guidance to add this descriptive phrase at this time.

The cross-reference target above the title must be name of the package followed by a ``-package`` suffix (see the example from the :ref:`starter template <package-homepage-template>`).

.. _package-homepage-context:

Context paragraph
=================

Directly after the title, include one or two paragraphs that describe what the package is for.
The purpose of this content is not to describe the package in detail, or how to use it, but instead to quickly orient a reader.

You can also mention related packages:

.. code-block:: rst

   Definitions of metrics and their specifications are provided separately in the :doc:`/packages/verify_metrics/index` package.

If a package provides datasets (such as a test data repository), you can summarize what these datasets are for, and what APIs use those datasets.

.. _package-homepage-project-using:

Using <package> section
=======================

If the package documentation directory includes additional topics, in separate reStructuredText files, you should link to them in this section using a `toctree`_ directive.
For example, given a package named ``example`` with files :file:`doc/example/topic-a.rst` and :file:`doc/example/topic-b.rst`, the “Using” section should be presented like this:

.. code-block:: rst

   Using example
   =============

   .. toctree::
      :maxdepth: 1

      topic-a
      topic-b

Each of these other reStructuredText files should follow the :doc:`Generic guide topic type <generic-guide-topic-type>`.

.. _package-homepage-contributing:

Contributing section
====================

This section puts the package in context as an open source development project.
The `template <package-homepage-template>` seeds this section with links to the GitHub repository for the package and a ticket search with the package's corresponding Jira component (if the package does not have a Jira component, request one in `#dm-square`_).

If there is documentation describing how to develop (contribute) to the package, as opposed to using the package, you should link to those topics with a `toctree`_ in this section.

.. _stack_package: https://github.com/lsst/templates/tree/master/project_templates/stack_package
.. _toctree: http://www.sphinx-doc.org/en/master/usage/restructuredtext/directives.html#directive-toctree
.. _`#dm-square`: https://lsstc.slack.com/archives/dm-docs
