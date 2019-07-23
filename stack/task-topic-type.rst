.. _task-topic:

###############
Task topic type
###############

Tasks, as implemented by ``lsst.pipe.base``, are documented with the *task topic type*.
This page describes how to write task topic pages for `pipelines.lsst.io <https://pipelines.lsst.io>`__.

.. _task-topic-template:

Starter template
================

The task topic file template is available in the `lsst/templates repository`_.

.. note::

   The `task topic file template`_ sets technical details like names and labels for sections, and any boilerplate autodocumenting directives.
   Starting from the template is the best way to follow the task topic standard.

.. _task topic file template:
.. _lsst/templates repository: https://github.com/lsst/templates/tree/master/file_templates/task_topic

For an example task named ``lsst.example.ExampleCmdLineTask``, the rendered template looks like this:

.. remote-code-block:: https://raw.githubusercontent.com/lsst/templates/master/file_templates/task_topic/lsst.example.ExampleCmdLineTask.rst
   :language: rst

The next sections describe the key components of task topics.

.. _task-topic-filename:

File name and location
======================

Task topic files are located in the :file:`tasks/` subdirectory of the :ref:`module documentation directory <docdir-module-doc-directories>` within a package.
The page itself is named after the fully-qualified name of the task class with a ``.rst`` extension.

For example, suppose a task class is ``lsst.pipe.tasks.processCcd.ProcessCcdTask``.
Its task topic page is located in the ``pipe_tasks`` repository like this:

.. code-block:: text

   .
   └── doc
       └── lsst.pipe.tasks
           ├── index.rst
           └── tasks
               └── lsst.pipe.tasks.processCcd.ProcessCcdTask.rst

.. _task-topic-preamble:

Preamble
========

The :rst:dir:`lsst-task-topic` directive at the top of the page declares that the page is a canonical reference for the specified task class.
For example:

.. code-block:: rst

   .. lsst-task-topic:: lsst.pipe.tasks.processCcd.ProcessCcdTask

Through this directive, other pages can reference this page using the :rst:role:`lsst-task` role:

.. code-block:: rst

   :lsst-task:`lsst.pipe.tasks.processCcd.ProcessCcdTask`

In addition, other pages can use the :rst:dir:`lsst-tasks` and :rst:dir:`lsst-cmdlinetasks` directives to automatically list task pages that are marked by an :rst:dir:`lsst-task-topic` directive.
See the :doc:`module-homepage-topic-type` for an example of this strategy.

.. _task-topic-title:

Title
=====

The title (top-level header) of the task topic is the class's name (without the module).
No special code formatting is applied to the title.

.. caution::

   If there are two tasks of the same class name, the additional tasks should have their module name in parentheses after the class name.
   For example: ``RegisterTask (lsst.pipe.tasks.ingest)``.

.. _task-topic-context:

Context paragraph
=================

Directly below the title, write a paragraph or two (though not many) that describe what the task is for.
The aim of this content is to help a reader navigate the documentation and understand whether this task is relevant to what they are trying to understand.

Consider including the following information in the context paragraphs:

- What the task does.

- The names of important datasets that are created by the task.

- Whether the task is a command-line task or not (and if so, the name of the executable).

This is a succinct context paragraph for ``ProcessCcdTask``:

.. code-block:: rst

  ``ProcessCcdTask`` provides a preliminary astrometric and photometric calibration for a single frame (a ``raw`` dataset), yielding a ``calexp`` dataset.
  ``ProcessCcdTask`` is available as a `command-line task <pipe-tasks-command-line-tasks>`, ``processCcd.py``.

.. _task-topic-processing:

Processing summary section
==========================

The "Processing summary" section outlines the algorithm that the task implements.
Like the context paragraph above it, the "Processing summary" should be brief and highly scannable.
The reader should be able to quickly grasp what the task does through this section.
For algorithmic or usage details, refer the reader to the :ref:`"In depth" section <task-topic-indepth>`.

In most cases you can express the algorithm as an enumerated list.
Introduce the list with a sentence like this:

.. code-block:: rst

   ``ProcessCcdTask`` runs this sequence of operations:

If a step is implemented by a subtask, refer to the subtask by its configuration name and with the default target in parentheses:

.. code-block:: rst

   #. Removes instrumental signature from the ``raw`` dataset by calling the
      :lsst-config-field:`~lsst.pipe.tasks.processCcd.ProcessCcdConfig.isr` subtask
      (default: :lsst-task:`~lsst.ip.isr.isrTask.IsrTask`).

If an important configuration field (besides a retargetable subtask) controls the flow of a task, you should point out that configuration field as well.

Additional notes:

- Note the use of the active, present-tense verb that describes what the task does.

- Use the :rst:role:`lsst-config-field` role to link to documentation for the configuration field.

  The argument of the :rst:role:`lsst-config-field` role is the fully-qualified name of the configuration field, as a member of the Config class (**not as a member of the task class**).

- Use the :rst:role:`lsst-task` role to refer to other task topic pages.

.. _task-topic-cmdline:

Command-line interface section
==============================

