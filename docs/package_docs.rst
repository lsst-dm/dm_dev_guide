##########################
Documenting Stack Packages
##########################

.. note::

   This is a preview documentation format specification.
   Software documentation should currently be written in the format described at https://confluence.lsstcorp.org/display/LDMDG/Documentation+Standards

The LSST Stack is an aggregation of packages contained in individual git repositories (see `github.com/lsst <https://github.com/lsst>`_).
This page explains how to organize and write package documentation that can be integrated into software documentation, such as the `LSST Science Pipelines <http://pipelines.lsst.io>`_ docs.
In separate pages we cover writing :doc:`docstrings for Python <py_docs>` and :doc:`C++ <cpp_docs>`, respectively.
We use reStructuredText to markup our documentation; see our :doc:`reStructuredText Style Guide <rst_styleguide>` for more information on this markup language.

.. _pkg-doc-pkg-layout:

Layout of a Package: The Doc Perspective
========================================

.. Stack packages are consistently laid out so that documentation of various forms can be found by developers and the robots that continuously deploy the Stack Docs.

From a perspective of documentation, the repository of every Stack package is laid out as follows::

   package_name/
   \ _ ... source files
    |_ README.rst
    |_ LICENSE
    |_ COPYRIGHT
    |_ CONTRIBUTING.rst
    |_ docs/
       \_ index.rst

In the follow sections we describe how to produce the content for each of these documentation files and directories.

.. _pkg-doc-dev-docs:

Developer Documentation: GitHub Summary, README, LICENSE, COPYRIGHT & CONTRIBUTING
==================================================================================

Each repository needs a few files and pieces of metadata to make them approachable for developers.

.. _pkg-doc-github-summary:

GitHub Summary Line
-------------------

