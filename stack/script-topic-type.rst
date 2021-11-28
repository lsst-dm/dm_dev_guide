.. _script-topic-type:

##############################
Command-line script topic type
##############################

The script topic type provides a common documentation format for describing ad hoc scripts that are packaged with the LSST Stack.
This topic type is oriented towards creating *reference* documentation; these topics are the canonical descriptions for a script's command-line arguments, options, and functionality.
Other topics, like how-to guides and tutorials, can link to these descriptions.

This script topic type works for any type of command-line executable (like shell scripts and compiled C++ executables) and relies on manually writing the usage, and documentation for options and arguments.
If your script is written in Python and uses `argparse`, you can automate this reference documentation by using the :doc:`argparse-based variant of the script topic type <argparse-script-topic-type>`.

.. seealso::

   If the script is implemented in Python with an `argparse`-based command-line interface, refer to :doc:`argparse-script-topic-type` instead.

   If the script is actually a command-line task, document it with a :doc:`task topic <task-topic-type>` instead.

.. _script-topic-type-template:

Starter template
================

Create a new script topic from Slack.\ [#template]_
Open a |dmw-sqrbot| and type:

.. code-block:: text

   create file

Then select **Science Pipelines documentation > Script topic (generic)**.

.. [#template] The script topic file template is available in the `lsst/templates repository`_.

.. _lsst/templates repository: https://github.com/lsst/templates/tree/main/file_templates/script_topic

For an example script named ``exampleScript.sh``, the rendered template looks like this:

.. remote-code-block:: https://raw.githubusercontent.com/lsst/templates/main/file_templates/script_topic/exampleScript.sh.rst
   :language: rst

The next sections describe the key components of script topics.

.. _script-topic-type-filename:

File name and location
======================

The file must be named after the command-line executable, including any extension.
For example, if the script is ``myScript.py``, the topic's file should be named ``myScript.py.rst``.

The file must be located in the :file:`scripts/` subdirectory of the :ref:`module documentation directory <docdir-module-doc-directories>` within a package.

For example, if the module’s namespace is ``lsst.example``, the full path for the file is :file:`doc/lsst.example/scripts/myScript.py.rst`.

.. _script-topic-type-preamble:

Preamble
========

The topic of the script topic file should have a program_ directive with the executable’s name as an argument:

.. code-block:: rst

   .. program:: exampleScript.sh

This allows you to associate option_ directives further down the page with this executable in cross-references.

.. _program: http://www.sphinx-doc.org/en/master/usage/restructuredtext/domains.html#directive-program
.. _option: http://www.sphinx-doc.org/en/master/usage/restructuredtext/domains.html#directive-option

.. _script-topic-type-title:

Title
=====

The title (top-level header) is the executable's name (what you would type on the command line, assuming the executable is in the ``$PATH``), without any special formatting (like code literals).

.. _script-topic-type-summary:

Summary sentence
================

Directly below the title, write a sentence that says what the script is for.
Think of this sentence as a subtitle that helps a reader quickly understand what the script is for, without getting into too much detail.

.. _script-topic-description:

Description
===========

After the summary sentence (a paragraph of its own), you can add additional paragraphs that discuss functionality in depth, and provide small examples of how the script might be used.

If necessary, organize these paragraphs into subsections.

.. _script-topic-usage:

Usage
=====

Before the options and arguments are documented, include a `usage message`_ inside a code-block directive.

The :ref:`starter template <script-topic-type-template>` includes a basic usage message.
To learn more about formatting usage messages, see Wikipedia_.

.. _usage message:
.. _Wikipedia: https://en.wikipedia.org/wiki/Usage_message

.. _script-topic-positional:

Positional arguments (optional section)
=======================================

The section named "Positional arguments" is where you document command-line arguments that are positional.
*Leave this section out if there aren't any positional arguments.*

Document each argument with an option_ directive.
For example:

.. code-block:: rst

   .. option:: file

      Path of an input file.

.. _script-topic-options:

Optional arguments (optional section)
=====================================

The section named "Optional arguments" is where you document options, like the ``-h`` option to produce a help message.
*Leave this section out if there aren't any optional arguments.*

Document each optional argument using the option_ directive, including the dash character (``-``):

.. code-block:: rst

   .. option:: -h, --help

      Print the help message and exit.

Notice how both the short and long forms of an option can be documented together.
Of course, options don't need to have both forms.

The option_ directive also works with options that have operands:

.. code-block:: rst

   .. option:: --ref gitref

      The Git commit SHA, tag, or branch name.

.. _script-topic-custom-option-groups:

Grouped argument sections (optional sections)
=============================================

If the command-line interface has a large number of options, you might want to organize them into their own sections.
This corresponds to how you would use the `argparse.ArgumentParser.add_argument_group` method in Python scripts.

Make sure the section name ends with the word "arguments" and start the section name with the name of the group.
The content of this section is also made up of option_ directives.

.. code-block:: rst

   Positional arguments
   ====================

   .. option:: file

      Path to the file

   Optional arguments
   ==================

   .. option:: -h, --help

      Print the help message and exit.

   .. option:: --verbose

      Enable verbose logging.

   XYZ arguments
   =============

   .. option:: --flag1 bar

      Description of flag1.

   .. option:: --flag2

      Description of flag2.
