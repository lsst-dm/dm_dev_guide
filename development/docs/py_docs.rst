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

.. _py-docstring-basics:

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

Common Structure of Docstrings
==============================

We organize Python docstrings into sections that appear in a common order.

1. :ref:`Short Summary <py-docstring-short-summary>`
2. :ref:`Deprecation Warning <py-docstring-deprecation>` (if applicable)
3. :ref:`Extended Summary <py-docstring-extended-summary>` (optional)
4. :ref:`Parameters <py-docstring-parameters>` (if applicable; for classes, methods and functions)
5. :ref:`Methods <py-docstring-methods>` (if applicable; for classes)
6. :ref:`Attributes <py-docstring-attributes>` (if applicable; for classes)
7. :ref:`Returns <py-docstring-returns>` or `Yields <py-docstring-yields>` (if applicable; for functions, methods, and generators)
8. :ref:`Other Parameters <py-docstring-other-parameters>` (if applicable; for classes, methods and functions)
9. :ref:`Raises <py-docstring-raises>` (if applicable)
10. :ref:`See Also <py-docstring-see-also>` (optional)
11. :ref:`Notes <py-docstring-notes>` (optional)
12. :ref:`References <py-docstring-references>` (optional)

In the following sections we describe the content of these docstring sections provides examples of full docstrings composed for classes, methods, functions, and constants.  

.. _py-docstring-short-summary:

Short Summary
-------------

A one-line summary that does not use variable names or the function name:

.. code-block:: python

   def add(a, b):
       """Sum two numbers."""
       return a + b

For very simple objects the one line summary can be used alone.
Keep in mind our `style guideline for placing the short summary on the same line as the opening (and closing, if used alone) docstring delimiters <py-docstring-basics>`_.

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

*For functions and methods.*

*Parameters* is a description of the function arguments, keywords and their respective types.

.. code-block:: rst

   Parameters
   ----------
   x : type
      Description of parameter `x`.

Notice that the description is indented by three spaces from the ``{name} : {type}`` line of each argument.
If the descriptions spans more than one line, the continuation lines must be indented to the same level.

Arguments should be listed in the same order as they appear in the function signature.

When describing argument in the description, enclose the name of the variable in single backticks.

Parameter Types
^^^^^^^^^^^^^^^

For the parameter types, be as precise as possible.

.. code-block:: rst

   Parameters
   ----------
   filename : str
   copy : bool
   dtype : data-type
   iterable : iterable object
   shape : int or tuple of int
   files : list of str

For instances of classes, provide the full namespace to the class.

When a parameter can only assume one of a fixed set of values, those values can be listed in braces:

.. code-block:: rst

   order : {'C', 'F', 'A'}
      Description of `order`.

Optional Parameters
^^^^^^^^^^^^^^^^^^^

If it is not necessary to specify a keyword argument, use ``optional``:

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

If a class has a very large number of methods, which are hard to discover, an additonal *Methods* section *can* be provided to list them:

.. code-block:: rst

   Methods
   -------
   read(filename)
      Read a table from a file
   sort(column, order='ascending')
      Sort by `column`

Do not list private methods in the Methods section.
If it is necessary to explain a private method (use with care!), it can be referred to in the :ref:`extended summary <py-docstring-extended-summary>` or the :ref:`notes`.

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
   InvalidWCSException
      If the WCS information is invalid.

This section should be used judiciously---only for errors that are non-obvious or have a large chance of getting raised.

.. _py-docstring-see-also:

See Also
--------

*See Also* is an optional section used to refer to related code.
This section can be very useful, but should be used judiciously.
The goal is to direct users to other functions they may not be aware of, or have easy means of discovering (by looking at the module docstring, for example).
Routines whose docstrings further explain parameters used by this function are good candidates.

As an example, for a hypothetical function ``astropy.wcs.world2pix``
converting sky to pixel coordinates, we would have

.. code-block:: rst

   See Also
   --------
   pix2world : Convert pixel to sky coordinates

When referring to functions in the same sub-module, no prefix is needed, and the tree is searched upwards for a match.

Prefix functions from other sub-modules appropriately.
E.g., whilst documenting a hypothetical ``astropy.vo`` module, refer to a function in ``table`` by

.. code-block:: rst

   table.read : Read in a VO table

When referring to an entirely different module

.. code-block:: rst

   astropy.coords : Coordinate handling routines

Functions may be listed without descriptions, and this is preferable if the functionality is clear from the function name:

.. code-block:: rst

   See Also
   --------
   func_a : Function a with its description.
   func_b, func_c_, func_d
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

   >>> astropy.wcs.world2pix(233.2, -12.3)
   (134.5, 233.1)

   Comment explaining the second example

   >>> astropy.coords.fk5_to_gal("00:42:44.33 +41:16:07.5")
   (121.1743, -21.5733)

For tests with a result that is random or platform-dependent, mark the output as such:

.. code-block:: rst

   >>> astropy.coords.randomize_position(244.9, 44.2, radius=0.1)
   (244.855, 44.13)  # random

It is not necessary to use the doctest markup ``<BLANKLINE>`` to indicate empty lines in the output.

.. The examples may assume that ``import numpy as np`` is executed before the example code.

Documenting Methods and Functions
=================================

Documenting Classes
===================

Documenting constants
=====================

Documenting Modules
===================

Acknowledgements
================

These docstring guidelines are derived/adapted from in the `Numpy <https://github.com/numpy/numpy/blob/master/doc/HOWTO_DOCUMENT.rst.txt>`_ and `Astropy <http://docs.astropy.org/en/stable/_sources/development/docrules.txt>`_ documentation.

Numpy is Copyright © 2005-2013, NumPy Developers.

Astropy is Copyright (c) 2011-2015, Astropy Developers.
