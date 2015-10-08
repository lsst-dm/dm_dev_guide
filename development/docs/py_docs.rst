.. _doc-python-code:

#######################
Documenting Python Code
#######################

- ``_doc__`` ``help`` Jupyter's ``?``, Sphinx.
- Python objects should also be self describing: ``__repr__`` and ``__str__``.

Boilerplate
===========

LSST's Python source files begin with a small amount of boilerplate text:

.. code-block:: python

   #
   # LSST Data Management System
   # See COPYRIGHT file at the top of the source tree.
   #
   # This product includes software developed by the
   # LSST Project (http://www.lsst.org/).
   #
   # This program is free software: you can redistribute it and/or modify
   # it under the terms of the GNU General Public License as published by
   # the Free Software Foundation, either version 3 of the License, or
   # (at your option) any later version.
   #
   # This program is distributed in the hope that it will be useful,
   # but WITHOUT ANY WARRANTY; without even the implied warranty of
   # MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
   # GNU General Public License for more details.
   #
   # You should have received a copy of the LSST License Statement and
   # the GNU General Public License along with this program. If not,
   # see <http://www.lsstcorp.org/LegalNotices/>.
   #

Python Docstring Basics
=======================

Python docstrings are special comments that form the ``__doc__`` attributes attached to modules, classes, methods and functions.

Docstrings are delimited by triple double quotes, ``"""``.
This allows docstrings to span multiple lines.

Single line docstrings should have the delimiters and text all on one line:

.. code-block:: python

   """A one-line docstring."""

If the docstring spans multiple lines, the first line of text should appear with the opening delimiter.
The closing delimiter should appear on its own line:

.. code-block:: python

   """Summary for a docstring.

   More discussion in addition paragraphs.

   And another paragraph.
   """

By convention, the first paragraph of a multi-line docstring should be a single summary sentence.

**Do not place the opening delimeter on its own line,** as in:

.. code-block:: python

   """
   Summary for a docstring.

   More discussion in addition paragraphs.

   And another paragraph.
   """

Placement and Indentation
-------------------------

Modules
^^^^^^^

Module-level docstrings should be placed as close to the top of the Python file as possible: *below* the boilerplate, but *above* the imports.
Module-level docstrings should not be indented.

.. code-block:: python
   
   #
   # LSST Data Management System
   # See COPYRIGHT file at the top of the source tree.
   #
   # [...]
   #
   # You should have received a copy of the LSST License Statement and
   # the GNU General Public License along with this program. If not,
   # see <http://www.lsstcorp.org/LegalNotices/>.
   #
   """Summary of MyModule.

   Extended discussion of my module.
   """

   import lsst.afw.table as afw_table
   # [...]

Classes, Methods, and Functions
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Class/method/function docstrings should be placed directly below the class/method/function declaration, and indented to the level of the scope.

.. code-block:: python

   class MyClass(object):
       """Summary of MyClass.

       Additional discussion.
       """

       def __init__(self):
           pass

       def method(self):
           """Summary of method.

           Extended Discussion of my method.
           """
           pass

   def my_function():
       """Summary of my_function.

       Extended discussion of my_function.
       """
       pass

Note that the class docstring takes the place of a docstring of the ``__init__`` method; ``__init__`` has no docstring.

ReStructuredText Specifics for Docstrings
=========================================

We use reStructuredText to mark up and give semantic meaning to text in docstrings.
ReStructuredText is lightweight enough to read in raw form, such as in a help printout in a terminal.
All of the style guidance for using restructured text from our :doc:`ReStructuredText Style Guide <rst_styleguide>` applies in docstrings with a few exceptions defined here.

No space between headers and paragraphs
---------------------------------------

For docstrings we recommend that any space between a header and the following paragraph be omitted.

For example

.. code-block:: python

   """A summary

   A Headline
   ----------
   A paragraph
   """

This deviation from the normal style guide is in keeping with Python community idioms, and to save vertical space in terminal help printouts.

Top level headers are defined with '-'
--------------------------------------

In docstrings, the top level header is marked up with a ``-``, the third level listed in our ReStructuredTextStyle guide.
The header hierarchy is thus:

1. Sections ``-``,
2. Subsections ``^``,
3. Subsubsections ``"``.

This deviation from our reST style guide is in keeping with NumPy community idioms.

Docstring lines should be 75 characters long or less
----------------------------------------------------

Our Coding Style Guide (TODO link) allows for Python lines to be as long as 110 lines.
However docstring lines *must be 75 characters or fewer* to facilitate reading in the terminal or Jupyter notebook contexts.\ [#length]_

.. [#length] '75' originates from the PEP8 length length recommendation of 79 characters, with the typical 4-space indentation level assumed.


