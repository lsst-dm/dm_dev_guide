.. note::
   Changes to this document must be approved by the System Architect (`RFC-24 <https://jira.lsstcorp.org/browse/RFC-24>`_).
   To request changes to these standards, please file an :doc:`RFC </communications/rfc>`.

.. _numpydoc-format:

#######################################
Documenting Python APIs with docstrings
#######################################

We use Python docstrings to create reference documentation for our Python APIs.
Docstrings are read by developers, interactive Python users, and readers of our online documentation.
This page describes how to write these docstrings for LSST DM.

Although this style guide grew out of the `Numpydoc Style Guide`_, and DM docstrings are parsed by Numpydoc_, this style guide has small tweaks and clarifications compared to the original `Numpydoc Style Guide`_.
Always refer to this guide, rather than others, to learn how to write DM docstrings.
If you have any questions, ask in `#dm-docs <https://lsstc.slack.com/archives/dm-docs>`_ on Slack.

**Format reference:**

- :ref:`py-docstring-basics`.
- :ref:`py-docstring-rst`.
- :ref:`py-docstring-sections`.

  1. :ref:`Short summary <py-docstring-short-summary>`
  2. :ref:`Extended summary <py-docstring-extended-summary>`
  3. :ref:`Parameters <py-docstring-parameters>`
  4. :ref:`Returns <py-docstring-returns>` or :ref:`Yields <py-docstring-yields>`
  5. :ref:`Other Parameters <py-docstring-other-parameters>`
  6. :ref:`Raises <py-docstring-raises>`
  7. :ref:`See Also <py-docstring-see-also>`
  8. :ref:`Notes <py-docstring-notes>`
  9. :ref:`References <py-docstring-references>`
  10. :ref:`Examples <py-docstring-examples>`

**How to format different APIs:**

- :ref:`py-docstring-module-structure`.
- :ref:`py-docstring-class-structure`.
- :ref:`py-docstring-method-function-structure`.
- :ref:`py-docstring-attribute-constants-structure`.
- :ref:`py-docstring-property-structure`.

**Learn by example:**

- :ref:`py-docstring-example-module`.

Treat the guidelines on this page as an extension of the :doc:`style`.

.. _py-docstring-basics:

Basic format of docstrings
==========================

Python docstrings form the ``__doc__`` attributes attached to modules, classes, methods and functions.
See :pep:`257` for background.

.. _py-docstring-triple-double-quotes:

Docstrings MUST be delimited by triple double quotes
----------------------------------------------------

Docstrings **must** be delimited by triple double quotes: ``"""``.
This allows docstrings to span multiple lines.
In cases where the restructured text contains a backslash, it may be necessary to use a raw string with ``r"""``.

