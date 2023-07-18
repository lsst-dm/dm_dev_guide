.. _module-homepage:

##########################
Module homepage topic type
##########################

The module homepage is the :file:`index.rst` file located at the root of each :ref:`module documentation directory <docdir-module-doc-directories>` in a package.
The purpose of the module homepage is to serve as an index for all documentation related to a Python and C++ module namespace.
The module homepage links to guides and tutorials (see :doc:`generic-guide-topic-type`), :doc:`task topic pages <task-topic-type>`, and the Python and C++ API reference pages.

The module homepage is linked from the “Python API reference” section of the `pipelines.lsst.io`_ homepage (automatically, using the ``package-toctree`` directive).

.. _module-homepage-template:

Starter template
================

The `stack_package`_ project template includes the `Jinja-formatted template for the module homepage <https://raw.githubusercontent.com/lsst/templates/main/project_templates/stack_package/%7B%7Bcookiecutter.package_name%7D%7D/doc/%7B%7Bcookiecutter.python_module%7D%7D/index.rst>`__.

For an example module named ``lsst.example``, the rendered template looks like this:

.. remote-code-block:: https://raw.githubusercontent.com/lsst/templates/main/project_templates/stack_package/example/doc/lsst.example/index.rst
   :language: rst

The next sections describe the key components of the module homepage.

.. _module-homepage-filename:

File name and location
======================

This file must be named :file:`index.rst` and must be located in a :ref:`module documentation directory <docdir-module-doc-directories>` within a package.
For example, if the module’s name is ``lsst.example``, the full path for the file is :file:`doc/lsst.example/index.rst`.

.. _module-homepage-preamble:

Preamble
========

The top of the module homepage :file:`index.rst` file should have a `py:currentmodule directive <http://www.sphinx-doc.org/en/master/usage/restructuredtext/domains.html#directive-py:currentmodule>`__ with the module’s namespace as an argument.
For example:

.. code-block:: rst

   .. py:currentmodule:: lsst.example

This allows you to reference APIs relative to that base namespace.
For example these two Python API cross-references are equivalent:

.. code-block:: rst

   `MyClass` and `lsst.example.MyClass`.

.. _module-homepage-title:

Title
=====

The title (top-level header) of the module homepage is the module’s name, without any special formatting (like code literals).

.. note::

   In the future we might include a brief descriptive phrase after the module’s name.
   There is no guidance to add this descriptive phrase at this time.

The cross-reference target above the title must be the name of the module (see the example from the :ref:`starter template <module-homepage-template>`).

.. _module-homepage-context:

Context paragraph
=================

Directly below the title you should add one or more (though not many) paragraphs that describe what the module is for, highlight key features that the module provides, and link to other modules that are related to this module.

The purpose of these paragraphs is not to get into fine details and usage instructions.
Rather, the purpose is to help the reader navigate through the docs.
With this information, the reader should be able to figure out whether this module is relevant to their task in less than a minute and either continue reading or keep searching.

.. _module-homepage-toctrees:

Using <module> and toctrees
===========================

After the context paragraphs, you can add one or more sections containing just `toctree`_ directives.
These `toctree`_\ s link to individual topic pages, such as explanations for how the APIs work and tutorials for using the APIs.
These topics follow the :doc:`Generic guide topic type <generic-guide-topic-type>`.
We haven’t settled on specific guidelines yet for these guides and tutorials.

In most cases, you can add a single section titled “Using <module>” containing a toctree_ that links to the pages:

.. code-block:: rst

   Using lsst.example
   ==================

   .. toctree::
      :maxdepth: 1

      howto-a
      howto-b

.. _module-homepage-python-contributing:

Contributing section
====================

This section puts the module in context as an open source development project.
The template seeds this section with links to the GitHub repository for the module's corresponding package and a ticket search with the module's corresponding Jira component (if the package does not have a Jira component, request one in `#dm-square`_).

If there is documentation describing how to develop (contribute) to the module, as opposed to using the APIs, you should link to those topics with a `toctree`_ in this section.

.. _module-homepage-task-reference:

Task reference section
======================

This section lists any tasks, pipeline tasks, command-line tasks, and standalone configuration classes that are provided by the module.
See the :doc:`task-topic-type` and :doc:`config-topic-type` pages for descriptions of how to document tasks and standalone configuration classes.

Since the content for this section is automatically generated through Sphinx extensions, refer to the :ref:`template and example <module-homepage-template>` for the boilerplate needed to implement this section.
There are two scenarios where the boilerplate needs to be customized:

1. If a module does not provide pipeline tasks, command-line tasks, regular tasks, or standalone config classes, omit the corresponding subsections from the "Task reference" section.
   If a module does not provide any of these topic types, omit the "Task reference" section entirely.

2. If the module does not provide tasks, but does provide either pipeline tasks or command-line tasks, move the ``:toctree: tasks`` field to either of :rst:dir:`lsst-pipelinetasks` or :rst:dir:`lsst-cmdlinetasks`.
   One (and only one) of :rst:dir:`lsst-pipelinetasks`, :rst:dir:`lsst-cmdlinetasks`, or :rst:dir:`lsst-tasks` needs to include the ``:toctree: tasks`` field — it doesn't matter which, though.

