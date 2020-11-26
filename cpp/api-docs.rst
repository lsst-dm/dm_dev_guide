####################
Documenting C++ Code
####################

We document C++ code in two ways:

1. By writing *documentation blocks* for all public or protected C++ components (namespaces, types, methods, functions, and constants).

   The LSST Stack uses `Doxygen <http://www.doxygen.org/>`_ to build C++ API reference documentation from comment blocks. This documentation is exposed to users in a variety of contexts, from developers reading the code to readers of the `Stack Doxygen Documentation <http://doxygen.lsst.codes/stack/doxygen/x_masterDoxyDoc/>`_.

   Doxygen comment blocks are the public specification of our C++ API.

   Our Doxygen configuration file is located in the `base package <https://github.com/lsst/base/blob/master/doc/base.inc>`_.
   For Science Pipelines packages, it is automatically included in all documentation builds.

2. By commenting our code internally with C++ comments (``//`` or ``/* .. */``).

   These comments are meant to be read only by developers reading and editing the source code.

This page focuses on public code documentation using Doxygen, while internal comments are discussed in our :doc:`style`.

Treat the guidelines on this page as an extension of the :doc:`style`.

.. note::

   Changes to this document must be approved by the System Architect (`RFC-24 <https://jira.lsstcorp.org/browse/RFC-24>`_).
   To request changes to these standards, please file an :doc:`RFC </communications/rfc>`.

**This guide will evolve as a mechanism to document C++ APIs wrapped in Python is developed.**

.. _cpp-file-boilerplate:

Boilerplate for Header (.h) and Source (.cc) Files
==================================================

The beginning of both header and source code files should include

1. A formatting hint for Emacs

   .. code-block:: cpp

      // -*- lsst-c++ -*-

2. A copyright and license block (note: **NOT** a Doxygen comment block) using `the standard text <https://github.com/lsst/templates/tree/master/file_templates/stack_license_preamble_cpp>`_.

   .. remote-code-block:: https://raw.githubusercontent.com/lsst/templates/master/file_templates/stack_license_preamble_cpp/template.cc.jinja
      :language: jinja

   Replace ``{{ cookiecutter.package_name }}`` with the package's name.

Some older code contains file-level Doxygen blocks (i.e., comments with a ``@file`` command).
Such blocks should not be used in new code, as they rarely provide useful information about API elements defined by the file, and do not integrate well with `pipelines.lsst.io`_.
Ordinary C++ comments may still be used to document files for developers reading the source code.

.. _`pipelines.lsst.io`: https://pipelines.lsst.io

.. _cpp-doxygen-basics:

Basic Format of Documentation Blocks
====================================

This page covers the most important concepts in writing Doxygen-friendly C++ comments for the LSST Stack, though `Doxygen's manual <http://www.doxygen.org/manual/>`_ is the most comprehensive reference.

.. _cpp-doxygen-javadoc:

Documentation MUST be delimited in Javadoc style
------------------------------------------------

Multi-line documentation blocks must begin with ``/**`` and end in ``*/``. Single-line documentation blocks must begin with ``///``. For consistency, do not begin documentation blocks with ``/*!`` or ``//!``.

(*Note:* one-line documentation blocks are rarely used for public APIs, see :ref:`cpp-doxygen-sections`.)

Under certain circumstances, single-line documentation blocks may begin with ``///<`` instead of ``///``. These cases are indicated below.

.. _cpp-doxygen-form:

Multi-line documentation delimiters SHOULD be on their own lines
----------------------------------------------------------------

A multi-line documentation block's summary sentence should occur on the line after the opening ``/**``, and the terminating ``*/`` should be on its own line. An example:

.. code-block:: cpp

   /**
    * Sum numbers in a vector.
    *
    * This sum is the arithmetic sum, not some other kind of sum that only
    * mathematicians have heard of.
    *
    * @param values Container whose values are summed.
    * @return sum of `values`, or 0.0 if `values` is empty.
    */

.. _cpp-doxygen-tag:

Documentation MUST use Javadoc-style tags
-----------------------------------------

Documentation blocks must use tags such as ``@see`` or ``@param`` in place of ``\see`` or ``\param``.
This is both for internal consistency and to avoid conflicts with other tools that give special treatment to ``\word``.

.. _cpp-doxygen-styling:

Documentation SHOULD use Markdown for formatting
------------------------------------------------

LSST uses `Markdown-formatted Doxygen comment blocks <http://www.doxygen.org/manual/markdown.html>`_. If a particular format cannot be expressed using Markdown, you MAY use `Doxygen's built-in formatting <http://www.doxygen.org/manual/commands.html>`_ or, if necessary, `HTML markup <http://www.doxygen.org/manual/htmlcmds.html>`_.

.. _cpp-doxygen-headeronly:

Documentation MUST appear where a component is first declared
-------------------------------------------------------------

In general, this means documentation blocks will appear in header (``.h``) files rather than source (``.cc``) files. This keeps all the documentation with the API and avoids certain false alarms when Doxygen parses C++11 code.

.. _cpp-doxygen-indentation:

Documentation MUST appear before the declaration it describes, and with the same indentation
--------------------------------------------------------------------------------------------

For example:

.. code-block:: cpp

   /**
    * Sum numbers in a vector.
    *
    * @param values Container whose values are summed.
    * @return sum of `values`, or 0.0 if `values` is empty.
    */
   double sum(std::vector<double> & const values) {
       ...
   }

Not:

.. code-block:: cpp

   double sum(std::vector<double> & const values) {
       /**
        * Sum numbers in a vector.
        *
        * @param values Container whose values are summed.
        * @return sum of `values`, or 0.0 if `values` is empty.
        */
       ...
   }

.. _cpp-doxygen-sections:

Common Structure of Documentation Blocks
========================================

We organize Doxygen comment blocks into sections that appear in a common order. This format is analogous to the one adopted for the :ref:`Python documentation <py-docstring-sections>`.
The sections and their relative order are:

1. :ref:`cpp-doxygen-short-summary`
2. :ref:`cpp-doxygen-extended-summary` (recommended)
3. :ref:`cpp-doxygen-tparameters` (if applicable; for classes, methods, and functions)
4. :ref:`cpp-doxygen-parameters` (if applicable; for methods and functions)
5. :ref:`cpp-doxygen-returns` (if applicable; for methods and functions)
6. :ref:`cpp-doxygen-throws` (if applicable; for methods and functions)
7. :ref:`cpp-doxygen-exceptsafe` (optional; for methods and functions)
8. :ref:`cpp-doxygen-related` (if applicable; for functions)
9. :ref:`cpp-doxygen-initializer` (optional; for constants)
10. :ref:`cpp-doxygen-see-also` (optional)
11. :ref:`cpp-doxygen-notes` (optional)
12. :ref:`cpp-doxygen-references` (optional)
13. :ref:`cpp-doxygen-examples` (optional)

For summaries of how these sections are composed in specific contexts, see:

- :ref:`cpp-doxygen-class-structure`
- :ref:`cpp-doxygen-enum-structure`
- :ref:`cpp-doxygen-method-function-structure`
- :ref:`cpp-doxygen-attribute-constants-structure`

.. _cpp-doxygen-short-summary:

Short Summary
-------------

A one-line summary that does not use variable names or the function's name. This summary will appear in lists of class/namespace members.

.. code-block:: cpp

   /// Sum two numbers.
   double add(double a, double b);

By default, brief summaries will end at a period followed by whitespace, or at a new line, whichever comes first. You can ignore periods that shouldn't end the description by following them with a backslash and a space (as in ``"e.g.\ "``).

Brief summaries should be short enough to fit on one line. If you must have a summary that extends over multiple lines, you must prefix the summary by ``@brief``, which will cause the summary to end at the next blank line rather than the next line break.

For functions and methods, the summary should be written in the imperative voice (i.e., as a command that the API consumer is giving). Getters and other methods that are more naturally described as values rather than actions may ignore this rule.

.. _cpp-doxygen-extended-summary:

Extended Summary
----------------

The extended summary is an optional sentence or short paragraph that clarifies and supports the :ref:`summary sentence <cpp-doxygen-short-summary>`.
Taken together with the summary sentence, the summary content in general exists to help users quickly understand the role and scope of the API.

Leave detailed discussions of the API's features, usage patterns, background theory, and implementation details to the :ref:`Notes <cpp-doxygen-notes>` and :ref:`Examples <cpp-doxygen-examples>` sections.
The :ref:`Parameters <cpp-doxygen-parameters>` and :ref:`Returns <cpp-doxygen-returns>` sections are ideal places to discuss in detail individual parameters and returned values, respectively.

This section's brevity is critical.
The extended summary is proximate to the summary sentence so that the two pieces of content support each other.
However, the extended summary also separates the API signature from the :ref:`Parameters <cpp-doxygen-parameters>` section, which users expect to see close together.
As a general guideline, the extended summary should be three sentences or fewer.

.. _cpp-doxygen-tparameters:

Template Parameters
-------------------

A series of ``@tparam`` tags, usually one for each template parameter. Each tag should have a description following the parameter name. You do *not* usually need to document default values; Doxygen will provide the default automatically. If the description extends over multiple lines, each line after the first must be indented.

Parameters should be listed in the same order as they appear in the class, function, or method signature.

.. code-block:: cpp

   /**
    * Storage for arbitrary data with log(N) lookup.
    *
    * ...
    *
    * @tparam T the type of data stored in the table
    * @tparam ComparatorT callable defining a strict weak ordering for objects
    *     of type `T`. Its `operator()` must accept two `T` and return `true`
    *     if and only if the first argument comes before the second. It must
    *     not throw exceptions.
    */
   template <typename T, typename ComparatorT = std::less<T>>
   class LookupTable
   {
       ...
   }

When two or more consecutive template parameters have *exactly* the same description, they can be combined:

.. code-block:: cpp

   /**
    * @tparam T, U the types of the pair components
    */

.. _cpp-doxygen-tparameters-specializations:

.. note::

   Doxygen will not properly parse parameter descriptions that have multiple paragraphs. If your template parameters require a lengthy explanation, put the explanation in the :ref:`cpp-doxygen-extended-summary` and refer to it from the parameter descriptions.

Template Specializations
^^^^^^^^^^^^^^^^^^^^^^^^

When a partial template specialization reuses parameters from the full template, there is no need to redocument each parameter. If you are omitting the parameters, the documentation must include a cross-reference to the full template, possibly as part of the :ref:`cpp-doxygen-see-also` section.

You must redocument the parameters if the template specialization redefines any parameters (e.g., if the generic parameter ``T`` becomes ``T*`` in the specialization) or if it places additional restrictions on their values.

.. _cpp-doxygen-parameters:

Function/Method Parameters
--------------------------

A series of ``@param`` tags, usually one for each parameter. Each tag should have a description following the parameter name. You do *not* usually need to document default arguments; Doxygen will provide the default automatically. If the description extends over multiple lines, each line after the first must be indented.

Parameters should be listed in the same order as they appear in the function or method signature.
Make sure to keep the parameter list in sync with the actual parameters; Doxygen will issue a warning if they don't match.

``@param`` should be given with the ``[in]``, ``[out]``, or ``[in, out]`` tag if the function method contains any output parameters. The ``[in]`` tag is optional if all parameters are input, even if other functions or methods in the same class or package use output parameters.

.. code-block:: cpp

   /**
    * Compute mean and standard deviation for a collection of data.
    *
    * @param[out] mean the mean of `data`, or `NaN` if `data` is empty
    * @param[out] stdDev the unbiased (sample) standard deviation, or `NaN`
    *     if `data` contains fewer than 2 elements
    * @param[in] data the data to analyze
    */
   void computeStatistics(double & mean, double & stdDev, std::vector<double> const & data);

When two or more consecutive parameters have *exactly* the same description, they can be combined:

.. code-block:: cpp

   /**
    * @param x, y the coordinates where the function is evaluated
    */

.. note::

   Doxygen will not properly parse parameter descriptions that have multiple paragraphs. If your function's input requires a lengthy explanation, put the explanation in the :ref:`cpp-doxygen-notes` and refer to it from the parameter descriptions.

.. _cpp-doxygen-parameters-inline:

Annotating Parameters with Inline Comments (historical)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

An alternative to the ``@param`` tag is to use an inline comment after each parameter, one per line.
These comments are prefixed with ``///<``.

This style is permitted for historical reasons, but should not be used in new code.
If the parameter descriptions are too long to fit in a single line of source, the ``@param`` documentation method *must* be used.

.. _cpp-doxygen-returns:

Returns
-------

A ``@returns`` tag, followed by a description similar to the one for :ref:`cpp-doxygen-parameters`. If the returned value is a map, ensure that the key-value pairs are documented in the description.

For consistency with Python documentation, always use ``@returns`` and not the synonymous ``@return``.

.. _cpp-doxygen-throws:

Throws
------

A series of ``@throws`` tags, one for each type of exception (see :ref:`the style guide <style-guide-cpp-5-36>`). Each tag should have a description following the exception type. If the description extends over multiple lines, each line after the first must be indented.

.. code-block:: cpp

   /**
    * Write an image to disk.
    *
    * @throws lsst::pex::exceptions::IoError Thrown if `fileName` could not be
    *     written to.
    */
   void writeImage(std::string const & fileName);

Exception classes must be namespace-qualified using the same rules as :ref:`@see <cpp-doxygen-see-also>`.
Doxygen will render one or more ``@throws`` tags as a table of exceptions and descriptions, so do not treat ``@throws`` as the first word of the description.

For consistency with Python documentation, always use ``@throws`` and not the synonymous ``@throw`` or ``@exception``.

.. _cpp-doxygen-exceptsafe:

Exception Safety
----------------

Whether or not there are any ``@throws`` tags for specific exceptions, a function or method should have an ``@exceptsafe`` tag.
The description following the tag should describe the level of exception safety provided by the function or method.

The following terms may be used for brevity:

no-throw
    The function is guaranteed to always return without throwing an exception.
strong
    If the function throws an exception, the program will be in the same state as before the call; i.e., failed calls have no side effects.
basic
    If the function throws an exception, the program will be in a valid state, but not necessarily a predictable one. No memory, file descriptors, locks, or other resources will be leaked.
none
    If the function throws an exception, objects may be corrupted and unsafe to use, or resources may be leaked.

Examples:

.. code-block:: cpp

   /**
    * Image associated with this map.
    *
    * @exceptsafe Shall not throw exceptions.
    */
   ImageF getImage() const noexcept;

.. code-block:: cpp

   /**
    * Apply a user-specified transformation to an image.
    *
    * @exceptsafe If `transform` provides basic exception safety, then this
    *     method shall provide strong exception safety. Otherwise, it provides
    *     no exception safety guarantee.
    */
   template <class Func>
   ImageF transformImage(Func const & transform) const;

.. _cpp-doxygen-related:

Helper Functions
----------------

Some operations on a class, particularly arithmetic operators, must be implemented as standalone functions even though they are *conceptually* part of the class. These functions should have the ``@relatesalso`` tag, followed by the name of the appropriate class. They will appear on the class's documentation page under the heading "Related Functions". Use this tag sparingly.

For internal consistency, always use ``@relatesalso`` and not the synonymous ``@relatedalso``.

Examples:

.. code-block:: cpp

   /**
    * Add two images pixel-by-pixel.
    *
    * @relatesalso ImageF
    */
   ImageF operator+(ImageF const & lhs, ImageF const & rhs);

.. _cpp-doxygen-initializer:

Initializer Declaration
-----------------------

By default, Doxygen shows the values of constants unless they are very long. The ``@showinitializer`` and ``@hideinitializer`` tags override this behavior.

.. code-block:: cpp

   /**
    * Maximum number of simultaneous readers supported.
    *
    * @hideinitializer
    */
   int const MAX_READERS = 16;    // Value is implementation detail and subject to change

.. _cpp-doxygen-see-also:

See Also
--------

'See Also' is an optional section used to refer to related code.
This section can be very useful, but should be used judiciously.
The goal is to direct users to other functions they may not be aware of, or have easy means of discovering (by looking at the class or package documentation, for example).
Functions whose documentation further explains parameters used by this function are good candidates.

This section can also refer to arbitrary pages using a URL or a Markdown-style link.

List each class, function, method, or link using a ``@see`` tag:

.. code-block:: cpp

   /**
    * Compute an element-wise cosine.
    *
    * @see sin
    * @see tan
    * @see [numpy.vectorize](https://docs.scipy.org/doc/numpy/reference/generated/numpy.vectorize.html)
    */
   vector<double> cos(vector<double> const & angles);

Prefix objects from other namespaces appropriately by their greatest common namespace. For example, while documenting an ``lsst::afw::tables`` module, refer to a class in ``lsst::afw::detection`` by ``afw::detection::Footprint``. When referring to an entirely different module or package, use the full namespace.
Do not use namespace abbreviations, as Doxygen has trouble resolving them.

For internal consistency, always use ``@see`` and not the synonymous ``@sa``.

.. _cpp-doxygen-notes:

Notes
-----

*Notes* is an optional section that provides additional conceptual information about the API.

The notes must be prefixed by a ``@note`` or ``@warning`` command.
For internal consistency, always use ``@note`` and not the synonymous ``@remark`` or ``@remarks``.

Some things to include in a *Notes* section:

- Discussions of features, going beyond the level of the :ref:`summary sentence <py-docstring-short-summary>` and :ref:`extended summary <py-docstring-extended-summary>`.
- Usage patterns, like how code is expected to use this API, or how this API is intended to be used in relation to other APIs.
- Background theory. For example, if the API implements an algorithm, you can fully document the algorithm here.
- Implementation details and limitations, if those details affect the user's experience.
  Purely internal details should be written as regular code comments.

Specific how-tos, tutorials, and examples go in the :ref:`Examples section <py-docstring-examples>` instead of *Notes*.
The *Notes* section is dedicated to conceptual documentation.

The :ref:`cpp-doxygen-parameters` and :ref:`cpp-doxygen-returns` sections are the best places to describe specific input and output variables.
The *Notes* section can still reference these variables by name (see :ref:`py-docstring-parameter-markup`), and discuss how they work at a big-picture level.
Since the content in the :ref:`cpp-doxygen-parameters` needs to be brief, you can write additional content as part of the *Notes* section.

This section may include mathematical equations to document the algorithm implemented by the function or class.
Equations may be written in `LaTeX <http://www.latex-project.org/>`_ format:

.. code-block:: cpp

   /**
    * The FFT is a fast implementation of the discrete Fourier transform:
    * @f[ X(e^{j\omega } ) = x(n)e^{ - j\omega n} @f]
    */

LaTeX environments can also be used:

.. code-block:: cpp

   /**
    * The discrete-time Fourier time-convolution property states that
    * @f{eqnarray*}
    * x(n) * y(n) \Leftrightarrow X(e^{j\omega } )Y(e^{j\omega } )\\
    * another equation here
    * @f}
    */

Math can also be used inline:

.. code-block:: cpp

   /**
    * Fit a model of the form @f$y = a x + b@f$ to the data.
    */

Note that LaTeX is not particularly easy to read, so use equations judiciously. In particular, do not use inline LaTeX just to add Greek or other special symbols; prefer `HTML character entities <http://www.doxygen.org/manual/htmlcmds.html>`_ or Unicode instead.

Doxygen recovers poorly from typos in formulas; you may need to manually delete ``docs/html/formula.repository`` if it contains a bad formula.

Images are allowed, but should not be central to the explanation; users viewing the documentation as text must be able to comprehend its meaning without resorting to an image viewer.
These additional illustrations are included using the ``@image`` command:

.. code-block:: cpp

   /**
    * @image html filename ["caption"]
    */

``filename`` is a path relative to the project root directory.

Equations or images may be used as described in :ref:`cpp-doxygen-extended-summary`.

.. _cpp-doxygen-references:

References
----------

References can be included either in the :ref:`'Notes' <cpp-doxygen-notes>` section or in a separate list below them. A reference consists of the ``@cite`` tag, followed by a BibTeX label. Bibfiles must be listed in the ``CITE_BIB_FILES`` configuration tag in ``doc/doxygen.conf.in``.

Note that Web pages should be referenced with regular inline links.

References are meant to augment the documentation, but should not be required to understand it.

.. _cpp-doxygen-examples:

Examples
--------

'Examples' is an optional section for examples. This section is very strongly encouraged.

Examples should use Markdown formatting for code blocks (i.e., indented by four extra spaces):

.. code-block:: cpp

   /**
    * This is an amazing function! For example:
    *
    *     auto cosines = cos(angles);
    *
    * Comment explaining the second example.
    *
    *     auto cosines = cos(radians(angles));
    */

.. _cpp-doxygen-package-definition:

Documenting/Defining Packages
=============================

LSST packages are no longer documented using Doxygen.
Instead, they should be documented using the Sphinx :ref:`module-homepage`.

.. _cpp-doxygen-class-structure:

Documenting Classes and Type Aliases
====================================

Class documentation blocks are placed immediately before the class declaration, and serve to document the class as a whole rather than individual methods.

1. :ref:`cpp-doxygen-short-summary`
2. :ref:`cpp-doxygen-extended-summary` (recommended)
3. :ref:`cpp-doxygen-tparameters` (if applicable)
4. :ref:`cpp-doxygen-see-also` (optional)
5. :ref:`cpp-doxygen-notes` (optional)
6. :ref:`cpp-doxygen-references` (optional)
7. :ref:`cpp-doxygen-examples` (optional)

For example:

.. code-block:: cpp

   /**
    * Implementation of a trace facility for LSST
    *
    * Tracing is controlled on a per "component" basis, where a "component" is a
    * name of the form aaa.bbb.ccc where aaa is the Most significant part; for
    * example, the utilities library might be called "utils", the doubly-linked
    * list "utils.dlist", and the code to destroy a list "utils.dlist.del"
    *
    */
   class TraceImpl
   {
       public:
           ...
   }

Type alias declarations and typedefs should also be documented, although just a short summary is usually sufficient.
Doxygen will automatically provide links to the types being renamed, if their documentation is available.

.. _cpp-doxygen-enum-structure:

Documenting Enumerated Types
============================

An enumerated type is a type, and should be documented similarly to a class:

1. :ref:`cpp-doxygen-short-summary`
2. :ref:`cpp-doxygen-extended-summary` (recommended)
3. :ref:`cpp-doxygen-see-also` (optional)
4. :ref:`cpp-doxygen-notes` (optional)
5. :ref:`cpp-doxygen-references` (optional)

In addition, each value of the type should be documented. A short description is almost always sufficient.

For example:

.. code-block:: cpp

   /**
    * Supported coordinate systems for flux-conserving transformations.
    *
    * These values are used in arguments to various functions in this package.
    * Unless otherwise stated, these functions do not validate whether the data
    * set makes sense in the "from" coordinates.
    */
   enum class CoordType
   {
       /// Untransformed detector coordinates.
       PIXEL,
       /// Idealized detector coordinates after applying a distortion correction.
       WARP_PIXEL,
       /// Equatorial J2000.0 coordinates.
       SKY_WCS
   };

.. _cpp-doxygen-enum-inline:

Annotating Enum Values with Inline Comments (optional)
------------------------------------------------------

If the value descriptions are very short, you may choose to annotate values with inline comments after each constant, one per line.
These comments are prefixed with ``///<``.

For example:

.. code-block:: cpp

   enum class CoordType
   {
       PIXEL,    ///< Untransformed detector coordinates
       WARP_PIXEL,    ///< Distortion-corrected detector coordinates
       SKY_WCS    ///< Equatorial J2000.0 coordinates
   };

If the constant descriptions are too long to fit in a single line of source, ordinary documentation blocks before each constant must be used.

.. _cpp-doxygen-method-function-structure:

Documenting Methods and Functions
=================================

All public or protected methods and all functions must be preceded by a documentation block.
Method or function documentation blocks contain the following sections:

1. :ref:`cpp-doxygen-short-summary`
2. :ref:`cpp-doxygen-extended-summary` (recommended)
3. :ref:`cpp-doxygen-tparameters` (if applicable)
4. :ref:`cpp-doxygen-parameters` (if applicable)
5. :ref:`cpp-doxygen-returns` (if applicable)
6. :ref:`cpp-doxygen-throws` (if applicable)
7. :ref:`cpp-doxygen-exceptsafe` (optional)
8. :ref:`cpp-doxygen-related` (if applicable; for functions only)
9. :ref:`cpp-doxygen-see-also` (optional)
10. :ref:`cpp-doxygen-notes` (optional)
11. :ref:`cpp-doxygen-references` (optional)
12. :ref:`cpp-doxygen-examples` (optional)

An example:

.. code-block:: cpp

   /**
    * Read an image from disk.
    *
    * @param fileName the file to read. Must be either absolute or relative to
    *     the program working directory.
    *
    * @return the image stored in `fileName`. If the image on disk does not
    *     have `double` pixels, they will be cast to `double`.
    *
    * @throws IoError Thrown if `fileName` does not exist or is not readable.
    *
    * @exceptsafe Strong exception guarantee.
    */
   lsst::afw::image::Image<double> loadImage(std::string const & fileName);

.. _cpp-doxygen-method-function-overloads:

Overloaded Function/Method Definitions
--------------------------------------

``@overload`` may be used when two methods/functions are effectively the same but have different parameter lists for reasons of convenience.
Use this tag **only** when the specification of the abbreviated overload can be easily inferred from the fully documented one.

The text generated by the ``@overload`` tag tells readers to see the method "above".
Because Doxygen sorts the detailed documentation of namespace and class members, you should check the generated documentation to make sure the fully documented overload appears before any that use the ``@overload`` tag.

For example:

.. code-block:: cpp

   /**
    * Sum numbers in a vector.
    *
    * @param values Container whose values are summed.
    * @return sum of `values`, or 0.0 if `values` is empty.
    *
    * @exceptsafe This function does not throw exceptions.
    */
   double add(std::vector<double> const & values);

   /**
    * Sum numbers in an array.
    *
    * @overload
    */
   double add(double[] const values, size_t nValues);

.. _cpp-doxygen-attribute-constants-structure:

Documenting Constants, Variables, and Data Members
==================================================

All non-private constants, variables, or data members must be preceded by a documentation block.
At minimum, constants/variables/data members should have a summary line, but can also have a more complete structure:

1. :ref:`cpp-doxygen-short-summary`
2. :ref:`cpp-doxygen-extended-summary` (optional)
3. :ref:`cpp-doxygen-initializer` (optional; for constants only)
4. :ref:`cpp-doxygen-notes` (optional)
5. :ref:`cpp-doxygen-references` (optional)
6. :ref:`cpp-doxygen-examples` (optional)

For example:

.. code-block:: cpp

   /// Flag set if background subtraction should not be done.
   const int NO_BACKGROUND = 1 << 3;

.. _cpp-doxygen-attribute-constants-inline:

Annotating Constants and Variables with Inline Comments (optional)
------------------------------------------------------------------

If the constant, variable, or data member descriptions are very short, you may choose to annotate them with inline comments after each value, one per line.
These comments are prefixed with ``///<``.

For example:

.. code-block:: cpp

   const int NO_BACKGROUND = 1 << 3;        ///< Skip background subtraction

If the descriptions are too long to fit in a single line of source, ordinary documentation blocks before each value must be used.
