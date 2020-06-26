#################################################
Technotes for Stand-Alone Technical Documentation
#################################################

Technotes are a way for Data Management team members to write standalone documents that are native to the web, can be cited in literature, and are easy to write, publish, and update.
You can write with either our reStructuredText or LaTeX templates.
All technotes are developed on GitHub and published with `LSST the Docs`_.
You can find a listing of available technotes at `www.lsst.io <https://www.lsst.io>`__.

.. _LSST the Docs: https://sqr-006.lsst.io

When to write technotes
=======================

Some of the possible applications for technotes are:

- Report the results of a project, such as a data processing or software development experiment.
- Announce a new technology, serving as a high-level overview complementing user documentation.
- Propose an architecture, possibly becoming the subject of a :doc:`request for comment (RFC) </communications/rfd>`.

For further background, see `SQR-000: The LSST DM Technical Note Publishing Platform`_.

Technotes are not always the right platform for your information.
Consider these alternatives:

- Change-controlled documentation (``LDM`` documents, for example).
  See :lpm:`19` for guidelines on what kinds of information are change-controlled.
- User documentation (https://pipelines.lsst.io, for example).
  Descriptions of how to use software, services, or data should be written as user documentation.
  Technotes complement user documentation by being point-in-time discussions of software, like a technical blog post.

.. _`SQR-000: The LSST DM Technical Note Publishing Platform`: https://sqr-000.lsst.io

.. _technote-series:

Technote series
===============

- **Data Management Technical Notes (DMTN).**
  This is the general purpose technote series for the DM team.
  DMTN technotes are hosted in the https://github.com/lsst-dm organization.
  `Find DMTN technotes <https://github.com/search?o=desc&q=org%3Alsst-dm+dmtn-&s=updated&type=Repositories>`_.

- **LSST Operations Technical Notes (OPSTN).**
  This series if for technotes by LSST Operations.
  OPSTN technotes are hosted in the https://github.com/lsst-ops organization.
  `Find OPSTN technotes <https://github.com/search?o=desc&q=org%3Alsst-ops+opstn-&s=updated&type=Repositories>`_.

- **Project Science Team Technical Notes (PSTN).**
  This series is for technotes by the LSST PST.
  PSTN technotes are hosted in the https://github.com/lsst-pst organization.
  `Find PSTN technotes <https://github.com/search?o=desc&q=org%3Alsst-pst+pstn-&s=updated&type=Repositories>`_.

- **Systems Integration, Test and Commissioning Technical Notes (SITCOMTN).**
  This series is for technotes by the System Integration, Test and Commissioning Team.
  SITCOMTN technotes are hosted in the https://github.com/lsst-sitcom organization.
  `Find SITCOMTN technotes <https://github.com/search?o=desc&q=org%3Alsst-sitcom+sitcomtn-&s=updated&type=Repositories>`_.

- **SQuaRE Technical Notes (SQR).**
  This series is for technotes about SQuaRE products and services.
  SQR technotes are hosted in the https://github.com/lsst-sqre organization.
  `Find SQR technotes <https://github.com/search?o=desc&q=org%3Alsst-sqre+sqr-&s=updated&type=Repositories>`_.

- **Simulations Technical Notes (SMTN)**
  This series is for technotes by the LSST Simulations team.
  SMTN technotes are hosted in the https://github.com/lsst-sims organization.
  `Find SMTN technotes <https://github.com/search?o=desc&q=org%3Alsst-sims+smtn-&s=updated&type=Repositories>`_.

.. _technote-create:

Create a technote
=================

Creating a new technote is easy and takes just a moment.
In Slack, open a |dmw-sqrbot| and type:

.. code-block:: text

   create project

From the drop-down, select **Documents > Technote (reStructuredText)** or **(lsstdoc LaTeX)** depending on the format you wish to work in.
Once you select the template type and fill in the form on Slack, the bot will create and configure the technote on GitHub.
Watch for Slack messages from the bot about the technote's GitHub repository and publication URL.

Any time you push to GitHub, your technote will be republished at its ``lsst.io`` site.
Pushes to the ``master`` branch update your technote's main page, while updates to other branches update preview editions behind the ``/v/`` URL path.
Click on the **Switch editions** or **Change version** link from your published technote to get links for other editions.

.. _technote-latex:

Working with LaTeX-formatted technotes
======================================

LaTeX-formatted technotes use the ``lsstdoc`` class.
The `lsst-texmf documentation <https://lsst-texmf.lsst.io/lsstdoc.html>`__ explains how to write ``lsstdoc``-based documents.

.. _technote-rst:

Working with reStructuredText-formatted technotes
=================================================

See the :doc:`/restructuredtext/style` for a primer on writing reStructuredText.
The sections below deal with specific issues for technote projects.

.. _technote-rst-bib:

Using bibliographies in reStructuredText technotes
--------------------------------------------------

The lsst-texmf project includes `shared BibTeX bibliographic databases <https://lsst-texmf.lsst.io/lsstdoc.html#bibliographies>`_.
You can also use these bibliographies from reStructuredText technotes.

First, add or uncomment the ``bibliography`` directive at the bottom of your technote's :file:`index.rst` file:

.. code-block:: rst

   .. bibliography:: local.bib lsstbib/books.bib lsstbib/lsst.bib lsstbib/lsst-dm.bib lsstbib/refs.bib lsstbib/refs_ads.bib
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
----------------------------------------------

ReStructuredText-format technotes use a :file:`metadata.yaml` in their repositories to describe attributes like the document's title, author list, and abstract.
To change the technote's title or author list, for example, commit a change to the :file:`metadata.yaml` file.
See the comments in :file:`metadata.yaml` for a description of these fields.
