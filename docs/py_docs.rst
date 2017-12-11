.. note::
   Changes to this document must be approved by the System Architect (`RFC-24 <https://jira.lsstcorp.org/browse/RFC-24>`_).
   To request changes to these standards, please file an :ref:`RFC <decision-making-rfc>`.

#######################################
Documenting Python APIs with Docstrings
#######################################

We use Python docstrings to create reference documentation for our Python APIs.
Docstrings are read by developers, interactive Python users, and readers of our online documentation.
This page describes how to write these docstrings in Numpydoc, DM's standard format:

- :ref:`py-docstring-basics`.
- :ref:`py-docstring-placement`.
- :ref:`py-docstring-rst`.
- :ref:`py-docstring-sections`.
- :ref:`py-docstring-module-structure`.
- :ref:`py-docstring-class-structure`.
- :ref:`py-docstring-method-function-structure`.
- :ref:`py-docstring-attribute-constants-structure`.

Treat the guidelines on this page as an extension of the :doc:`../coding/python_style_guide`.

.. _py-docstring-basics:

Basic Format of Docstrings
==========================

Python docstrings are special strings that form the ``__doc__`` attributes attached to modules, classes, methods and functions.
Docstrings are specified by :pep:`257`.

.. _py-docstring-triple-double-quotes:

Docstrings MUST be delimited by triple double quotes
----------------------------------------------------

Docstrings **must** be delimited by triple double quotes: ``"""``.
This allows docstrings to span multiple lines.
You may use ``u"""`` for unicode but it is usually preferable to stick to ASCII.

