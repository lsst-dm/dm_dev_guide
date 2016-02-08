####################
Documenting C++ Code
####################

.. note::

   This is a preview documentation format specification.
   Software documentation should currently be written in the format described at https://confluence.lsstcorp.org/display/LDMDG/Documentation+Standards

The LSST Stack uses `Doxygen <http://www.stack.nl/~dimitri/doxygen/>`_ to build C++ API reference documentation by extracting source code comments.
This page covers the most important concepts in writing Doxygen-friendly C++ comments for the LSST Stack, though `Doxygen's manual <http://www.stack.nl/~dimitri/doxygen/manual.html>`_ is the most comprehensive reference.

Note that LSST uses `Markdown-formatted Doxygen comment blocks <http://www.doxygen.nl/manual/markdown.html>`_.

This document is ported from original documentation in Confluence; https://confluence.lsstcorp.org/display/LDMDG/Documentation+Standards.
**This guide will evolve as a mechanism to document C++ APIs wrapped in Python in developed.**

Boilerplate for Header (.h) and Source (.cpp) Files
===================================================

The beginning of both header and source code files should include

1. A formating hint for Emacs

   .. code-block:: cpp

      // -*- lsst-c++ -*-

2. A copyright and license block

   .. code-block:: cpp

      /*
      * LSST Data Management System
      * See COPYRIGHT file at the top of the source tree.
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

File Description Comment for Header Files
=========================================

After the boilerplate, any C++ header file should have a Doxygen-style comment block (that begins with ``/**``) that includes the following fields:

1. ``@file`` giving the file's name

2. ``@brief`` to provide a synopsis of the file for Doxygen's index. This should be a line, at most.

3. ``@ingroup`` to specify the name of the LSST Stack package containing this file (see :ref:`below <doc-cpp-package-definition>`).

4. ``@author`` to provide the name of the file's primary author.

For example:

.. code-block:: cpp

   /**
    * @file ExampleClass.cc
    *
    * @brief This message displayed in Doxygen Files index
    *
    * @ingroup PackageName
    * (Note: this needs exactly one @defgroup somewhere)
    *
    * @author Joe Smith
    * Contact: js@lsst.org
    *
    */

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