If the task is a command-line task, include this "Command-line interface" section in the task topic.
This section briefly reminds users what the command-line interface for a task looks like and primarily refers the reader to centralized documentation for command-line task usage in the `lsst.pipe.base <https://pipelines.lsst.io/v/daily/modules/lsst.pipe.base/>`__ docs.
To implement this section, copy from the template or example shown above.

.. caution::

   The "Command-line interface" component of the task topic isn't fully developed yet.
   As the Science Pipelines migrate towards ``PipelineTask`` we will introduce a rigorous system for documenting command-line activator usage.
   This means that while you can put some effort into this section now, don't *too much* effort into this content.

.. _task-topic-api:

Python API summary section
==========================

The "Python API summary" section provides a bridge to the API reference for task classes, which are written as numpydoc docstrings (as are all Python APIs).

This section is automatically generated with the :rst:dir:`lsst-task-api-summary` directive.
The directive's argument is the task's fully-qualified name.
For example:

.. code-block:: rst

   .. lsst-task-api-summary:: lsst.pipe.tasks.processCcd.ProcessCcdTask

.. _task-topic-datasets:

Butler datasets section
=======================

The "Butler datasets" section lists the datasets that are consumed and generated by this task.
Input datasets are listed in a subsection called "Input datasets," while output datasets are listed in "Output datasets."

Each dataset is represented by a :ref:`definition list item <rst-dl>`.
The dataset name is the "term" and is formatted as a code literal (wrapped in double backticks).
The definition is free-form content that briefly describes the dataset.

An example of an input dataset description:

.. code-block:: rst

   ``raw``
       Raw dataset from a camera, as ingested into the input Butler data repository.
       Unpersisted by the :lsst-config-field:`~lsst.pipe.tasks.processCcd.ProcessCcdConfig.isr` subtask.

An example of an output dataset description:

.. code-block:: rst

   ``calexp``
       The calibrated exposure.
       Persisted by the :lsst-config-field:`~lsst.pipe.tasks.processCcd.ProcessCcdConfig.calibrate` subtask.

       The default subtask (:lsst-task:`~lsst.pipe.tasks.calibrate.CalibrateTask`) adds the following metadata:

       ``MAGZERO_RMS``
           The RMS (standard deviation) of ``MAGZERO``, measured by the :lsst-config-field:`~lsst.pipe.tasks.calibrate.CalibrateTask.photoCal` subtask.
       ``MAGZERO_NOBJ``: ``Number of stars used to estimate ``MAGZERO``.
           This is ``ngood`` reported by the :lsst-config-field:`~lsst.pipe.tasks.calibrate.CalibrateTask.photoCal` subtask.
       ``COLORTERM1``
           Always ``0.0``.
       ``COLORTERM2``
           Always ``0.0``.
       ``COLORTERM3``
           Always ``0.0``.

.. caution::

   The "Butler datasets" component of the task topic isn't fully developed yet.
   As the Science Pipelines migrates towards ``PipelineTask``, we will introduce a rigorous system for documenting datasets and their relationship to tasks.
   This means that while you can put some effort into this section now, don't put *too much* effort into this content.

.. _task-topic-subtasks:

Retargetable subtasks section
=============================

The "Retargetable subtasks" section describes the configuration fields associated with subtasks or subtask-like objects.
Specifically, this section lists all ``ConfigurableField`` or ``RegistryField`` types.

This section should only include an :rst:dir:`lsst-task-config-subtasks` directive.
The directive's argument is the task's fully-qualified name.
For example:

.. code-block:: rst

   .. lsst-task-config-subtasks:: lsst.pipe.tasks.processCcd.ProcessCcdTask

.. _task-topic-configs:

Configuration fields section
============================

The "Configuration fields" section describes the task's configuration fields that aren't ``ConfigurableField`` or ``RegistryField`` types.

This section should only include a :rst:dir:`lsst-task-config-fields` directive.
The argument of the directive is the task's fully-qualified name.
For example:

.. code-block:: rst

   .. lsst-task-config-fields:: lsst.pipe.tasks.processCcd.ProcessCcdTask

.. _task-topic-indepth:

In depth section
================

You can include an "In depth" section in the task topic to go into greater depth about the algorithms that the task implements.
The discussion can touch on both the scientific aspects of the task as well as concrete details like configuration fields and subtasks.
This section can be as long as it needs to be and can organized into subsections.

The "In depth" section is located after "Configuration fields" but before "Examples."
If this type of content is not present, leave this section out.
It can always be added later.

.. _task-topic-examples:

Examples section
================

In this section, provide examples that show how the task can be used.
Ideally, the examples should be runnable by a user either on the command-line or Python REPL, as appropriate.

.. caution::

   How DM includes examples in user documentation is still being developed.
   The new system will facilitate testing, dataset delivery, and integration with Jupyter.

   In the meantime, you can include examples in plain reStructuredText on a best-effort basis with the expectation that they will be reimplemented later.
   Use the :rst:dir:`code-block` directive to include code samples, and command-line prompts and outputs.

.. _task-topic-debugging:

Debugging section
=================

You can port the debugging section from existing task documentation into reStructuredText in the "Debugging" section.
Document individual fields in the debug info dictionary with a :ref:`reStructuredText definition list <rst-dl>`.
