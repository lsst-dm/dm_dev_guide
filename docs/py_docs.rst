#######################
Documenting Python Code
#######################

.. note::

   This is a preview documentation format specification.
   Software documentation should currently be written in the format described at https://confluence.lsstcorp.org/display/LDMDG/Documentation+Standards#DocumentationStandards-Python

We document Python code in three ways:

1. By writing *docstrings* for all public python objects (modules, classes, methods, functions and constants).
   
   These docstrings are exposed to users in a variety of contexts, from developers reading the code, to interactive Python users introspecting an object with ``help()``, Jupyter notebook users typing `object?`, and finally to readers of this user guide.

   Docstrings are the public specification of our Python API.

2. By commenting our code internally with hash marks (``#``).
   
   These comments are meant to be read only by developers reading and editing the source code.

3. By allowing Python objects to be introspected interactively with the ``__str__`` and ``__repr__`` magic methods.

This page focuses on public code documentation through docstrings, while the latter two are discussed in our Python style guide.

.. TODO add link to python style guide.

.. _py-doc-boilerplate:

Boilerplate
===========

LSST's Python source files begin with a small amount of boilerplate text:

.. Note: should this boilerplate be moved to our coding standard guide?

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

.. _py-docstring-basics:

Python Docstring Basics
=======================

Python docstrings are special strings that form the ``__doc__`` attributes attached to modules, classes, methods and functions.
Docstrings are specified by `PEP-257`_.

.. _PEP-257: https://www.python.org/dev/peps/pep-0257/

Docstrings are delimited by triple double quotes, ``"""``.
This allows docstrings to span multiple lines.

Single line docstrings should have the delimiters and text all on one line:

.. code-block:: python

   """A one-line docstring."""

Such single line docstrings should only be considered acceptable for private (read: *undocumented*) APIs or for properties.
Complete docstrings will span multiple lines.

When the docstring spans multiple lines, the first line of text should appear with the opening delimiter.
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

   Discussion how how the summary line should start on the same line as the
   opening delimiter.

   And another paragraph.
   """

.. _py-docstring-placement:

Docstring Placement
===================

Modules
-------

Module-level docstrings must be placed as close to the top of the Python file as possible: *below* the boilerplate and any ``#!/usr/bin/env python``, but *above* the imports.
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
-------------------------------

Class/method/function docstrings must be placed directly below the class/method/function declaration, and indented to the level of the scope.

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

.. _py-doc-docstring-rst:

ReStructuredText in Docstrings
==============================

We use reStructuredText to mark up and give semantic meaning to text in docstrings.
ReStructuredText is lightweight enough to read in raw form, such as command line terminal printout.
All of the style guidance for using restructured text from our :doc:`ReStructuredText Style Guide <rst_styleguide>` applies in docstrings with a few exceptions defined here.

No space between headers and paragraphs
---------------------------------------

For docstrings the numpydoc standard is to omit any space between a header and the following paragraph.

For example

.. code-block:: python

   """A summary

   A Headline
   ----------
   A paragraph
   """

This deviation from the normal style guide is in keeping with Python community idioms, and to save vertical space in terminal help printouts.

.. _py-doc-section-levels:

Top level headers are defined with '-'
--------------------------------------

In docstrings, the top level header is marked up with a ``-``, the third level listed in our ReStructuredTextStyle guide.
The header hierarchy is thus:

1. Sections ``-``,
2. Subsections ``^``,
3. Subsubsections ``"``.

This deviation from our :ref:`reST style guide <rst-sectioning>` is in keeping with Numpy community idioms, and required by our Sphinx tooling.

.. FIXME uncomment this when RFC-107 is decided
..
.. Docstring lines should be 75 characters long or less
.. ----------------------------------------------------
.. 
.. .. TODO link to code style guide
.. 
.. Our Coding Style Guide allows for Python lines to be as long as 110 lines.
.. However docstring lines *must be 75 characters or fewer* to facilitate reading in the terminal or Jupyter notebook contexts.\ [#length]_
.. 
.. .. [#length] '75' originates from the PEP8 length length recommendation of 79 characters, with the typical 4-space indentation level assumed.

.. _py-docstring-sections:

Common Structure of Docstrings
==============================

We organize Python docstrings into sections that appear in a common order.
This format follows the `Numpydoc`_ standard (used by NumPy, SciPy, and Astropy, among other scientific Python packages) rather than the format described in `PEP-287`_.

.. _Numpydoc: https://github.com/numpy/numpy/blob/master/doc/HOWTO_DOCUMENT.rst.txt

.. _PEP-287: https://www.python.org/dev/peps/pep-0287/

1. :ref:`Short Summary <py-docstring-short-summary>`
2. :ref:`Deprecation Warning <py-docstring-deprecation>` (if applicable)
3. :ref:`Extended Summary <py-docstring-extended-summary>` (optional)
4. :ref:`Parameters <py-docstring-parameters>` (if applicable; for classes, methods and functions)
5. :ref:`Methods <py-docstring-methods>` (if applicable; for classes)
6. :ref:`Attributes <py-docstring-attributes>` (if applicable; for classes)
7. :ref:`Returns <py-docstring-returns>` or :ref:`Yields <py-docstring-yields>` (if applicable; for functions, methods, and generators)
8. :ref:`Other Parameters <py-docstring-other-parameters>` (if applicable; for classes, methods and functions)
9. :ref:`Raises <py-docstring-raises>` (if applicable)
10. :ref:`See Also <py-docstring-see-also>` (optional)
11. :ref:`Notes <py-docstring-notes>` (optional)
12. :ref:`References <py-docstring-references>` (optional)
13. :ref:`Examples <py-docstring-examples>` (optional)

In the following sections we describe the content of these docstring sections and provide examples of full docstrings composed for classes, methods, functions, and constants.  

.. _py-docstring-short-summary:

Short Summary
-------------

A one-line summary that does not use variable names or the function name:

.. code-block:: python

   def add(a, b):
       """Sum two numbers."""
       return a + b

The summary should be written as a present-tense action.
*Do not write something like "Sums two numbers."*

The one line summary can be used alone only in *extremely* trivial cases, such as Python properties.
Keep in mind our `style guideline for placing the short summary on the same line as the opening (and closing, if used alone) docstring delimiters <py-docstring-basics>`_.
In virtually all cases using a full multi-line docstring is the correct thing to do.

.. _py-docstring-deprecation:

Deprecation Warning
-------------------

A section (where applicable) to warn users that the object is deprecated.
Section contents should include:

1. In what stack version the object was deprecated, and when it will be removed.
2. Reason for deprecation if this is useful information (e.g., object is superseded, duplicates functionality found elsewhere, etc.).
3. New recommended way of obtaining the same functionality.

This section should use the ``note`` Sphinx directive instead of an underlined section header.

.. code-block:: rst

   .. note:: Deprecated in 11_0
             `ndobj_old` will be removed in 12_0, it is replaced by
             `ndobj_new` because the latter works also with array subclasses.

.. _py-docstring-extended-summary:

Extended Summary
----------------

A few sentences giving an extended description.
This section should be used to clarify *functionality*, not to discuss implementation detail or background theory, which should rather be explored in the :ref:`Notes <py-docstring-notes>` section below.
You may refer to the parameters and the function name, but parameter descriptions still belong in the :ref:`Parameters <py-docstring-parameters>` section.

.. _py-docstring-parameters:

Parameters
----------

*For functions, methods and classes.*

*Parameters* is a description of the function arguments, keywords and their respective types.

.. code-block:: rst

   Parameters
   ----------
   x : type
       Description of parameter `x`.

Notice that the description is **indented by four spaces** from the ``{name} : {type}`` line of each argument.
If a description spans more than one line, the continuation lines must be indented to the same level.

Arguments should be listed in the same order as they appear in the function signature.

When describing an argument in the description, enclose the name of the variable in single backticks (the default role in reST, which is Python-aware in docstrings).

Parameter Types
^^^^^^^^^^^^^^^

For the parameter types, be as precise as possible.

.. code-block:: rst

   Parameters
   ----------
   filename : str
       Description of `filename`.
   copy : bool
       Description of `copy`.
   dtype : data-type
       Description of `dtype`.
   iterable : iterable object
       Description of `iterable`.
   shape : int or tuple of int
       Description of `shape`.
   files : list of str
       Description of `files`.

For instances of classes, provide the full namespace to the class.

When a parameter can only assume one of a fixed set of values, those values can be listed in braces:

.. code-block:: rst

   order : {'C', 'F', 'A'}
       Description of `order`.

Optional Parameters
^^^^^^^^^^^^^^^^^^^

For keyword arguments, add ``optional`` to the type specification:

.. code-block:: rst

   x : int, optional

Optional keyword parameters have default values, which are displayed as
part of the function signature. They can also be detailed in the
description:

.. code-block:: rst

   Parameters
   ----------
   x : type
       Description of parameter `x` (the default is -1, which implies summation
       over all axes).


Shorthand
^^^^^^^^^

When two or more input parameters have exactly the same type, shape and
description, they can be combined:

.. code-block:: rst

   x1, x2 : array-like
       Input arrays, description of `x1`, `x2`.

.. _py-docstring-methods:

Methods
-------

*For classes.*

If a class has a very large number of methods, which are hard to discover, an additional *Methods* section *can* be provided to list them:

.. code-block:: rst

   Methods
   -------
   read(filename)
      Read a table from a file
   sort(column, order='ascending')
      Sort by `column`

Do not list private methods in the Methods section.
If it is necessary to explain a private method (use with care!), it can be referred to in the :ref:`Extended Summary <py-docstring-extended-summary>` or :ref:`Notes <py-docstring-notes>` sections.

Do not list ``self`` as the first parameter of a method.

.. _py-docstring-attributes:

Attributes
----------

*For classes.*

An ``Attributes`` section, located below the ``Parameters`` section, may be
used to describe class variables:

.. code-block:: rst

   Attributes
   ----------
   x : float
       The X coordinate.
   y : float
       The Y coordinate.

Attributes that are properties and have their own docstrings can be simply
listed by name:

.. code-block:: rst

   Attributes
   ----------
   real
   imag
   x : float
       The X coordinate
   y : float
       The Y coordinate

.. _py-docstring-returns:

Returns
-------

*For functions and methods*.

*Returns* is an explanation of the returned values and their types, of the same format as `Parameters <py-docstring-parameters>`_.

If a sequence of values is returned, each value may be separately listed, in order:

.. code-block:: rst

   Returns
   -------
   x : int
       Description of x.
   y : int
       Description of y.

If a return type is `dict`, ensure that the key-value pairs are documented in the description.

.. _py-docstring-yields:

Yields
------

*For generators.*

*Yields* is used identically to `Returns <py-docstring-yields>`_, but for generators.

.. _py-docstring-other-parameters:

Other Parameters
----------------

*For classes, methods and functions.*

*Other Parameters* is an optional section used to describe infrequently used parameters.
It should only be used if a function has a large number of keyword parameters, to prevent cluttering the :ref:`Parameters <py-docstring-parameters>` section.

.. _py-docstring-raises:

Raises
------

*For classes, methods and functions.*

*Raises* is an optional section detailing which errors get raised and under what conditions:

.. code-block:: rst

   Raises
   ------
   IOError
       If the file could not be read.

This section should be used judiciously---only for errors that are non-obvious or have a large chance of getting raised.

.. _py-docstring-see-also:

See Also
--------

*See Also* is an optional section used to refer to related code.
This section can be very useful, but should be used judiciously.
The goal is to direct users to other functions they may not be aware of, or have easy means of discovering (by looking at the module docstring, for example).
Routines whose docstrings further explain parameters used by this function are good candidates.

As an example, for a function such as ``numpy.cos``, we would have

.. code-block:: rst

   See Also
   --------
   sin : Compute an element-wise Sine function.
   tan : Compute an element-wise Tangent function.

When referring to functions in the same sub-module, no prefix is needed, and the tree is searched upwards for a match.

Prefix objects from other sub-modules appropriately by their greatest common namespace.
E.g., whilst documenting a ``lsst.afw.tables`` module, refer to a class in ``lsst.afw.detection`` by

.. code-block:: rst

   afw.detection.Footprint : Regular detection footprint.

When referring to an entirely different module or package, use the full namespace.

.. code-block:: rst

   astropy.table.Tables : Flexible table data structures

Functions may be listed without descriptions; this is preferable if the functionality is clear from the function name:

.. code-block:: rst

   See Also
   --------
   func_a : Function a with its description.
   func_b, func_c, func_d
   func_e
   
.. _py-docstring-notes:

Notes
-----

*Notes* is an optional section that provides additional information about the code, possibly including a discussion of the algorithm.
This section may include mathematical equations, written in `LaTeX <http://www.latex-project.org/>`_ format:

.. code-block:: rst

  The FFT is a fast implementation of the discrete Fourier transform:

  .. math:: X(e^{j\omega } ) = x(n)e^{ - j\omega n}

Equations can also be typeset underneath the math directive:

.. code-block:: rst

  The discrete-time Fourier time-convolution property states that

  .. math::

     x(n) * y(n) \Leftrightarrow X(e^{j\omega } )Y(e^{j\omega } )\\
     another equation here

Math can furthermore be used inline:

.. code-block:: rst

   The value of :math:`\omega` is larger than 5.

Variable names are displayed in typewriter font, obtained by using ``\mathtt{var}``:

.. code-block:: rst

   We square the input parameter `alpha` to obtain
   :math:`\mathtt{alpha}^2`.

Note that LaTeX is not particularly easy to read, so use equations sparingly.

Images are allowed, but should not be central to the explanation; users viewing the docstring as text must be able to comprehend its meaning without resorting to an image viewer.
These additional illustrations are included using:

.. code-block:: rst

   .. image:: filename

where filename is a path relative to the reference guide source directory.

.. _py-docstring-references:

References
----------

References cited in the :ref:`Notes <py-docstring-notes>` section may be listed here, e.g. if you cited the article below using the text ``[1]_``, include it as in the list as follows:

.. code-block:: rst

   .. [1] O. McNoleg, "The integration of GIS, remote sensing,
      expert systems and adaptive co-kriging for environmental habitat
      modelling of the Highland Haggis using object-oriented, fuzzy-logic
      and neural-network techniques," Computers & Geosciences, vol. 22,
      pp. 585-588, 1996.

Note that Web pages should be referenced with regular inline links.

References are meant to augment the docstring, but should not be required to understand it. References are numbered, starting from one, in the order in which they are cited.

.. _py-docstring-examples:

Examples
--------

*Examples* is an optional section for examples, using the `doctest <http://docs.python.org/library/doctest.html>`_ format.
These examples do not replace unit tests, but *are* intended to be tested to ensure documentation and code is consistent.
While optional, this section is very strongly encouraged.

When multiple examples are provided, they should be separated by blank lines.
Comments explaining the examples should have blank lines both above and below them:

.. code-block:: rst

   >>> np.add(1, 2)
   3

   Comment explaining the second example

   >>> np.add([1, 2], [3, 4])
   array([4, 6])

For tests with a result that is random or platform-dependent, mark the output as such:

.. code-block:: rst

   >>> np.random.rand(2)
   array([ 0.35773152,  0.38568979])  #random

It is not necessary to use the doctest markup ``<BLANKLINE>`` to indicate empty lines in the output.

.. The examples may assume that ``import numpy as np`` is executed before the example code.

Documenting Modules
===================

Module docstrings are placed *after* the boilerplate and before any imports or other code.
Module docstrings contain the following sections:

1. :ref:`Short Summary <py-docstring-short-summary>`
2. :ref:`Deprecation Warning <py-docstring-deprecation>` (if applicable)
3. :ref:`Extended Summary <py-docstring-extended-summary>` (optional)
4. :ref:`See Also <py-docstring-see-also>` (optional)

.. TODO Provide an example

Documenting Classes
===================

Class docstrings are placed directly after the class definition, and serve to document both the class as a whole, *and* the arguments passed to the ``__init__`` constructor.
Class docstrings contain the following sections:

1. :ref:`Short Summary <py-docstring-short-summary>`
2. :ref:`Deprecation Warning <py-docstring-deprecation>` (if applicable)
3. :ref:`Extended Summary <py-docstring-extended-summary>` (optional)
4. :ref:`Parameters <py-docstring-parameters>` (if applicable)
5. :ref:`Methods <py-docstring-methods>` (if applicable)
6. :ref:`Attributes <py-docstring-attributes>` (if applicable)
7. :ref:`Other Parameters <py-docstring-other-parameters>` (if applicable)
8. :ref:`Raises <py-docstring-raises>` (if applicable)
9. :ref:`See Also <py-docstring-see-also>` (optional)
10. :ref:`Notes <py-docstring-notes>` (optional)
11. :ref:`References <py-docstring-references>` (optional)
12. :ref:`Examples <py-docstring-examples>` (optional)

Note that the `Methods <py-docstring-methods>`_ section is only used if the method list is extremely long.
In general, trust that the tables to contents in the user guide pages will provide useful summaries of a class's methods.

.. code-block:: python

   class SkyCoordinate(object):
       """Coordinate on the sky as Right Ascension and Declination.

       Parameters
       ----------
       ra : float
          Right ascension (degrees).
       dec : float
          Declination (degrees).
       frame : {'icrs', 'fk5'}, optional
          Coordinate frame.

       Raises
       ------
       ValueError : Input angles are outside range.
       
       See also
       --------
       GalacticCoordinate

       Examples
       --------
       To define the coordinate of the M31 galaxy,

       >>> m31_coord = SkyCoordinate(10.683333333, 41.269166667)
       SkyCoordinate(10.683333333, 41.269166667, frame='icrs')
       """

       def __init__(self, ra, dec, frame='icrs'):
           pass


Documenting Methods and Functions
=================================

Method and function docstrings contain the following sections:

1. :ref:`Short Summary <py-docstring-short-summary>`
2. :ref:`Deprecation Warning <py-docstring-deprecation>` (if applicable)
3. :ref:`Extended Summary <py-docstring-extended-summary>` (optional)
4. :ref:`Parameters <py-docstring-parameters>` (if applicable)
5. :ref:`Returns <py-docstring-returns>` or `Yields <py-docstring-yields>` (if applicable)
6. :ref:`Other Parameters <py-docstring-other-parameters>` (if applicable)
7. :ref:`Raises <py-docstring-raises>` (if applicable)
8. :ref:`See Also <py-docstring-see-also>` (optional)
9. :ref:`Notes <py-docstring-notes>` (optional)
10. :ref:`References <py-docstring-references>` (optional)
11. :ref:`Examples <py-docstring-examples>` (optional)

A minimal example:

.. code-block:: python

   def log(message, level):
       """Submit a message to the log.

       Parameters
       ----------
       message : str
          Log message.
       level : str
          Priority level of the log message.
       """


Documenting constants, class properties, attributes
===================================================

Constants in modules, and properties and attributes in classes are all similar in that their values are accessed with arguments.
At minimum, constants/properties/attributes should have a summary line, but can also have a more complete structure with sections:

1. :ref:`Short Summary <py-docstring-short-summary>`
2. :ref:`Deprecation Warning <py-docstring-deprecation>` (if applicable)
3. :ref:`Extended Summary <py-docstring-extended-summary>` (optional)
4. :ref:`Notes <py-docstring-notes>` (optional)
5. :ref:`References <py-docstring-references>` (optional)
6. :ref:`Examples <py-docstring-examples>` (optional)

In the short summary, a description of the type should be included:

.. code-block:: rst

   NAME = 'LSST'
   """Name of the project (str)"""

Note that class attributes can alternatively be documented in an :ref:`Attributes <py-docstring-attributes>` section of the class's docstring.
This is particularly useful when the attribute is not set in the class scope, but rather in a method such as ``__init__``.

.. code-block:: rst

   class Answer(object):
       """Container for the answer.
       
       Attributes
       ----------
       answer : obj
          The answer.
       source
       """

       def __init__(self):
           self.contents = 42

       @property
       def source(self):
           """Purveyor of the answer."""
           return 'Deep Thought'

Acknowledgements
================

These docstring guidelines are derived/adapted from in the `Numpy <https://github.com/numpy/numpy/blob/master/doc/HOWTO_DOCUMENT.rst.txt>`_ and `Astropy <http://docs.astropy.org/en/stable/_sources/development/docrules.txt>`_ documentation.

Numpy is Copyright © 2005-2013, NumPy Developers.

Astropy is Copyright (c) 2011-2015, Astropy Developers.