For consistency, *do not* use triple single quotes: ``'''``.

.. _py-docstring-form:

Docstrings SHOULD begin with ``"""`` and terminate with ``"""`` on its own line
-------------------------------------------------------------------------------

The docstring's :ref:`summary sentence <py-docstring-short-summary>` occurs on the same line as the opening ``"""``.

The terminating ``"""`` should be on its own line except for one-line docstrings.
If the docstring is a single line, the terminating ``"""`` may be either on the same line or on its own line.
(Be aware that :pep:`257` requires that it be on the same line and `black`_ will enforce this rule.)

.. _black: https://github.com/psf/black

.. code-block:: py

   """Sum numbers in an array.
   """

or:

.. code-block:: py

   """Sum numbers in an array."""

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
      Sum of ``values``.
   """

.. _py-docstring-blank-lines:

Docstrings of methods and functions SHOULD NOT be preceded or followed by a blank line
--------------------------------------------------------------------------------------

Inside a function or method, there should be no blank lines surrounding the docstring:

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
          Sum of ``values``.
       """
       pass

.. _py-docstring-class-blank-lines:

Docstrings of classes SHOULD be followed, but not preceded, by a blank line
---------------------------------------------------------------------------

Like method and function docstrings, the docstring should immediately follow the class definition, without a blank space.
However, there should be a **single blank line before following code** such as class variables or the ``__init__`` method:

.. code-block:: py

   class Point(object):
       """A point in a 2D cartesian space.

       Parameters
       ----------
       x, y : `float`
          The point's coordinate.
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

.. _py-docstring-rst:

ReStructuredText in docstrings
==============================

We use reStructuredText to mark up and give semantic meaning to text in docstrings.
ReStructuredText is lightweight enough to read in raw form, such as command line terminal printouts, but is also parsed and rendered with our Sphinx-based documentation build system.
All of the style guidance for using reStructuredText from our :doc:`/restructuredtext/style` applies in docstrings with a few exceptions defined here.

.. _py-docstring-nospace-headers:

No space between headers and paragraphs
---------------------------------------

For docstrings, the Numpydoc_ standard is to omit any space between a header and the following paragraph.

For example

.. code-block:: python

   """A summary sentence.

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

Line lengths
------------

Hard-wrap text in docstrings to match the :ref:`docstring line length allowed by the coding standard <style-guide-py-docstring-line-length>`.

.. _py-docstring-parameter-markup:

Marking up parameter names
--------------------------

The default reStructuredText role in docstrings is ``:py:obj:``.
Sphinx automatically generates links when the API names are marked up in single backticks.
For example: ```str``` or ```lsst.pipe.base.Struct```.

You cannot use this role to mark up parameters, however.
Instead, use the code literal role (double backticks) to mark parameters and return variables in monospace type.
For example, the description for ``format`` references the ``should_plot`` parameter:

.. code-block:: rst

   Parameters
   ----------
   should_plot : `bool`
       Plot the fit if `True`.
   plot_format : `str`, optional
       Format of the plot when ``should_plot`` is `True`.

.. _py-docstring-sections:

Numpydoc sections in docstrings
===============================

We organize Python docstrings into sections that appear in a common order.
This format is based on the original `Numpydoc Style Guide`_ (used by NumPy, SciPy, and Astropy, among other scientific Python packages), though this style guide includes several DM-specific clarifications.
These are the sections and their relative order:

1. :ref:`Short summary <py-docstring-short-summary>`
2. :ref:`Extended summary <py-docstring-extended-summary>` (optional)
3. :ref:`Parameters <py-docstring-parameters>` (if applicable; for classes, methods, and functions)
4. :ref:`Returns <py-docstring-returns>` or :ref:`Yields <py-docstring-yields>` (if applicable; for functions, methods, and generators)
5. :ref:`Other Parameters <py-docstring-other-parameters>` (if applicable; for classes, methods, and functions)
6. :ref:`Raises <py-docstring-raises>` (if applicable)
7. :ref:`See Also <py-docstring-see-also>` (optional)
8. :ref:`Notes <py-docstring-notes>` (optional)
9. :ref:`References <py-docstring-references>` (optional)
10. :ref:`Examples <py-docstring-examples>` (optional)

.. important::

   These sections — including names, capitalizations, and relative order — are highly prescribed by the Numpydoc standard and the tooling that works in that ecosystem including documentation builders (Sphinx) and linters (pydocstyle).
   You cannot add custom sections.
   Also note that the sections are title cased (e.g. "See Also"), as opposed to the sentence casing recommended otherwise in our :ref:`user-doc-style-guide`.

For summaries of how these docstring sections are composed in specific contexts, see:

- :ref:`py-docstring-module-structure`
- :ref:`py-docstring-class-structure`
- :ref:`py-docstring-method-function-structure`
- :ref:`py-docstring-attribute-constants-structure`
- :ref:`py-docstring-property-structure`

.. _py-docstring-short-summary:

Short summary
-------------

All docstrings begin with a one-sentence summary:

.. code-block:: python
   :emphasize-lines: 2

   def add(a, b):
       """Sum two numbers.

       Parameters
       ----------
       a, b : `float`
           The numbers to add together.

       Returns
       -------
       sum : `float`
           The sum of ``a`` and ``b``.
       """
       return a + b

The summary sentence can wrap across multiple lines (see also :ref:`py-docstring-length`):

.. code-block:: python
   :emphasize-lines: 2-3

   def sumif(sequence, conditional)
       """Sum the numbers in a sequence as long as they pass a
       user-provided conditional callback function.

       Parameters
       ----------
       sequence : `list` [`float`]
           A sequence (`list`, for example) of numbers.
       conditional : callable
           A callback function that takes a single number as an
           argument. The ``conditional`` function returns `True`
           if the number passes the conditional, and `False`
           otherwise.

       Returns
       -------
       sum : `float`
           The sum of numbers that meet the conditional.
       """
       total = 0
       for n in sequence:
           if conditional(n):
               total += n
        return total

Do not write multiple sentences in the *Short summary*, however.
If additional content is needed to clarify the *Short summary,* consider adding an :ref:`Extended summary <py-docstring-extended-summary>` section.


On API and parameter names in summary sentences
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Do not repeat the name of the class, method, function, or attribute in the summary sentence.
This information is already clear from the context.

As well, it's best to not repeat the names of parameters in the summary sentence.
The summary sentence is often seen in API listings where individual parameters may be truncated from the displayed API signature.
Write the summary in plain English and in a way that is as self-contained as practical (aside from the implicit context of the API name and the name of the parent class).
If the English word is the same as the parameter name then it's fine to use that word in the summary sentence; don't display the word as a code literal, though.

Writing summaries for functions and methods
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

For functions and methods, write in the imperative voice.
That is, the summary is treated as a command that the API consumer can give.

Some examples:

- .. code-block:: python
     :emphasize-lines: 2

     def getMetadata(self):
         """Get metadata for all tasks.

         Returns
         -------
         metadata : `lsst.pipe.base.Struct`
             The metadata.
         """

- .. code-block:: python
     :emphasize-lines: 2

     def makeRegistry(doc, configBaseType=Config):
         """Create a `Registry`.

         Parameters
         ----------
         doc : `str`
             Docstring for the created `Registry` (this is set as the ``__doc__``
             attribute of the `Registry` instance.
         configBaseType : `lsst.pex.config.Config`-type
             Base type of config classes in the `Registry`
             (`lsst.pex.config.Registry.configBaseType`).

         Returns
         -------
         registry : `Registry`
             Registry with ``__doc__`` and `~Registry.configBaseType` attributes
             set.
         """

Writing summaries for classes
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

State what the class *is* through its summary sentence.

Examples:

- .. code-block:: python
     :emphasize-lines: 2-4

     class Job:
         """A container for measurements, blobs, and metadata associated
         with a pipeline run.
         """

- .. code-block:: python
     :emphasize-lines: 2-4

     class Field:
         """A field in a `~lsst.pex.config.Config` class that supports `int`,
         `float`, `complex`, `bool`, and `str` data types.
         """

Additional tips:

- Don't repeat the class name in the summary sentence.
- Don't write "This class..."

.. _py-docstring-extended-summary:

Extended summary
----------------

The extended summary is an optional sentence or short paragraph that clarifies and supports the :ref:`summary sentence <py-docstring-short-summary>`.
Taken together with the summary sentence, the summary content in general exists to help users quickly understand the role and scope of the API.

Leave detailed discussions of the API's features, usage patterns, background theory, and implementation details to the :ref:`Notes <py-docstring-notes>` and :ref:`Examples <py-docstring-examples>` sections.
The :ref:`Parameters <py-docstring-parameters>` and :ref:`Returns <py-docstring-returns>` sections are ideal places to discuss in detail individual parameters and returned values, respectively.

This section's brevity is critical.
The extended summary is proximate to the summary sentence so that the two pieces of content support each other.
However, the extended summary also separates the API signature from the :ref:`Parameters <py-docstring-parameters>` section, which users expect to see close together.
As a general guideline, the extended summary should be three sentences or fewer.

.. _py-docstring-parameters:

Parameters
----------

*For functions, methods and classes.*

'Parameters' is a description of a function or method's arguments and their respective types.
Parameters should be listed in the same order as they appear in the function or method signature.

For example:

.. code-block:: python

   def calcDistance(x, y, x0=0., y0=0., **kwargs):
       """Calculate the distance between two points.

       Parameters
       ----------
       x : `float`
           X-axis coordinate.
       y : `float`
           Y-axis coordinate.
       x0 : `float`, optional
           X-axis coordinate for the second point (the origin,
           by default).

           Descriptions can have multiple paragraphs, and lists:

           - First list item.
           - Second list item.
       y0 : `float`, optional
           Y-axis coordinate for the second point (the origin,
           by default).
       **kwargs
           Additional keyword arguments passed to
           `calcExternalApi`.
       """

Formatting tips:

- Each parameter is declared with a line formatted as ``{name} : {type}`` that is justified to the docstring.
- A single space is required before and after the colon (``:``).
- The ``name`` corresponds to the variable name in the function or method's arguments.
- The ``type`` is discussed in :ref:`py-docstring-parameter-types`).
- The description is indented by **four** spaces relative to the docstring and appears without a preceding blank line.
  Descriptions can have multiple lines, and even multiple paragraphs, lists, and definition lists.
  Ensure that all of the content in a description is aligned with respect to the **first line** of the description content.
  See the ``x0`` parameter in the example, above.
- Normally parameters are documented consecutively, without blank lines between.

.. _py-docstring-parameter-types:

Describing parameter types
^^^^^^^^^^^^^^^^^^^^^^^^^^

Be as precise as possible when describing parameter types.
The type description is free-form text, making it possible to list several supported types or indicate nuances.
Complex and lengthy type descriptions can be partially moved to the parameter's *description* field.
The following sections will help you deal with the different kinds of types commonly seen:

- :ref:`py-docstring-parameter-types-concrete`
- :ref:`py-docstring-parameter-types-choices`
- :ref:`py-docstring-parameter-types-sequences`
- :ref:`py-docstring-parameter-types-dict`
- :ref:`py-docstring-parameter-types-struct`
- :ref:`py-docstring-parameter-types-array`
- :ref:`py-docstring-parameter-types-callable`

.. _py-docstring-parameter-types-concrete:

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
The ``.`` prefix denotes the current module, and it may be possible to reference objects in the same package as the current type or function without any namespace prefix at all.
Always check the compiled documentation site to ensure the link worked.

.. note::

   Unqualified links to types are evaluated relative to the *package* in which the linking object is documented, not the module file in which the docstring is written.
   In particular, importing a type into a module does not let you use unqualified links to that type from module code.


.. _py-docstring-parameter-types-choices:

Choices
"""""""

When a parameter can only assume one of a fixed set of values, those choices can be listed in braces:

.. code-block:: rst

   order : {'C', 'F', 'A'}
       [...]

.. _py-docstring-parameter-types-sequences:

Sequence types
""""""""""""""

When a type is a sequence container (like a `list` or `tuple`), you can describe the type of the contents using a :pep:`484`-like syntax.
For example:

.. code-block:: rst

   mags : `list` [`float`]
       A sequence of magnitudes.

The type inside the brackets is the type of each item.

.. warning::

   Ensure that you place a space between the container type and the bracket that wraps the item type.
   Don't do:

   .. code-block:: rst

      `list`[`float`]

   Instead, do:

   .. code-block:: rst

      `list` [`float`]

   Leaving out the space results in a parsing error.

If the type of the sequence's items isn't known, leave out the item typing and explain with the description:

.. code-block:: rst

   items : `list`
       A sequence of items, which can be any type.

Sequences of complex types can potentially have very long type descriptions.
If such a description must be split across multiple lines, you must end each line but the last with a ``\``:

.. code-block:: rst

    items : `lsst.afw.collections.FancyList` [`~collections.abc.Mapping` \
            [`str`, `~lsst.pex.config.Config`]]

.. _py-docstring-parameter-types-dict:

Dictionary types
""""""""""""""""

If the types of the keys and values are well-known, document the type of a `dict` parameter using a :pep:`484`-like syntax:

.. code-block:: rst

   measurements : `dict` [`str`, `astropy.quantity.Quantity`]
       The keys are names of metrics and values are measurements
       as `astropy.quantity.Quantity` instances, which combine
       both value and unit information.

Use the description to explain what the keys and values, since that information often isn't completely obvious from types alone.

.. warning::

   Ensure that you place a space between the container type and the bracket that wraps the key and value type.
   Don't do:

   .. code-block:: rst

      `dict`[`str`, `str`]

   Instead, do:

   .. code-block:: rst

      `dict` [`str`, `str`]

   Leaving out the space results in a parsing error.

If the types of keys and values are completely unknown, simply describe the type as ```dict``` and explain in the description.

If the keys are well-known, document the keys using a pattern similar to :ref:`py-docstring-parameter-types-struct`, by documenting each key-value pair using a :ref:`definition list <rst-dl>`:

.. code-block:: rst

   settings : `dict`
       Settings dictionary with keys:

       ``"color"``
           Hex colour code (`str`).
       ``"size"``
           Point area in pixels (`float`).
       ``"complicatedKey"``
           A key with a complicated description. Like any definition list item,
           the content can be wrapped. You can include lists inside the item as well:

           - The first item of the list. Lorem ipsum dolor sit amet, consectetur
             adipiscing elit.

             Proin nulla magna, egestas quis nisi id, dictum mollis diam. Duis lorem
             eros, tempor egestas ligula eget, dapibus posuere justo.

           - The second item of the list.

           You can also include multiple paragraphs in a key's description. Ensure that
           all content is aligned with the opening content line.

Notice how the keys are shown by enclosing the quoted strings in double backticks to clarify that the keys are `str` types.

Mappings of complex types can potentially have very long type descriptions.
If such a description must be split across multiple lines, you must end each line but the last with a ``\``:

.. code-block:: rst

    items : `lsst.afw.collections.FancyList` [`~collections.abc.Mapping` \
            [`str`, `~lsst.pex.config.Config`]]

.. _py-docstring-parameter-types-struct:

Struct types
""""""""""""

``lsst.pipe.base.Struct`` parameters are documented similarly to dictionaries with known keys.
Describe each attribute of a ``Struct`` parameter as a :ref:`definition list <rst-dl>` item:

.. code-block:: rst

   coord : `lsst.pipe.base.Struct`
      Coordinate as a struct with attributes:

      ``x``
          x-axis coordinate (`int`).
      ``y``
          y-axis coordinate (`int`).
      ``z``
          z-axis coordinate (`int`). Nam ut ligula tristique, consequat risus vel,
          sodales tellus. Sed sit amet vehicula felis, placerat pharetra nunc:

          - Morbi commodo euismod faucibus.
          - Fusce quis tortor et ex tincidunt dapibus quis ac lorem. Morbi quis
            tellus suscipit quam elementum euismod.

          Morbi vehicula facilisis diam ac volutpat. Proin suscipit mi ac ullamcorper
          vulputate. Nullam aliquet iaculis aliquam.

.. _py-docstring-parameter-types-array:

Array types
"""""""""""

For Numpy arrays, try to include the dimensionality:

.. code-block:: rst

   coords : `numpy.ndarray`, (N, 2)
       [...]
   flags : `numpy.ndarray`, (N,)
       Boolean array identifying sources that failed photometry.
   image : `numpy.ndarray`, (Ny, Nx)
       Processed image as a 2-dimensional array of float or double.

Choose conventional variables or labels to describe dimensions, like ``N`` for the number of sources or ``Nx, Ny`` for rectangular dimensions.
If the array should contain a specific type (e.g. `float` or `bool`), note that in the description.

.. _py-docstring-parameter-types-callable:

Callable types
""""""""""""""

For callback functions, describe the type as ``callable``:

.. code-block:: rst

   likelihood : callable
       Likelihood function that takes two positional arguments:

       - ``x``: current parameter (`float`).
       - ``extra_args``: additional arguments (`dict`).

.. _py-docstring-optional:

Optional parameters
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

.. _py-docstring-args-kwargs:

Additional positional and keyword arguments
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Functions and methods can take additional positional (``*args``) and keyword arguments (``*kwargs``):

.. code-block:: python

   def demoFunction(namedArg, *args, flag=False, **kwargs):
       """Demonstrate documentation for additional keyword and
       positional arguments.

       Parameters
       ----------
       namedArg : `str`
           A named argument that is documented like always.
       *args : `str`
           Additional names.

           Notice how the type is singular since the user is expected to pass individual
           `str` arguments, even though the function itself sees ``args`` as an iterable
           of `str` objects).
       flag : `bool`
           A regular keyword argument.
       **kwargs
           Additional keyword arguments passed to `otherApi`.

           Usually kwargs are used to pass parameters to other functions and
           methods. If that is the case, be sure to mention (and link) the
           API or APIs that receive the keyword arguments.

           If kwargs are being used to generate a `dict`, use the description to
           document the use of the keys and the types of the values.
       """

Order ``*args`` and ``**kwargs`` as they appear in the signature.

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
See the :ref:`Parameters secton <py-docstring-parameters>` and :ref:`py-docstring-parameter-types` for guidelines on how to describe specific types of yielded values.

Basic example
^^^^^^^^^^^^^

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

Naming return variables
^^^^^^^^^^^^^^^^^^^^^^^

Note that the names of the returned variables do not necessarily correspond to the names of variables.
Simply choose a variable-like name that is clear.

Rename attributes or private names:

.. code-block:: python
   :emphasize-lines: 6-7,9

   def getDistance(self):
       """Get the distance.

       Returns
       -------
       x : `float`
           Distance, in units of pixels.
       """
       return self._x

Name variables that don't have a name within the function scope:

.. code-block:: python
   :emphasize-lines: 8-9,10

   def getDistance(self, x, y):
       """Compute the distance of the point to an (x, y) coordinate.

       [...]

       Returns
       -------
       distance : `float`
           Distance, in units of pixels.
       """
       return np.hypot(self._x - x, self._y - y)

If the variable has a name in the scope that is useful, feel free to use that:

.. code-block:: python
   :emphasize-lines: 8-9,11

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

.. warning::

   The original `Numpydoc Style Guide`_ suggests a short-hand syntax that avoids naming a returned value:

   .. code-block:: python
      :emphasize-lines: 8-9,11

      def getDistance(self, x, y):
          """Compute the distance of the point to an (x, y) coordinate.

          [...]

          Returns
          -------
          `float`
              Distance, in units of pixels.
          """
          return np.hypot(self._x - x, self._y - y)

   **Don't use this syntax because it does not render properly.**

.. _py-docstring-yields:

Yields
------

*For generators.*

'Yields' is used identically to :ref:`'Returns' <py-docstring-yields>`, but for generators.
See the :ref:`Parameters secton <py-docstring-parameters>` and :ref:`py-docstring-parameter-types` for guidelines on how to describe specific types of yielded values.

Describe the yielded values as singular items yielded from each step, rather than as a sequence of items yielded from all iteration steps.

For example:

.. code-block:: python

   def items(self):
       """Iterate over items in the container.

       Yields
       ------
       key : `str`
           An item's key.
       value : obj
           An item's value.
       """
       for key, value in self._data.items():
           yield key, value

.. _py-docstring-other-parameters:

Other Parameters
----------------

*For classes, methods and functions.*

'Other Parameters' is an optional section used to describe infrequently used parameters.
It should only be used if a function has a large number of keyword parameters, to prevent cluttering the :ref:`Parameters <py-docstring-parameters>` section.
In practice, this section is seldom used.

.. _py-docstring-raises:

Raises
------

*For classes, methods and functions.*

'Raises' is an optional section for describing the exceptions that can be raised.
You usually cannot document all possible exceptions that might get raised by the entire call stack.
Instead, focus on:

- Exceptions that are commonly raised.
- Exceptions that are unique (custom exceptions, in particular).
- Exceptions that are important to using an API.

The 'Raises' section looks like this:

.. code-block:: rst

   Raises
   ------
   IOError
       Raised if the input file cannot be read.
   TypeError
       Raised if parameter ``example`` is an invalid type.

Don't wrap each exception's name with backticks, as we do when describing types in :ref:`Parameters <py-docstring-parameters>` and :ref:`Returns <py-docstring-returns>`).
No namespace prefix is needed when referring to exceptions in the same module as the API.
Providing the full namespace is often a good idea, though.

The description text is indented by four spaces from the docstring's left justification.
Like the description fields for :ref:`Parameters <py-docstring-parameters>` and :ref:`Returns <py-docstring-returns>`, the description can consist of multiple paragraphs and lists.

Stylistically, write the first sentence of each description in the form:

.. code-block:: text

   Raised if [insert circumstance].

.. _py-docstring-see-also:

See Also
--------

Use the 'See Also' section to link to related APIs that the user may not be aware of, or may not easily discover from other parts of the docstring.
Here are some good uses of the 'See Also' section:

- If a function wraps another function, you may want to reference the lower-level function.
- If a function is typically used with another API, you can reference that API.
- If there is a family of closely related APIs, you might link to others in the family so a user can compare and choose between them easily.

As an example, for a function such as ``numpy.cos``, we would have:

.. code-block:: rst

   See Also
   --------
   sin
   tan

Numpydoc assumes that the contents of the 'See Also' section are API names, so don't wrap each name with backticks, as we do when describing types in :ref:`Parameters <py-docstring-parameters>` and :ref:`Returns <py-docstring-returns>`).
No namespace prefix is needed when referring to functions in the same module.
Providing the full namespace is always safe, though, and provides clarity to fellow developers:

.. code-block:: rst

   See Also
   --------
   numpy.sin
   numpy.tan

.. _py-docstring-notes:

Notes
-----

*Notes* is an optional section that provides additional conceptual information about the API.
Some things to include in a *Notes* section:

- Discussions of features, going beyond the level of the :ref:`summary sentence <py-docstring-short-summary>` and :ref:`extended summary <py-docstring-extended-summary>`.
- Usage patterns, like how code is expected to use this API, or how this API is intended to be used in relation to other APIs.
- Background theory. For example, if the API implements an algorithm, you can fully document the algorithm here.
- Implementation details and limitations, if those details affect the user's experience.
  Purely internal details should be written as regular code comments.

Specific how-tos, tutorials, and examples go in the :ref:`Examples section <py-docstring-examples>` instead of *Notes*.
The *Notes* section is dedicated to conceptual documentation.

The :ref:`Parameters <py-docstring-parameters>`, :ref:`Returns <py-docstring-returns>` and :ref:`Yields <py-docstring-yields>` sections are the best places to describe specific input and output variables in detail.
The *Notes* section can still reference these variables by name (see :ref:`py-docstring-parameter-markup`), and discuss how they work at a big-picture level.

Most reStructuredText formatting is allowed in the *Notes* section, including:

- :ref:`Lists <rst-lists>`
- :ref:`Tables <rst-tables>`
- :ref:`Images <rst-figures>`
- :ref:`Inline and display math <rst-math>`
- :ref:`Links <rst-linking>`

When using images, remember that many developers and users will be reading the docstring in its raw source form.
Images should add information, but the docstring should still be useful and complete without them.

Subsections **are not** allowed in a Notes section (or any other section).
You can :ref:`simulate subsections with bold text <py-docstring-subsections>`.
See also :ref:`py-docstring-rst` for restrictions.

.. _py-docstring-references:

References
----------

References cited in the :ref:`'Notes' <py-docstring-notes>` section are listed here.
For example, if you cited an article using the syntax ``[1]_``, include its reference as follows:

.. code-block:: rst

   References
   ----------
   .. [1] O. McNoleg, "The integration of GIS, remote sensing,
      expert systems and adaptive co-kriging for environmental habitat
      modelling of the Highland Haggis using object-oriented, fuzzy-logic
      and neural-network techniques," Computers & Geosciences, vol. 22,
      pp. 585-588, 1996.

Web pages should be referenced with regular inline links.

References are meant to augment the docstring, but should not be required to understand it.
References are numbered, starting from one, in the order in which they are cited.

.. note::

   In the future we may support `bibtex-based references instead <https://github.com/mcmtroffaes/sphinxcontrib-bibtex>`__ instead of explicitly writing bibliographies in docstrings.

.. _py-docstring-examples:

Examples
--------

'Examples' is an optional section for usage examples written in the `doctest <http://docs.python.org/library/doctest.html>`_ format.
These examples do not replace unit tests, but *are* intended to be tested to ensure documentation and code are consistent.
While optional, this section is useful for users and developers alike.

When multiple examples are provided, they should be separated by blank lines.
Comments explaining the examples should have blank lines both above and below them:

.. code-block:: rst

   Examples
   --------
   A simple example:

   >>> np.add(1, 2)
   3

   Comment explaining the second example:

   >>> np.add([1, 2], [3, 4])
   array([4, 6])

For tests with a result that is random or platform-dependent, mark the output as such:

.. code-block:: rst

   Examples
   --------
   An example marked as creating a random result:

   >>> np.random.rand(2)
   array([ 0.35773152,  0.38568979])  #random

It is not necessary to use the doctest markup ``<BLANKLINE>`` to indicate empty lines in the output.

For more information on doctest, see:

- `The official doctest documentation <http://docs.python.org/library/doctest.html>`__.
- `doctest — Testing Through Documentation <https://pymotw.com/3/doctest/>`__ from Python Module of the Week.

Subsections **are not** allowed in an Examples section (or any other section).
You can :ref:`simulate subsections with bold text <py-docstring-subsections>`.
See also :ref:`py-docstring-rst` for restrictions.

.. _py-docstring-module-structure:

Documenting modules
===================

Sections in module docstrings
-----------------------------

Module docstrings contain the following sections:

1. :ref:`Short summary <py-docstring-short-summary>`
2. :ref:`Extended summary <py-docstring-extended-summary>` (optional)
3. :ref:`See Also <py-docstring-see-also>` (optional)

.. note::

   Module docstrings aren't featured heavily in the documentation we generate and publish with Sphinx.
   Avoid putting important end-user documentation in module docstrings.
   Instead, write introductory and overview documentation in the module's *user guide* (the :file:`doc/` directories of Stack packages).

   Module docstrings can still be useful for developer-oriented notes, though.

Placement of module docstrings
------------------------------

Module-level docstrings must be placed as close to the top of the Python file as possible: *below* any ``#!/usr/bin/env python`` and license statements, but *above* imports.
See also: :ref:`style-guide-py-file-order`.

Module docstrings should not be indented.
For example:

.. code-block:: python

   #
   # This file is part of dm_dev_guide.
   #
   # Developed for the LSST Data Management System.
   # This product includes software developed by the LSST Project
   # (http://www.lsst.org).
   # See the COPYRIGHT file at the top-level directory of this distribution
   # for details of code ownership.
   #
   # This program is free software: you can redistribute it and/or modify
   # it under the terms of the GNU General Public License as published by
   # the Free Software Foundation, either version 3 of the License, or
   # (at your option) any later version.
   #
   # This program is distributed in the hope that it will be useful,
   # but WITHOUT ANY WARRANTY; without even the implied warranty of
   # MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   # GNU General Public License for more details.
   #
   # You should have received a copy of the GNU General Public License
   # along with this program.  If not, see <http://www.gnu.org/licenses/>.
   #
   """Summary of MyModule.

   Extended discussion of my module.
   """

   import lsst.afw.table as afwTable
   # [...]

.. _py-docstring-class-structure:

Documenting classes
===================

Class docstrings are placed directly after the class definition, and serve to document both the class as a whole *and* the arguments passed to the ``__init__`` constructor.

Sections in class docstrings
----------------------------

Class docstrings contain the following sections:

1. :ref:`Short summary <py-docstring-short-summary>`
2. :ref:`Extended summary <py-docstring-extended-summary>` (optional)
3. :ref:`Parameters <py-docstring-parameters>` (if applicable)
4. :ref:`Other Parameters <py-docstring-other-parameters>` (if applicable)
5. :ref:`Raises <py-docstring-raises>` (if applicable)
6. :ref:`See Also <py-docstring-see-also>` (optional)
7. :ref:`Notes <py-docstring-notes>` (optional)
8. :ref:`References <py-docstring-references>` (optional)
9. :ref:`Examples <py-docstring-examples>` (optional)

Placement of class docstrings
-----------------------------

Class docstrings must be placed directly below the declaration, and indented according to the code scope:

.. code-block:: python

   class MyClass(object):
       """Summary of MyClass.

       Parameters
       ----------
       a : `str`
          Documentation for the ``a`` parameter.
       """

       def __init__(self, a):
           pass

The ``__init__`` method never has a docstring since the class docstring documents the constructor.

Examples of class docstrings
----------------------------

Here's an example of a more comprehensive class docstring with :ref:`Short Summary <py-docstring-short-summary>`, :ref:`Parameters <py-docstring-parameters>`, :ref:`Raises <py-docstring-raises>`, :ref:`See Also <py-docstring-see-also>`, and :ref:`Examples <py-docstring-examples>` sections:

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

       See Also
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

Documenting methods and functions
=================================

Sections in method and function docstring sections
--------------------------------------------------

Method and function docstrings contain the following sections:

1. :ref:`Short summary <py-docstring-short-summary>`
2. :ref:`Extended summary <py-docstring-extended-summary>` (optional)
3. :ref:`Parameters <py-docstring-parameters>` (if applicable)
4. :ref:`Returns <py-docstring-returns>` or :ref:`Yields <py-docstring-yields>` (if applicable)
5. :ref:`Other Parameters <py-docstring-other-parameters>` (if applicable)
6. :ref:`Raises <py-docstring-raises>` (if applicable)
7. :ref:`See Also <py-docstring-see-also>` (optional)
8. :ref:`Notes <py-docstring-notes>` (optional)
9. :ref:`References <py-docstring-references>` (optional)
10. :ref:`Examples <py-docstring-examples>` (optional)

Placement of module and function docstrings
-------------------------------------------

Class, method, and function docstrings must be placed directly below the declaration, and indented according to the code scope:

.. code-block:: python

   class MyClass(object):
       """Summary of MyClass.

       Extended discussion of MyClass.
       """

       def __init__(self):
           pass

       def myMethod(self):
           """Summary of method.

           Extended Discussion of myMethod.
           """
           pass


   def my_function():
       """Summary of my_function.

       Extended discussion of my_function.
       """
       pass

Again, the :ref:`class docstring <py-docstring-class-structure>` takes the place of a docstring for the ``__init__`` method.
``__init__`` methods don't have docstrings.

Dunder methods
--------------

Special "dunder" methods on classes only need to have docstrings if they are doing anything non-standard.
For example, if a ``__getslice__`` method cannot take negative indices, that should be noted.
But if ``__ge__`` returns true if ``self`` is greater than or equal to the argument, that need not be documented.

Examples of method and function docstrings
------------------------------------------

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

       See Also
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

Documenting constants and class attributes
==========================================

Sections in constant and class attribute docstrings
---------------------------------------------------

Constants in modules and attributes in classes are all documented similarly.
At a minimum, they should have a summary line that includes the type.
They can also have a more complete structure with these sections:

1. :ref:`Short Summary <py-docstring-short-summary>`
2. :ref:`Extended Summary <py-docstring-extended-summary>` (optional)
3. :ref:`Notes <py-docstring-notes>` (optional)
4. :ref:`References <py-docstring-references>` (optional)
5. :ref:`Examples <py-docstring-examples>` (optional)

Placement of constant and class attribute docstrings
----------------------------------------------------

Docstrings for module-level variables and class attributes appear directly below their first declaration.
For example:

.. code-block:: python
   :emphasize-lines: 1-3,10-12

   MAX_ITER = 10
   """Maximum number of iterations (`int`).
   """


   class MyClass(object):
       """Example class for documenting attributes.
       """

       x = None
       """Description of x attribute.
       """

Examples of constant and class attribute docstrings
---------------------------------------------------

Minimal constant or attribute example
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Include the attribute or constant's type in parentheses at the end of the summary line:

.. code-block:: py

   NAME = 'LSST'
   """Name of the project (`str`)."""

Multi-section docstrings
^^^^^^^^^^^^^^^^^^^^^^^^

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

Attributes set in \_\_init\_\_ methods
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In many classes, public attributes are set in the ``__init__`` method.
The best way to document these public attributes is by declaring the attribute at the class level and including a docstring with that declaration:

.. code-block:: python
   :emphasize-lines: 14-20

   class Metric(object):
       """Verification metric.

       Parameters
       ----------
       name : `str`
           Name of the metric.
       unit : `astropy.units.Unit`
           Units of the metric.
       package : `str`, optional
           Name of the package where this metric is defined.
       """

       name = None
       """Name of the metric (`str`).
       """

       unit = None
       """Units of the metric (`astropy.units.Unit`).
       """

       def __init__(self, name, unit, package=None):
           self.name = name
           self.unit = unit
           self._package = package

Notice that the :ref:`parameters <py-docstring-parameters>` to the ``__init__`` method are documented separately from the class attributes (highlighted).

.. _py-docstring-property-structure:

Documenting class properties
============================

Properties are documented like :ref:`class attributes <py-docstring-attribute-constants-structure>` rather than methods.
After all, properties are designed to appear to the user like simple attributes.

For example:

.. code-block:: python

   class Measurement(object):

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

.. _py-docstring-example-module:

Complete example module
=======================

.. literalinclude:: examples/numpydocExample.py
   :language: python

Acknowledgements
================

These docstring guidelines are derived/adapted from the `Numpydoc`_ and `Astropy <http://docs.astropy.org/en/stable/_sources/development/docrules.txt>`_ documentation.
The example module is adapted from the `Napoleon documentation <http://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_numpy.html#example-numpy>`_.

Numpy is Copyright © 2005-2013, Numpy Developers.

Astropy is Copyright © 2011-2015, Astropy Developers.

.. _Numpydoc: https://numpydoc.readthedocs.io/en/latest/
.. _Numpydoc Style Guide: https://numpydoc.readthedocs.io/en/latest/format.html
