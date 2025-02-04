.. _config-topic:

#################
Config topic type
#################

Config classes (subclasses of ``lsst.pex.config.Config``) are typically associated with a task class and are documented as part of the :doc:`task-topic-type`.
Some config classes stand alone, but are used used in tasks through a ``ConfigField`` configuration field.
For example, the ``lsst.pipe.tasks.photoCal.PhotoCalTask`` has a ``colorterms`` configuration field that points to a standalone ``lsst.pipe.tasks.colorterms.ColortermLibrary`` config class.
This page describes how to document config classes like ``ColortermLibrary``.

.. _config-topic-template:

Starter template
================

Create a new config topic from Slack.\ [#template]_
Open a |dmw-squarebot| and type:

.. code-block:: text

   create file

Then select **Science Pipelines documentation > Config topic**.

.. [#template] The config topic file template is maintained in the `lsst/templates repository`_.

.. _lsst/templates repository: https://github.com/lsst/templates/tree/main/file_templates/config_topic

For an example config named ``lsst.example.ExampleConfig``, the rendered template looks like this:

.. remote-code-block:: https://raw.githubusercontent.com/lsst/templates/main/file_templates/config_topic/lsst.example.ExampleConfig.rst
   :language: rst

The next sections describe the key components of config topics.

.. _config-topic-filename:

File name and location
======================

Config topic files are located in the :file:`configs/` subdirectory of the :ref:`module documentation directory <docdir-module-doc-directories>` within a package.
The page itself is named after the fully-qualified name of the config class with a ``.rst`` extension.

For example, suppose a standalone config class is ``lsst.pipe.tasks.colorterms.Colorterm``.
Its config topic page is located in the ``pipe_tasks`` package directory like this:

.. code-block:: text

   .
   └── doc
       └── lsst.pipe.tasks
           ├── index.rst
           └── configs
               └── lsst.pipe.tasks.colorterms.Colorterm.rst

.. _config-topic-preamble:

Preamble
========

The :rst:dir:`lsst-config-topic` directive at the top of the page declares that the page is a canonical reference for the specified config class.
For example:

.. code-block:: text

   .. lsst-config-topic:: lsst.pipe.tasks.colorterms.Colorterm

Through this directive, other pages can reference this config using the :rst:role:`lsst-config` role:

.. code-block:: rst

   :lsst-config:`lsst.pipe.tasks.colorterms.Colorterm`

In addition, other pages can use the :rst:dir:`lsst-configs` directive to automatically list config pages that are marked by an :rst:dir:`lsst-config-topic` directive.
See the :doc:`module-homepage-topic-type` for an example of this strategy.

.. _config-topic-title:

Title
=====

The title is the name of the config class (without its module name).
No special code formatting is applied to the title.

.. _config-topic-context:

Context paragraph
=================

Directly below the title, write a paragraph or two (though not many) that describe what the config is for.
Link to any related tasks using the :rst:role:`lsst-task` role.

.. _config-topic-fields:

Configuration fields
====================

This section lists the configuration fields that the config class provides.
The listing is similar to the :ref:`task-topic-configs` of task configs.

The only content of this section in the reStructuredText file is a :rst:dir:`lsst-config-fields` directive.
The fully-qualified name of the config class is the directive's sole argument.

For example:

.. code-block:: rst

   .. lsst-config-fields:: lsst.pipe.tasks.colorterms.Colorterm

In depth section
================

If necessary, you can provide an extended discussion of the configuration in this section.
Feel free to include examples as necessary.

Omit this section if there isn't any content for it.
