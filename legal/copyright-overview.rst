##################################################
Copyrights for LSST DM work and the COPYRIGHT file
##################################################

This page describes how copyrights are assigned and managed for LSST DM source code and documentation.

.. _copyright-updating:

Continuously update copyrights during development
=================================================

All DM developers should participate in keeping copyright statements up to date as you work on the DM codebase.
There is no automated process for updating copyright statements at the moment.

If you move source files between different source repositories, remember to also audit and move copyright assignments as necessary.

.. _copyright-holders:

Copyright holders
=================

.. _copyright-dm:

DM institutions
---------------

LSST Data Management is a collaboration of multiple institutions.
The contracts allow these institutions to retain the copyright for the intellectual property they generate.

Use these legal names when assigning copyright for work you contribute on behalf of your institution:

- Association of Universities for Research in Astronomy
- University of Washington
- The Trustees of Princeton University
- The Board of Trustees of the Leland Stanford Junior University, through SLAC National Accelerator Laboratory
- University of Illinois Champaign-Urbana
- California Institute of Technology

.. _copyright-external:

External contributors
---------------------

Contributions from institutions or individuals outside of DM are accepted and the relevant copyright statement should be included in the file if appropriate.

.. important::

   We do not require copyright assignment to AURA on external code contributions.
   However, small patches are not generally sufficient to grant copyright to the contributor.

.. _copyright-lsst-corp:

LSST Corporation and preconstruction era
----------------------------------------

Prior to the start of LSST construction (before August 2015) all copyright was granted to the LSST Corporation.

.. note::

   Since the beginning of construction (August 2015) some copyrights have been erroneously granted to the LSST Corporation because of a lack of policy communication.
   These post-2015 copyright assignments to LSST Corporation are errors and should be fixed.

.. _copyright-formatting:

Formatting copyright statements
===============================

Copyright statements have the following format:

.. code-block:: jinja

   Copyright {{years}} {{institution}}

When there is more than one institution, include each institution on a separate line.
Lines for each institution are formatted using the above template.

Here is an example of a copyright statement with two contributing institutions:

.. code-block:: text

   Copyright 2012-2015 LSST Corporation
   Copyright 2015-2017 Association of Universities for Research in Astronomy

The "years" in a copyright statement must reflect when contributions were made:

- A single year:

  .. code-block:: text

     Copyright 2015 Association of Universities for Research in Astronomy

- A continuous span of years:

  .. code-block:: text

     Copyright 2015-2018 Association of Universities for Research in Astronomy

- A sequence of multiple single years and spans of years:

  .. code-block:: text

     Copyright 2015-2016, 2018 Association of Universities for Research in Astronomy

  .. code-block:: text

     Copyright 2015, 2017 Association of Universities for Research in Astronomy

.. important::

   Don't use spans to cover years when no contributions were made.

   For example, if the code in a package has not been touched since 2015 and you are working on it in 2018, do not say ``2012-2018`` but instead write ``2012-2015, 2018``.
   You can determine this by looking at the repository change history.

.. _copyright-locations:

Where to record copyright information
=====================================

Where you record copyright information depends on the license that the project is using.
Some licenses, such as the `MIT license`_, provide a place to record the copyright in the license file itself.

For licenses where it's common to record copyrights in individual source files (such as `GPL-3.0`_), Data Management uses a centralized :ref:`COPYRIGHT <copyright-file>` instead.
See the next section.

In some types of projects it's natural to record copyrights in other places, such as READMEs, package metadata, and documentation configuration files.
If you do this, ensure that the extra copyright statements are always updated in step with the legally-binding copyright statement in the :file:`LICENSE` or :file:`COPYRIGHT` files.
For READMEs, it's usually best to just link to the :file:`LICENSE` and :file:`COPYRIGHT` files instead of duplicating information.

.. _copyright-file:

The COPYRIGHT file
==================

For projects whose license requires per-file license preambles (such as `GPL-3.0`_), we record copyright information in a centralized :file:`COPYRIGHT` file, instead of in individual source files.
:doc:`Stack packages use COPYRIGHT files </stack/license-and-copyright>`.

How to implement COPYRIGHT files
--------------------------------

The :file:`COPYRIGHT` is located at the root of the repository, just like :file:`LICENSE`.

:ref:`Format the copyright statements as described above <copyright-formatting>`, with one line per :ref:`copyright holder <copyright-holders>`.
For example:

.. code-block:: text

   Copyright 2012-2015 LSST Corporation
   Copyright 2016, 2018 University of Washington
   Copyright 2015-2018 Association of Universities for Research in Astronomy

The :file:`COPYRIGHT` file does not contain any other content.

`A template <https://github.com/lsst/templates/tree/master/file_templates/copyright>`_ for COPYRIGHT files is available.

Background
----------

Using a :file:`COPYRIGHT` file allows us to maintain copyright information more effectively than in source code comments.

.. seealso::

   See `this article from the Software Freedom Law Center <https://softwarefreedom.org/resources/2012/ManagingCopyrightInformation.html>`_ for background on this policy, which was proposed in :jira:`RFC-45`.

:file:`COPYRIGHT` files are designed to be robotically refreshed, though this automation does not currently exist.
Automatically updating the files requires people committing to the repository to use their :ref:`institutional email address <git-setup-institutional-email>`.

Related pages
=============

- :doc:`licensing-overview`
- :doc:`/stack/license-and-copyright`
- `COPYRIGHT file template <https://github.com/lsst/templates/tree/master/file_templates/copyright>`_

.. _`MIT license`: https://choosealicense.com/licenses/mit/
.. _`GPL-3.0`: https://choosealicense.com/licenses/gpl-3.0/