For more information, refer to these sections in Documenteer's documentation:

- :rst:dir:`lsst-tasks`
- :rst:dir:`lsst-cmdlinetasks`
- :rst:dir:`lsst-pipelinetasks`
- :rst:dir:`lsst-configs`

.. _module-homepage-script-reference:

Script reference section
========================

This section lists command-line scripts, aside from those that are implemented as command-line tasks, that are provided by the package and implemented by the module.
These scripts can be Python scripts or any other type of shell script.

To use this section, uncomment it from the :ref:`template <module-homepage-template>`.
Individual scripts have corresponding :ref:`script topic pages <script-topic-type>` in the :file:`scripts/` subdirectory of the module documentation directory.
List each of those files in the `toctree`_ of the "Script reference" section.

For example, suppose the :file:`scripts/` subdirectory has these contents:

.. code-block:: text

   scripts
   ├── myScript.py.rst
   └── myBashScript.bash.rst

The "Scripts reference" section then should look like this:

.. code-block:: rst

   .. _lsst.example-scripts:

   Script reference
   ================

   .. toctree::
      :maxdepth: 1

      scripts/myScript.py
      scripts/myBashScript.bash

.. _module-homepage-python-reference:

Python API reference
====================

The “Python API reference” section contains and links to reference information for the module’s Python APIs.
These APIs are documented as :doc:`Numpydoc-formatted docstrings </python/numpydoc>`.

The automodapi_ directive gathers all APIs for a given Python namespace and creates a table of contents that links to pages for each class and function.
This section provides guidance on how to use automodapi_ to document a module, and how to work around docstring syntax errors during development.

.. _module-homepage-single-module:

Single automodapi directive
---------------------------

Many modules import all their public APIs into the top-level module (through ``import`` statements in the :file:`__init__.py` file).
In this case, you only need to include one `automodapi`_ directive that points to this top-level module namespace.
For example:

.. code-block:: rst

   .. automodapi:: lsst.example
      :no-main-docstr:
      :no-inheritance-diagram:

.. note::

   We use ``no-main-docstr`` option because the module's docstring isn't the primary way we document the module (that's the purpose of the module homepage).
   Thus using ``no-main-docstr`` eliminates this clutter.

   The ``no-inheritance-diagram`` option disables a class inheritance from being shown for the module.
   If the inheritance diagram is useful, this option can be omitted.

.. _module-homepage-many-modules:

Multiple automodapi directives
------------------------------

Some modules don’t import all public APIs into the top-level module.
Instead, users are expected to import modules individually.
For this case, you can add an automodapi_ directive for each module that a user may need to import from:

.. code-block:: rst

   .. automodapi:: lsst.example.moduleA
      :no-main-docstr:
      :no-inheritance-diagram:

   .. automodapi:: lsst.example.moduleB
      :no-main-docstr:
      :no-inheritance-diagram:

.. _module-homepage-all:

Controlling what is documented
------------------------------

You may need to exclude APIs from automodapi_ for two reasons:

1. The API is not public, so it shouldn’t be published in documentation.
2. The API includes a broken docstring, and you need to remove that API temporarily.

The main tool for removing non-public APIs from the published documentation is ``__all__``.
Each module should provide an ``__all__`` tuple that explicitly lists the module’s public APIs.
`automodapi`_ respects ``__all__``.

.. _module-homepage-automodapi-skip:

Temporarily removing APIs
-------------------------

To resolve docstring syntax errors, you might need to temporarily remove one or more APIs from the documentation build.
`automodapi`_ provides a few options to help with this.

Use the ``skip`` option to remove one or more specific APIs:

.. code-block:: rst

   .. automodapi:: lsst.example
      :no-main-docstr:
      :no-inheritance-diagram:
      :skip: ClassA, ClassB, functionC

Alternatively, you can allow only one or more certain APIs with the ``allowed-package-names`` option:

.. code-block:: rst

   .. automodapi:: lsst.example
      :no-main-docstr:
      :no-inheritance-diagram:
      :allowed-package-names: ClassA, ClassB

.. tip::

   Remember to “clean” the documentation build when changing what docstrings are included using the :ref:`stack-docs clean <local-pipelines-lsst-io-build-clean>` or :ref:`package-docs clean <build-package-docs-install-delete-build>` commands.
   Otherwise, the cached documentation stub page will remain in the build.

.. _module-homepage-future-components:

Future components
=================

The module homepage topic type will continue to evolve. These are the near-term development themes:

-  C++ API reference section
-  Clearer organization of the “Using <module>” section.
-  EUPS dependencies: an automatically-generated list of both direct and implicit EUPS package dependencies.

.. _pipelines.lsst.io: https://pipelines.lsst.io
.. _stack_package: https://github.com/lsst/templates/tree/main/project_templates/stack_package
.. _toctree: http://www.sphinx-doc.org/en/master/usage/restructuredtext/directives.html#directive-toctree
.. _automodapi: http://sphinx-automodapi.readthedocs.io/en/latest/automodapi.html
.. _`#dm-square`: https://lsstc.slack.com/archives/dm-docs