For consistency, *do not* use triple single quotes: ``'''``.

.. _py-docstring-form:

Docstrings SHOULD begin with ``"""`` and terminate with ``"""`` on its own line
----------------------------------------------------------------------------------

The docstring's summary sentence occurs on the same line as the opening ``"""``.

The terminating ``"""`` should be on its own line, even for 'one-line' docstrings (this is a minor departure from :pep:`257`).
For example, a one-line docstring:

.. code-block:: py

   """Sum numbers in an array.
   """

(*Note:* one-line docstrings are rarely used for public APIs, see :ref:`py-docstring-sections`.)

An example of a multi-paragraph docstring:

.. code-block:: py

   """Sum numbers in an array.

   Parameters
   ----------
   values : iterable
      Python iterable whose values are summed.

   Returns
   -------
   sum : `float`
      Sum of `values`.
   """

.. _py-docstring-blank-lines:

Docstrings of methods and functions SHOULD NOT be preceded or followed by a blank line
--------------------------------------------------------------------------------------

Inside a function or method, there should be no blank lines surrounding the docstring.

.. code-block:: py

   def sum(values):
       """Sum numbers in an array.

       Parameters
       ----------
       values : iterable
          Python iterable whose values are summed.

       Returns
       -------
       sum : `float`
          Sum of `values`.
       """
       pass

.. _py-docstring-class-blank-lines:

Docstrings of classes SHOULD be followed, but not preceded, by a blank line
---------------------------------------------------------------------------

Like method and function docstrings, the docstring should immediately follow the class definition, without a blank space.
However, there should be a **single blank line before following code** such as class variables or the ``__init__`` method.

.. code-block:: py

   class Point(object):
       """Point in a 2D cartesian space.

       Parameters
       ----------
       x, y : `float`
          Coordinate of the point.
       """

       def __init__(x, y):
           self.x = x
           self.y = y

.. _py-docstring-indentation:

Docstring content MUST be indented with the code's scope
--------------------------------------------------------

For example:

.. code-block:: py

   def sum(values):
       """Sum numbers in an array.

       Parameters
       ----------
       values : iterable
          Python iterable whose values are summed.
       """
       pass

Not:

.. code-block:: py

   def sum(values):
       """Sum numbers in an array.

   Parameters
   ----------
   values : iterable
      Python iterable whose values are summed.
   """
       pass

.. _py-docstring-placement:

Docstring Placement
===================

.. _py-docstring-module-placement:

Modules
-------

Module-level docstrings must be placed as close to the top of the Python file as possible: *below* any ``#!/usr/bin/env python`` and license statements, but *above* imports.
See also: :ref:`style-guide-py-file-order`.

Module docstrings should not be indented.
For example:

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

.. _py-docstring-class-method-function-placement:

Classes, Methods, and Functions
-------------------------------

Class/method/function docstrings must be placed directly below the declaration, and indented according to the code scope.

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

Note that the class docstring takes the place of a docstring for the ``__init__`` method; ``__init__`` has no docstring.

.. _py-docstring-rst:

ReStructuredText in Docstrings
==============================

We use reStructuredText to mark up and give semantic meaning to text in docstrings.
ReStructuredText is lightweight enough to read in raw form, such as command line terminal printouts, but is also parsed and rendered with our Sphinx-based documentation build system.
All of the style guidance for using reStructuredText from our :doc:`rst_styleguide` applies in docstrings with a few exceptions defined here.

.. _py-docstring-nospace-headers:

No space between headers and paragraphs
---------------------------------------

For docstrings, the Numpydoc_ standard is to omit any space between a header and the following paragraph.

For example

.. code-block:: python

   """A summary

   Notes
   -----
   The content of the notes section directly follows the header, with no blank line.
   """

This :ref:`deviation from the normal style guide <rst-sectioning>` is in keeping with Python community idioms and to save vertical space in terminal help printouts.

.. _py-docstring-section-levels:

Sections are restricted to the Numpydoc section set
---------------------------------------------------

Sections must be from the set of standard Numpydoc sections (see :ref:`py-docstring-sections`).
You cannot introduce new section headers, or use the :ref:`full reStructuredText subsection hierarchy <rst-sectioning>`, since these subsections won't be parsed by the documentation toolchain.

Always use the dash (``-``) to underline sections.
For example:

.. code-block:: python

   def myFunction(a):
       """Do something.

       Parameters
       ----------
       [...]

       Returns
       -------
       [...]

       Notes
       -----
       [...]
       """

.. _py-docstring-subsections:

Simulate subsections with bold text
-----------------------------------

Conventional reStructuredText subsections are not allowed in docstrings, given the :ref:`previous guideline <py-docstring-section-levels>`.
However, you may structure long sections with bold text that simulates subsection headers.
This technique is useful for the :ref:`Notes <py-docstring-notes>` and :ref:`Examples <py-docstring-examples>` Numpydoc sections.
For example:

.. code-block:: python

   def myFunction(a):
       """Do something.

       [...]

       Examples
       --------
       **Example 1**

       [...]

       **Example 2**

       [...]
       """

.. _py-docstring-length:

Line Lengths
------------

Hard-wrap text in docstrings to match the :ref:`line length allowed by the coding standard <style-guide-py-line-length>`.

.. note::

   In the future we may require shorter line lengths specifically for docstrings.
   See :jira:`RFC-107`.

.. _py-docstring-sections:

Numpydoc Sections in Docstrings
===============================

We organize Python docstrings into sections that appear in a common order.
This format follows the `Numpydoc`_ format (used by NumPy, SciPy, and Astropy, among other scientific Python packages) rather than the format described in :pep:`287`.
The sections and their relative order is:

.. _Numpydoc: https://github.com/numpy/numpy/blob/master/doc/HOWTO_DOCUMENT.rst.txt

1. :ref:`Short Summary <py-docstring-short-summary>`
2. :ref:`Deprecation Warning <py-docstring-deprecation>` (if applicable)
3. :ref:`Extended Summary <py-docstring-extended-summary>` (optional)
4. :ref:`Parameters <py-docstring-parameters>` (if applicable; for classes, methods, and functions)
5. :ref:`Returns <py-docstring-returns>` or :ref:`Yields <py-docstring-yields>` (if applicable; for functions, methods, and generators)
6. :ref:`Other Parameters <py-docstring-other-parameters>` (if applicable; for classes, methods, and functions)
7. :ref:`Raises <py-docstring-raises>` (if applicable)
8. :ref:`See Also <py-docstring-see-also>` (optional)
9. :ref:`Notes <py-docstring-notes>` (optional)
10. :ref:`References <py-docstring-references>` (optional)
11. :ref:`Examples <py-docstring-examples>` (optional)

For summaries of how these docstring sections are composed in specific contexts, see:

- :ref:`py-docstring-module-structure`
- :ref:`py-docstring-class-structure`
- :ref:`py-docstring-method-function-structure`
- :ref:`py-docstring-attribute-constants-structure`
- :ref:`py-docstring-property-structure`

.. _py-docstring-short-summary:

Short Summary
-------------

A one-line summary that does not use variable names or the function's name:

.. code-block:: python

   def add(a, b):
       """Sum two numbers.
       """
       return a + b

For functions and methods, the summary should be written in the imperative voice (i.e., as a command that the API consumer is giving).

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
This section should be used to clarify *functionality*, not to discuss implementation detail or background theory, which should rather be explored in the :ref:`'Notes' <py-docstring-notes>` section below.
You may refer to the parameters and the function name, but parameter descriptions still belong in the :ref:`'Parameters' <py-docstring-parameters>` section.

.. _py-docstring-parameters:

Parameters
----------

*For functions, methods and classes.*

'Parameters' is a description of a function or method's arguments and their respective types.
Arguments should be listed in the same order as they appear in the function or method signature.

For example:

.. code-block:: python

   def calcDistance(x, y, x0=0., y0=0.):
       """Calculate the distance between two points.

       Parameters
       ----------
       x : `float`
           X-axis coordinate.
       y : `float`
           Y-axis coordinate.
       x0 : `float`, optional
           X-axis coordinate for the second point (the origin, by default).
       y0 : `float`, optional
           Y-axis coordinate for the second point (the origin, by default).
       
       [...]
       """

Each parameter is declared with a line formatted as ``{name} : {type}`` that is justified to the docstring.
A single space is required before and after the colon (``:``).
The ``name`` corresponds to the variable name in the function or method's arguments.
The ``type`` is described below (:ref:`py-docstring-parameter-types`).
The description is indented by **four** spaces relative to the docstring and appears without a preceding blank line.

Normally parameters are documented consecutively, without blank lines between (see the earlier example).
However, if the descriptions of an individual parameter span multiple paragraphs, or include lists, then you must separate each parameter with a blank line.
For example:

.. code-block:: rst

   Parameters
   ----------
   output_path : `str`
       Filepath where the plot will be saved.

   plot_settings : `dict`, optional
       Settings for the plot that may include these fields:

       - ``'dpi'``: resolution of the plot in dots per inch (`int`).
       - ``'rasterize'``: if `True`, then rasterize the plot. `False` by default.

.. _py-docstring-parameter-types:

Describing Parameter Types
^^^^^^^^^^^^^^^^^^^^^^^^^^

Be as precise as possible when describing parameter types.
The type description is free-form text, making it possible to list several supported types or indicate nuances.
Complex and lengthy type descriptions can be partially moved to the parameter's *description* field.
The following sections will help you deal with the different kinds of types commonly seen.

Concrete types
""""""""""""""

Wrap concrete types in backticks (in docstrings, single backticks are equivalent to ``:py:obj:``) to make a link to either an internal API or an external API that is supported by `intersphinx <http://www.sphinx-doc.org/en/stable/ext/intersphinx.html>`_.
This works for both built-in types and most importable objects:

.. code-block:: rst

   Parameters
   ----------
   filename : `str`
       [...]
   n : `int`
       [...]
   verbose : `bool`
       [...]
   items : `list` or `tuple`
       [...]
   magnitudes : `numpy.ndarray`
       [...]
   struct : `lsst.pipe.base.Struct`
       [...]

In general, provide the full namespace to the object, such as ```lsst.pipe.base.Struct```.
It may be possible to reference objects in the same namespace as the current module without any namespace prefix.
Always check the compiled documentation site to ensure the link worked.

Choices
"""""""

When a parameter can only assume one of a fixed set of values, those choices can be listed in braces:

.. code-block:: rst

   order : {'C', 'F', 'A'}
       [...]

Sequence types
""""""""""""""

When a type is a sequence container (like a `list` or `tuple`), you can describe the type of the contents.
For example:

.. code-block:: rst

   mags : `list` of `float`
       Sequence of magnitudes.

Dictionary types
""""""""""""""""

For dictionaries it is usually best to document the keys and their values in the parameter's description:

.. code-block:: rst

   settings : `dict`
       Settings dictionary with fields:

       - ``color``: Hex colour code (`str`).
       - ``size``: Point area in pixels (`float`).

Array types
"""""""""""

For Numpy arrays, try to include the dimensionality:

.. code-block:: rst

   coords : `numpy.ndarray`, (N, 2) 
       [...]
   flags : `numpy.ndarray`, (N,)
       [...]
   image : `numpy.ndarray`, (Ny, Nx)
       [...]

Choose conventional variables or labels to describe dimensions, like ``N`` for the number of sources or ``Nx, Ny`` for rectangular dimensions.

Callable types
""""""""""""""

For callback functions, describe the type as ``callable``:

.. code-block:: rst

   likelihood : callable
       Likelihood function that takes two positional arguments:

       - ``x``: current parameter (`float`).
       - ``extra_args``: additional arguments (`dict`).

.. _py-docstring-optional:

Optional Parameters
^^^^^^^^^^^^^^^^^^^

For keyword arguments with useful defaults, add ``optional`` to the type specification:

.. code-block:: rst

   x : `int`, optional

Optional keyword parameters have default values, which are automatically documented as part of the function or method's signature.
You can also explain defaults in the description:

.. code-block:: rst

   x : `int`, optional
       Description of parameter ``x`` (the default is -1, which implies summation
       over all axes).

.. _py-docstring-shorthand:

Shorthand
^^^^^^^^^

When two or more consecutive input parameters have exactly the same type, shape and description, they can be combined:

.. code-block:: rst

   x1, x2 : array-like
       Input arrays, description of `x1`, `x2`.

.. _py-docstring-returns:

Returns
-------

*For functions and methods*.

'Returns' is an explanation of the returned values and their types, in the same format as :ref:`'Parameters' <py-docstring-parameters>`.

If a sequence of values is returned, each value may be separately listed, in order:

.. code-block:: python

   def getCoord(self):
       """Get the point's pixel coordinate.

       Returns
       -------
       x : `int`
           X-axis pixel coordinate.
       y : `int`
           Y-axis pixel coordinate.
       """
       return self._x, self._y

If a return type is `dict`, ensure that the key-value pairs are documented in the description:

.. code-block:: python

   def getCoord(self):
       """Get the point's pixel coordinate.

       Returns
       -------
       pixelCoord : `dict`
          Pixel coordinates with fields:

          - ``x``: x-axis coordinate (`int`).
          - ``y``: y-axis coordinate (`int`).
        """
        return {'x': self._x, 'y': self._y}

Note that the names of the returned variables do not necessarily correspond to the names of variables.
In the previous examples, the variables ``x``, ``y``, and ``pixelCoord`` never existed in the method scope.
Simply choose a variable-like name that is clear.
Order is important.

If a returned variable is named in the method or function scope, you will usually want to use that name for clarity.
For example:

.. code-block:: python

   def getDistance(self, x, y):
       """Compute the distance of the point to an (x, y) coordinate.

       [...]

       Returns
       -------
       distance : `float`
           Distance, in units of pixels.
       """
       distance = np.hypot(self._x - x, self._y - y)
       return distance

.. _py-docstring-yields:

Yields
------

*For generators.*

'Yields' is used identically to :ref:`'Returns' <py-docstring-yields>`, but for generators.
For example:

.. code-block:: python

   def items(self):
       """Iterate over items in the container.

       Yields
       ------
       key : `str`
           Item key.
       value : obj
           Item value.
       """
       for key, value in self._data.items():
           yield key, value

.. _py-docstring-other-parameters:

Other Parameters
----------------

*For classes, methods and functions.*

'Other Parameters' is an optional section used to describe infrequently used parameters.
It should only be used if a function has a large number of keyword parameters, to prevent cluttering the :ref:`Parameters <py-docstring-parameters>` section.

.. _py-docstring-raises:

Raises
------

*For classes, methods and functions.*

'Raises' is an optional section detailing which errors get raised and under what conditions:

.. code-block:: rst

   Raises
   ------
   `IOError`
       If the file could not be read.

This section should be used judiciously---only for errors that are non-obvious or have a large chance of getting raised.

.. _py-docstring-see-also:

See Also
--------

Use the 'See also' section to link to related APIs that the user may not be aware of, or may not easily discover from other parts of the docstring.
Here are some good uses of the 'See also' section:

- If a function wraps another function, you may want to reference the lower-level function.
- If a function is typically used with another API, you can reference that API.
- If there is a family of closely related APIs, you might link to others in the family so a user can compare and choose between them easily.

As an example, for a function such as ``numpy.cos``, we would have:

.. code-block:: rst

   See also
   --------
   sin
   tan

Numpydoc assumes that the contents of the 'See also' section are API names, so don't wrap each name with backticks, as we do when describing types in :ref:`Parameters <py-docstring-parameters>` and :ref:`Returns <py-docstring-returns>`).
No namespace prefix is needed when referring to functions in the same module.
Providing the full namespace is always safe, though, and provides clarity to fellow developers:

.. code-block:: rst

   See also
   --------
   numpy.sin
   numpy.tan
   
.. _py-docstring-notes:

Notes
-----

*Notes* is an optional section that provides additional information about the code, possibly including a discussion of the algorithm.
This section may include mathematical equations, written in `LaTeX <http://www.latex-project.org/>`_ format:

.. code-block:: rst

  The FFT is a fast implementation of the discrete Fourier transform:

  .. math:: X(e^{j\omega } ) = x(n)e^{ - j\omega n}

Longer equations can also be typeset underneath the math directive:

.. code-block:: rst

  The discrete-time Fourier time-convolution property states that

  .. math::

     x(n) * y(n) \Leftrightarrow X(e^{j\omega } )Y(e^{j\omega } )\\
     another equation here

Math can also be used inline:

.. code-block:: rst

   The value of :math:`\omega` is larger than 5.

Variable names are displayed in typewriter font, obtained by using ``\mathtt{var}``:

.. code-block:: rst

   We square the input parameter `alpha` to obtain
   :math:`\mathtt{alpha}^2`.

See :ref:`rst-math` for more details on math typesetting in reStructuredText.

Note that LaTeX is not particularly easy to read, so use equations sparingly.

Images are allowed, but should not be central to the explanation; users viewing the docstring as text must be able to comprehend its meaning without resorting to an image viewer.
These additional illustrations are included using:

.. code-block:: rst

   .. image:: filename

where filename is a path relative to the reference guide source directory.

.. _py-docstring-references:

References
----------

References cited in the :ref:`'Notes' <py-docstring-notes>` section may be listed here, e.g. if you cited the article below using the text ``[1]_``, include it as in the list as follows:

.. code-block:: rst

   .. [1] O. McNoleg, "The integration of GIS, remote sensing,
      expert systems and adaptive co-kriging for environmental habitat
      modelling of the Highland Haggis using object-oriented, fuzzy-logic
      and neural-network techniques," Computers & Geosciences, vol. 22,
      pp. 585-588, 1996.

Note that Web pages should be referenced with regular inline links.

References are meant to augment the docstring, but should not be required to understand it.
References are numbered, starting from one, in the order in which they are cited.

We may support `bibtex-based references instead <https://github.com/mcmtroffaes/sphinxcontrib-bibtex>`__ instead of explicitly writing bibliographies in docstrings.

.. _py-docstring-examples:

Examples
--------

'Examples' is an optional section for examples, using the `doctest <http://docs.python.org/library/doctest.html>`_ format.
These examples do not replace unit tests, but *are* intended to be tested to ensure documentation and code are consistent.
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

.. _py-docstring-module-structure:

Documenting Modules
===================

Module docstrings are placed *after* the boilerplate and before any imports or other code.
Module docstrings contain the following sections:

1. :ref:`Short Summary <py-docstring-short-summary>`
2. :ref:`Deprecation Warning <py-docstring-deprecation>` (if applicable)
3. :ref:`Extended Summary <py-docstring-extended-summary>` (optional)
4. :ref:`See Also <py-docstring-see-also>` (optional)

.. note::

   Module docstrings aren't featured heavily in the documentation we generate and publish with Sphinx.
   Avoid putting important end-user documentation in module docstrings.
   Instead, write introductory and overview documentation in the module's *user guide* (the :file:`doc/` directories of Stack packages).

   Module docstrings can still be useful for developer-oriented notes, though.

.. _py-docstring-class-structure:

Documenting Classes
===================

Class docstrings are placed directly after the class definition, and serve to document both the class as a whole *and* the arguments passed to the ``__init__`` constructor.
Class docstrings contain the following sections:

1. :ref:`Short Summary <py-docstring-short-summary>`
2. :ref:`Deprecation Warning <py-docstring-deprecation>` (if applicable)
3. :ref:`Extended Summary <py-docstring-extended-summary>` (optional)
4. :ref:`Parameters <py-docstring-parameters>` (if applicable)
5. :ref:`Other Parameters <py-docstring-other-parameters>` (if applicable)
6. :ref:`Raises <py-docstring-raises>` (if applicable)
7. :ref:`See Also <py-docstring-see-also>` (optional)
8. :ref:`Notes <py-docstring-notes>` (optional)
9. :ref:`References <py-docstring-references>` (optional)
10. :ref:`Examples <py-docstring-examples>` (optional)

Here's an example of a class:

.. code-block:: python

   class SkyCoordinate(object):
       """Equatorial coordinate on the sky as Right Ascension and Declination.

       Parameters
       ----------
       ra : `float`
          Right ascension (degrees).
       dec : `float`
          Declination (degrees).
       frame : {'icrs', 'fk5'}, optional
          Coordinate frame.

       Raises
       ------
       ValueError
           Raised when input angles are outside range.
       
       See also
       --------
       lsst.example.GalacticCoordinate

       Examples
       --------
       To define the coordinate of the M31 galaxy:

       >>> m31_coord = SkyCoordinate(10.683333333, 41.269166667)
       SkyCoordinate(10.683333333, 41.269166667, frame='icrs')
       """

       def __init__(self, ra, dec, frame='icrs'):
           pass

.. _py-docstring-method-function-structure:

Documenting Methods and Functions
=================================

Method and function docstrings contain the following sections:

1. :ref:`Short Summary <py-docstring-short-summary>`
2. :ref:`Deprecation Warning <py-docstring-deprecation>` (if applicable)
3. :ref:`Extended Summary <py-docstring-extended-summary>` (optional)
4. :ref:`Parameters <py-docstring-parameters>` (if applicable)
5. :ref:`Returns <py-docstring-returns>` or :ref:`Yields <py-docstring-yields>` (if applicable)
6. :ref:`Other Parameters <py-docstring-other-parameters>` (if applicable)
7. :ref:`Raises <py-docstring-raises>` (if applicable)
8. :ref:`See Also <py-docstring-see-also>` (optional)
9. :ref:`Notes <py-docstring-notes>` (optional)
10. :ref:`References <py-docstring-references>` (optional)
11. :ref:`Examples <py-docstring-examples>` (optional)

Here's an example function:

.. code-block:: python

   def check_unit(self, quantity):
       """Check that a `~astropy.units.Quantity` has equivalent units to
       this metric.

       Parameters
       ----------
       quantity : `astropy.units.Quantity`
           Quantity to be tested.

       Returns
       -------
       is_equivalent : `bool`
           `True` if the units are equivalent, meaning that the quantity
           can be presented in the units of this metric. `False` if not.

       See also
       --------
       astropy.units.is_equivalent

       Examples
       --------
       Check that a quantity in arcseconds is compatible with a metric defined in arcminutes:

       >>> import astropy.units as u
       >>> from lsst.verify import Metric
       >>> metric = Metric('example.test', 'Example', u.arcminute)
       >>> metric.check_units(1.*u.arcsecond)
       True

       But mags are not a compatible unit:

       >>> metric.check_units(21.*u.mag)
       False
       """
       if not quantity.unit.is_equivalent(self.unit):
           return False
       else:
           return True

.. _py-docstring-attribute-constants-structure:

Documenting Constants and Class Attributes
==========================================

Constants in modules and attributes in classes are all documented similarly.
At a minimum, they should have a summary line that includes the type.
They can also have a more complete structure with these sections:

1. :ref:`Short Summary <py-docstring-short-summary>`
2. :ref:`Deprecation Warning <py-docstring-deprecation>` (if applicable)
3. :ref:`Extended Summary <py-docstring-extended-summary>` (optional)
4. :ref:`Notes <py-docstring-notes>` (optional)
5. :ref:`References <py-docstring-references>` (optional)
6. :ref:`Examples <py-docstring-examples>` (optional)

For example:

.. code-block:: py

   NAME = 'LSST'
   """Name of the project (`str`)."""

Note:

- The docstring appears directly below the constant or class attribute.
- The type is included in parentheses at the end of the summary line.

Multi-section docstrings keep the type information in the summary line.
For example:

.. code-block:: py

   PA1_DESIGN = 5. * u.mmag
   """PA1 design specification (`astropy.units.Quantity`).

   Notes
   -----
   The PA1 metric [1]_ is defined so that the rms of the unresolved source
   magnitude distribution around the mean value (repeatability) will not
   exceed PA1 millimag (median distribution for a large number of sources).

   References
   ----------
   .. [1] Z. Ivezic and the LSST Science Collaboration. 2011, LSST Science
      Requirements Document, LPM-17, URL https://ls.st/LPM-17
   """

In many classes, public attributes are set in the ``__init__`` method.
The best way to document these public attributes is by declaring the attribute at the class level and including a docstring with that declaration:

.. code-block:: python

   class Metric(object):
       """Verification metric.

       [...]
       """

       name = None
       """Name of the metric (`str`)."""

       unit = None
       """Units of the metric (`astropy.units.Unit`)."""

       def __init__(name, unit):
           self.name = name
           self.unit = unit

Private attributes (prefixed by underscores: ``self._myAttribute``) do not need to be documented with docstrings.

.. _py-docstring-property-structure:

Documenting Class Properties
============================

Properties are documented like :ref:`class attributes <py-docstring-attribute-constants-structure>` rather than methods.
After all, properties are designed to appear to the user like simple attributes.

For example:

.. code-block:: python

   class Measurement(object):

       # ...

       @property
       def quantity(self):
           """The measurement quantity (`astropy.units.Quantity`).
           """
           # ...

       @quantity.setter
       def quantity(self, q):
           # ...

       @property
       def unit(self):
           """Units of the measurement (`astropy.units.Unit`, read-only).
           """
           # ...

Note:

- Do not use the :ref:`Returns section <py-docstring-returns>` in the property's docstring.
  Instead, include type information in the summary, as is done for :ref:`class attributes <py-docstring-attribute-constants-structure>`.
- Only document the property's "getter" method, not the "setter" (if present).
- If a property does not have a "setter" method, include the words ``read-only`` after the type information.

Acknowledgements
================

These docstring guidelines are derived/adapted from the `NumPy <https://github.com/numpy/numpy/blob/master/doc/HOWTO_DOCUMENT.rst.txt>`_ and `Astropy <http://docs.astropy.org/en/stable/_sources/development/docrules.txt>`_ documentation.

NumPy is Copyright © 2005-2013, NumPy Developers.

Astropy is Copyright © 2011-2015, Astropy Developers.