From the root GitHub page of a Stack repository (e.g., https://github.com/lsst/afw), you can add/edit the repository's summary and homepage link, located directly below the repository's name.

The **summary** should be a concise one-sentence description the repository.
These summaries are critical for browsing repositories at https://github.com/lsst and for GitHub search.

The **homepage** should be set to the package's user guide page in the deployed software documentation (point to the 'latest' branch of the documentation).

.. _pkg-doc-readme:

README.rst
----------

Every repository needs a README.

READMEs are especially important since GitHub features them prominently on repository homepages.
At the same time, READMEs aren't a primary source of Stack documentation.
Thus we recommend you use your README to describe the purpose of the repository in slightly more detail than the GitHub summary line, and to point developers to the Stack documentation.
At your discretion, READMEs can also be used for developer-centric notices that you feel shouldn't be included in the main documentation.

To be consistent with the rest of the Stack's documentation, READMEs should be in reStructuredText format and named ``README.rst`` in the root of your repository.

We suggest this template:

.. code-block:: rst

   ============
   package_name
   ============

   {{repeat GitHub summary line}}

   ``package_name`` is a package in the LSST Stack.

   Documentation: {{doc url}}

   {{Additional descriptions and developer notices, as needed}}

   License
   -------

   See LICENSE and COPYRIGHT files.

.. _pkg-doc-copyright:

COPYRIGHT
---------

We assert copyright information in a centralized ``COPYRIGHT`` file, located in the repository's root rather than attempting to track copyright in each file separately within a package.
Using a ``COPYRIGHT`` file allows us to maintain copyright information more effectively than in source code comments.
(See `RFC-45 <https://jira.lsstcorp.org/browse/RFC-45>`_ for background on this policy).

Some code written before construction officially started will have an LSST Corporation copyright and this should not be changed unless it has erroneously been used for code after construction began in August 2015.
During LSST construction, copyright is asserted by your employer and not centrally by AURA.

The ``COPYRIGHT`` file should include a line for each legal entity that contributed to the package.
A common example may look like:

.. code-block:: text

   Copyright 2012-2015 LSST Corporation
   Copyright 2015-2017 Association of Universities for Research in Astronomy

Where the year range is changed as appropriate.
If the code in a package has not been touched since 2015 and you are working on it in 2018, do not say "2012-2018" but instead use "2012-2015, 2018".
You can determine this by looking at the repository change history.

.. note::
   Previously it was common to see AURA/LSST in the copyright assignment line.
   This is not a legal entity and the fully-expanded name of AURA should be used.

Use a line per institution even if the years are the same:
E.g.:

.. code-block:: text

   Copyright 2012-2015 LSST Corporation
   Copyright 2012-2015 University of Washington
   Copyright 2015-2018 Association of Universities for Research in Astronomy

These ``COPYRIGHT`` files should be updated during development and may be robotically refreshed.
Automatically updating the files requires people committing to the repository use their :ref:`institutional email address <git-setup-institutional-email>`.

The downside of using a single ``COPYRIGHT`` file is that moving a file between packages requires that both the source and destination ``COPYRIGHT`` files may need to be amended, since the copyright information is not included in the file being moved.

Standard Institutional Copyrights
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The institutions contributing to the Data Management software use the following copyright statements:

* Association of Universities for Research in Astronomy
* University of Washington
* The Trustees of Princeton University
* The Board of Trustees of the Leland Stanford Junior University, through SLAC National Accelerator Laboratory
* University of Illinois Champaign-Urbana
* California Institute of Technology

.. _pkg-doc-license:

LICENSE
-------

A ``LICENSE`` file in the repository's root is the canonical description of LSST's code licensing.

We use the GPLv3 license and a copy of it can be obtained from https://www.gnu.org/licenses/gpl.txt.

.. _pkg-doc-code-preamble:

CODE PREAMBLE
-------------

Each source file needs to include a short license and copyright statement.
This should normally be included in a comment block at the top of the file and should take the following form:

.. literalinclude:: snippets/license_preamble.txt
   :language: text

where the package name is stated explicitly at the top.

.. _pkg-doc-contributing:

CONTRIBUTING.rst
----------------

`GitHub popularized the use of CONTRIBUTING files to help open source developers stay on the same page <https://github.com/blog/1184-contributing-guidelines>`_.
Whenever a GitHub Issue or Pull Request is made, GitHub will display a link to the `CONTRIBUTING.rst` file.

.. code-block:: rst

   #################
   How to Contribute
   #################

   If you've found a bug or have a question
   ========================================

   If you've found a bug, or have a question about using the LSST stack,
   please join us at https://community.lsst.org and post a new topic in
   the `Q&A` category <https://community.lsst.org/c/qa>`_.

   At LSST we don't use GitHub issues to track work. Posting in the forum is
   the best way to contact LSST developers and get help.

   If you haven't consulted with it yet, the `LSST Stack Handbook
   <http://lsst_stack_docs.rtd.org>`_ may also help.

   If you'd like to contribute code
   ================================

   We appreciate getting open source contributions to the LSST Stack. Thanks!
   We've put together a guide for developing on the LSST Stack at
   http://lsst_stack_docs.rtd.org/development/workflow.

   Resources
   =========

   - LSST Community forum: https://community.lsst.org
   - LSST Data Management Homepage: https://dm.lsst.org
   - LSST Stack Handbook: https://lsst_stack_docs.rtd.org

   Team Culture and Conduct Standards
   ==================================

   All interaction within the LSST DM team, and between the community and
   DM are goverened by the `LSST DM Team Culture and Conduct Standards`_.

   .. _LSST DM Team Culture and Conduct Standards: https://confluence.lsstcorp.org/display/LDMDG/Team+Culture+and+Conduct+Standards

.. note:: Some of the documentation URLs listed in this ``CONTRIBUTING.rst`` guide don't exist yet.

.. _pkg-doc-user-guide:

The Package's User Guide in docs/
=================================

The heart of a Stack package's documentation are files in the ``docs/`` directory [#]_.
This content is ingested by Sphinx, our documentation build tool, to publish user guides for each package.
In the following section we describe how to write the main documentation file, ``docs/index.rst``.

..
   For complex packages, documentation can be split across many files in the docs/ directory.
   We cover that use case in a later section.

.. [#] LSST's previous Doxygen-based documentation platform placed its content in the ``doc/`` directory.
   Thus the Sphinx and Doxygen documentation can coexist during the documentation transition.

.. _pkg-doc-template:

Template for a Package's index.rst
----------------------------------

Consistent documentation patterns make it easier for users to read the Docs.
For every package's user guide, we strongly recommend using the following sections:

1. "Introduction"
2. "Getting Started"
3. "Tutorials" (optional)
4. "Using package\_name"
5. *Discretionary sections*
6. "Python Reference"
7. "C++ Reference"

To implement this pattern, every package's ``index.rst`` should follow this basic template:

.. code-block:: rst

   .. _lsst-package-name:

   ###################
   package_name - Slug
   ###################

   .. _lsst-package-name-intro:

   Introduction
   ============

   Tell people what the package does (in a few paragraphs).
   List features here.

   .. _lsst-package-getting-started:

   Getting Started
   ===============

   A quick tutorial that covers the main functionality.
   It should be *brief* (a laptop screen or two) and *shouldn't be exhaustive*.

   .. _lsst-package-getting-started:

   Using package_name
   ==================

   A series of sections that cover API usage.

   Subsections
   -----------

   Use sectioning liberally.

   Other sections
   ==============

   This is where you can put other types of content, such as more
   detailed architectural descriptons for developers.

   .. _lsst-package-name-py-ref:

   Python Reference
   ================

   API reference for Python developers.

   .. _lsst-package-name-cpp-ref:

   C++ Reference
   =============

   API reference for C++ developers

We recommend that the entirety of a package's documentation be contained in a single ``index.rst`` file.
This minimal pagination makes it easier for readers for use their browser's search to find specific phrases.

In the following sections we expand on key concepts in writing a package's user guide.

.. _pkg-doc-sections:

Sections
--------

In keeping with Python community conventions and our :ref:`style guide <rst-sectioning>`, we use the following section markup for different levels of headings:

1. Page title: ``#`` with overline,
2. Sections: ``=``,
3. Subsections: ``-``,
4. Subsubsections: ``^``,
5. Paragraphs: ``"``.

.. _pkg-doc-labels:

Section Labels
--------------

Although Sphinx can automatically provide section link targets, we recommend that you :ref:`provide explicit link targets since they don't change when headline text changes <rst-internal-links>`.

Section labels should be placed directly above the header and follow the syntax ``_label:``.
Note that hyphens should be used to separate words in a label; underscores are only used to prefix the label.

For package documentation, we recommend that you prefix section labels with the Python namespace, joined by hyphens (`-`). For example, the section label for the ``lsst.afw`` package should be:

.. code-block:: rst

   .. _lsst-afw:

By convention, we use the following labels for standardized package sections

* "Introduction:" ``lsst-package-name-intro``
* "Getting Started:" ``lsst-package-name-getting-started``
* "Using package\_name:" ``lsst-package-name-using``
* "Python Reference:" ``lsst-package-name-py-ref``
* "C++ Reference:" ``lsst-package-name-cpp-ref``

.. _pkg-doc-titles:

Titling the Package's User Guide
--------------------------------

We recommend the title for a package's user guide follow the format

.. code-block:: rst

   ########################
   lsst.package_name - Slug
   ########################

That is, the title should provide the Python namespace of the package first, followed by the 'slug.'. The slug is merely a short phrase that elucidates the package's role.
For example,

.. code-block:: rst

   ################################
   lsst.afw - Application Framework
   ################################

.. _pkg-doc-intro:

The 'Introduction' Section
--------------------------

The *Introduction* section should be an approachable summary of what the package does.
Write the Introduction for users who have never used the package before, and need to decide quickly whether this is the package that can solve their problems or not.
Including a bulleted feature list could be a good thing too, but don't be long-winded.

.. _pkg-doc-getting-started:

The 'Getting Started' Section
-----------------------------

The *Getting Started* section is a quick demo, with code that a user could paste into a Jupyter notebook and see something happen.
This section isn't meant to be a complete survey of the package's functionality; it's only meant to say *hey there! you can actually use this thing.*

.. _pkg-doc-tutorials:

The 'Tutorials' Section
-----------------------

This section can provide links to tutorials that use this package.

.. _pkg-doc-using:

The 'Using package\_name' Section
---------------------------------

This section is the heart of the Package's user guide.
This section should be comprehensive and explain all the major functionality of the package.
Code examples should be used liberally.
We encourage you to divide the *Using* section into multiple, short, subsections to ensure it is skimable/navigable.

.. _pkg-doc-py-reference:

The 'Python Reference' Section
------------------------------

The *Python Reference* is generated automatically from the :doc:`Python docstrings <py_docs>`.

.. todo:: Explain how to setup autodoc directives

.. _pkg-doc-cpp-reference:

The 'C++ Reference' Section
---------------------------

The *C++ Reference* is generated automatically from the :doc:`doxygen-formatted C++ code comments <cpp_docs>`.

.. todo:: Explain how to setup the documentation directives

.. _pkg-doc-acknowledgements:

Acknowledgements
================

We credit the `Astropy project <http://docs.astropy.org/en/stable/>`_ for developing the *Introduction - Getting Started - Using - API Reference* pattern for package documentation.
