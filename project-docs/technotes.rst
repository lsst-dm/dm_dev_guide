#################################################
Technotes for Stand-Alone Technical Documentation
#################################################

Technotes are a way for Data Management team members to write standalone documents that are native to the web, can be cited in literature, and are easy to write, publish, and update.
You can write with either our reStructuredText or LaTeX templates.
All technotes are developed on GitHub and published with `LSST the Docs`_.

.. _LSST the Docs: https://sqr-006.lsst.io

When to write technotes
=======================

Some of the possible applications for technotes are:

- Report the results of a project, such as a data processing or software development experiment.
- Announce a new technology, serving as a high-level overview complementing user documentation.
- Propose an architecture, possibly becoming the subject of a :doc:`request for comment (RFC) </communications/rfd>`.

For further background, see `SQR-000: The LSST DM Technical Note Publishing Platform <SQR-000>`_.

Technotes are not always the right platform for your information.
Consider these alternatives:

- Change-controlled documentation (``LDM`` documents, for example).
  See :lpm:`19` for guidelines on what kinds of information are change-controlled.
- User documentation (https://pipelines.lsst.io, for example).
  Descriptions of how to use software, services, or data should be written as user documentation.
  Technotes complement user documentation by being point-in-time discussions of software, like a technical blog post.

.. _SQR-000: https://sqr-000.lsst.io

.. _technote-series:

Technote series
===============

- **Data Management Technical Notes (DMTN).**
  This is the general purpose technote series for the DM team.
  DMTN technotes are hosted in the https://github.com/lsst-dm organization.
  `Find DMTN technotes <https://github.com/search?o=desc&q=org%3Alsst-dm+dmtn-&s=updated&type=Repositories>`_.

- **SQuaRE Technical Notes (SQR).**
  This series is for technotes about SQuaRE products and services.
  SQR technotes are hosted in the https://github.com/lsst-sqre organization.
  `Find SQR technotes <https://github.com/search?o=desc&q=org%3Alsst-sqre+sqr-&s=updated&type=Repositories>`_.

- **Simulations Technical Notes (SMTN)**
  This series is for technotes by the LSST Simulations team.
  SMTN technotes are hosted in the https://github.com/lsst-sims organization.
  `Find SMTN technotes <https://github.com/search?o=desc&q=org%3Alsst-sims+smtn-&s=updated&type=Repositories>`_.

.. _technote-create-rst:

Create a reStructuredText technote
==================================

ReStructuredText-formatted technotes are built with Sphinx_ into websites.
Create a reStructuredText-formatted technote by messaging the SQuaRE Bot on Slack:

.. code-block:: text

   @sqrbot project create technote series={{<series>}} title={{<title>}} description={{<description>}}

Set the ``<title>``, ``<description>`` and ``<series>`` fields (see below) for your technote, but keep the ``{{`` and ``}}`` delimiters.

.. note::

   In a Direct Message channel with SQuaRE Bot, don't include the ``@sqrbot`` prefix.

The fields are:

series
   Values can be ``dmtn``, ``sqr`` or ``smtn``.
   Use ``test`` for testing.

title
   Title of the technote.
   The title doesn't include the handle (DMTN, SQR, or SMTN).
   You can update the title later by modifying the :ref:`metadata file <technote-rst-metadata>`.

description
   Short abstract for the technote.
   The description is used both as an abstract in the technote itself and in the technote's README.
   You can update description later by editing the technote and the :ref:`metadata file <technote-rst-metadata>`.

SQuaRE Bot prepares technotes in the background after you make your request.
Go to the GitHub organization for your :ref:`document series <technote-series>` to find your new technote repository.
Reach out on the `#dm-docs <slack-dm-docs>`_ Slack channel for help.

.. _Sphinx: http://www.sphinx-doc.org/en/stable/
.. _stack-dm-docs: https://lsstc.slack.com/messages/C2B6DQBAL/

.. _technote-create-latex:

Create a LaTeX technote
=======================

Technotes can be written as LaTeX documents that are published to the web as PDFs inside landing pages.

Follow the `lsst-texmf documentation <https://lsst-texmf.lsst.io/templates/document.html>`_ to create a new LaTeX-formatted technote.

.. _technote-rst-bib:

Using bibliographies in reStructuredText technotes
==================================================

The lsst-texmf project includes `shared BibTeX bibliographic databases <https://lsst-texmf.lsst.io/lsstdoc.html#bibliographies>`_.
You can also use these bibliographies from reStructuredText technotes.

First, add or uncomment the ``bibliography`` directive at the bottom of your technote's :file:`index.rst` file:

.. code-block:: rst

   .. bibliography:: local.bib lsstbib/books.bib lsstbib/lsst.bib lsstbib/lsst-dm.bib lsstbib/refs.bib lsstbib/refs_ads.bib
      :encoding: latex+latin
      :style: lsst_aa

.. note::

   Only include the :file:`local.bib` file if your technote's repository has one.
   Use :file:`local.bib` to temporarily store bib items before you permanently `transfer them to the lsst-texmf project <https://lsst-texmf.lsst.io/developer.html#updating-bibliographies>`_.

The bibliographies in the :file:`lsstbib` directory are copies from the https://github.com/lsst/lsst-texmf repository.
Refresh the copies maintained in your technote's repository by running this command:

.. code-block:: bash

   make refresh-bib

To make citations in the technote's text, use the ``cite`` role.
For example:

.. code-block:: rst

   :cite:`2007PASP..119.1462B`

In-text citations are numbered, not author-year style.

.. _technote-rst-metadata:

Editing metadata in reStructuredText technotes
==============================================

ReStructuredText-format technotes use a :file:`metadata.yaml` in their repositories to describe attributes like the document's title, author list, and abstract.
To change the technote's title or author list, for example, commit a change to the :file:`metadata.yaml` file.
See the comments in :file:`metadata.yaml` for a description of these fields.
