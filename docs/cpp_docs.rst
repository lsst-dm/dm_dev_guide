####################
Documenting C++ Code
####################

.. note::

   This is a preview documentation format specification.
   Software documentation should currently be written in the format described at https://confluence.lsstcorp.org/display/LDMDG/Documentation+Standards


We document C++ code in two ways:

1. By writing *documentation blocks* for all public or protected C++ components (namespaces, types, methods, functions, and constants).

   The LSST Stack uses `Doxygen <http://www.doxygen.org/>`_ to build C++ API reference documentation from comment blocks. This documentation is exposed to users in a variety of contexts, from developers reading the code to readers of the `Stack Documentation <https://lsst-web.ncsa.illinois.edu/doxygen/x_masterDoxyDoc/>`_.

   Doxygen comment blocks are the public specification of our C++ API.

2. By commenting our code internally with C++ comments (``//`` or ``/* .. */``).

   These comments are meant to be read only by developers reading and editing the source code.

This page focuses on public code documentation using Doxygen, while internal comments are discussed in our :doc:`../coding/cpp_style_guide`.

Treat the guidelines on this page as an extension of the :doc:`../coding/cpp_style_guide`.

.. note::

   Changes to this document must be approved by the System Architect (`RFC-24 <https://jira.lsstcorp.org/browse/RFC-24>`_).
   To request changes to these standards, please file an :ref:`RFC <decision-making-rfc>`.

This document is ported from original documentation in Confluence; https://confluence.lsstcorp.org/display/LDMDG/Documentation+Standards.
**This guide will evolve as a mechanism to document C++ APIs wrapped in Python is developed.**

.. _cpp-file-boilerplate:

Boilerplate for Header (.h) and Source (.cc) Files
==================================================

The beginning of both header and source code files should include

1. A formating hint for Emacs

   .. code-block:: cpp

      // -*- lsst-c++ -*-

2. A copyright and license block (note: **NOT** a Doxygen comment block)

   .. code-block:: cpp

      /*
       * LSST Data Management System
       * Copyright 2008-2017 AURA/LSST.
       *
       * This product includes software developed by the
       * LSST Project (http://www.lsst.org/).
       *
       * This program is free software: you can redistribute it and/or modify
       * it under the terms of the GNU General Public License as published by
       * the Free Software Foundation, either version 3 of the License, or
       * (at your option) any later version.
       *
       * This program is distributed in the hope that it will be useful,
       * but WITHOUT ANY WARRANTY; without even the implied warranty of
       * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
       * GNU General Public License for more details.
       *
       * You should have received a copy of the LSST License Statement and
       * the GNU General Public License along with this program. If not,
       * see <http://www.lsstcorp.org/LegalNotices/>.
       */

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

.. _doc-cpp-package-definition:

Package Documentation / Definition
==================================

Each LSST package corresponds to a group in Doxygen.
We declare this package in the root header file for a package, usually named ``package.h``.

In this header file, below the preamble, provide a Doxygen comment block that declares the package with the fields:

1. ``@defgroup`` followed by the ``PackageName`` and  ``PackageTitle``

2. ``@brief`` to provide a one-line description of the package.

For example:

.. code-block:: cpp

   /**
    * @defgroup PackageName PackageTitle
    *
    * @brief Provide some stuff to do stuff
    */

Class Definitions
=================

Where a class is *defined* (usually in a header file), provide a Doxygen block preceeding the class that includes

1. A one-line description of the class.

2. A paragraph (or more) describing the class. Markdown can be used to provide nuanced typography.

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
   class TraceImpl {
       public:
   }

Function/Method Definitions
===========================

Where a function or class method is *defined*, provide a Doxygen block preceeding that class that includes

1. A one-line description of the function/method

2. Optionally, a paragraph or more with detailed descriptions of the function/method. Markdown can be used here.

3. ``@param`` statements describing each function/method argument. Optionally, inline comments can be used (see below).

An example of a Doxygen comment for a function:

.. code-block:: cpp

   /** Set a component's verbosity.
   *
   * If no verbosity is specified, inherit from parent
   *
   * @param name component of interest
   * @param verbosity desired trace verbosity
   */
   void TraceImpl::setVerbosity(const std::string &name, const int verbosity) {
   }

Annotating Arguments with Inline Comments (optional)
----------------------------------------------------

If the argument descriptions are very short, you may choose to annotate arguments with inline comments after each argument, one per line.
These comments are prefixed with ``///< set:``.

For example:

.. code-block:: cpp

   /** Set a component's verbosity.
   *
   * If no verbosity is specified, inherit from parent
   */
   void TraceImpl::setVerbosity(const std::string &name, ///< component of interest
                                const int verbosity) { ///< desired trace verbosity
   }

If the argument descriptions are too long to fit in a single line of source, the ``@param`` documenation method should be used.

Overloaded Function/Methods Definitions
=======================================

'`@overload`` may be used when two methods/functions are effectively the same but have different parameters list for reasons of convenience.

For example:

.. code-block:: cpp

   /**
    * seconds from midnight
    */
   long GetTime(void){
       return secondFromMidnight(CURRENT);
   }
   /**
    # @overload void GetTime(int &hours, int &minutes, int &seconds)
    */
   void GetTime(int &hours, ///< set: current hour
                int &minutes, ///< set: current minutes
                int &seconds) { ///< set: current seconds
    hours = _hours;
    minutes = _minutes;
    seconds = _seconds;
   }
