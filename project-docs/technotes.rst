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

- **Rubin Technical Notes (RTN).**
  The RTN series is for technotes relating to Operations that cut across individual systems, or relate to functions that cut across departments such as management, planning and operational procedures.
  RTN technotes are hosted in the https://github.com/lsst organization.
  `Find RTN technotes <https://github.com/search?q=org%3Alsst+rtn-&type=Repositories>`_.

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

.. _which-series:

Operations vs construction
--------------------------

The DMTN and SQR series still exist in operations and so it may still be used.
In general if a topic fits in a given series use the series without hesitation.

.. _technote-create:

Create a technote
=================

Creating a new technote is easy and takes just a moment.
In the rubin-obs Slack, send a message to Squarebot:

.. code-block:: text

   /msg @Squarebot create project

From the drop-down, select **Documents > Technote <format>** for the format you wish to work in:

- ``Documents > Technote (reStructuredText)`` creates web-native technotes using the same reStructuredText markup as Python docstrings and most Sphinx documentation
- ``Documents > Technote (Markdown)`` use the same HTML output as above, but with Markdown syntax
- ``Documents > Technote (lsstdoc LaTeX)`` is the LaTeX format for Rubin documents (PDF output)
- ``Documents > Technote (AASTeX LaTeX)`` for AAS preprints (PDF output)
- ``Documents > Technote (ADASS LaTeX)``  for ADASS conference proceedings (PDF output)
- ``Documents > Technote (ASCOM LaTeX)`` for Astronomy & Computing preprints (PDF output)
- ``Documents > Technote (SPIE LaTeX)`` for SPIE conference proceedings (PDF output)

Once you select the template type and fill in the form on Slack, the bot will create and configure the technote on GitHub.
Watch for Slack messages from the bot about the technote's GitHub repository and publication URL.

.. tip::

   The template form asks for your *author ID*.
   You can find your author ID in the `Author DB Google Sheet <https://docs.google.com/spreadsheets/d/1_zXLp7GaIJnzihKsyEAz298_xdbrgxRgZ1_86kwhGPY/edit?usp=drivesdk>`__.
   Send a pull request to update your entry in `authordb.yaml <https://github.com/lsst/lsst-texmf/blob/main/etc/authordb.yaml>`__, or use the Google form linked from the ``#all-users`` channel in Slack.

Updating a technote
-------------------

Any time you push to GitHub, your technote will be republished at its ``lsst.io`` site.
Pushes to the ``main`` branch update your technote's main page, while updates to other branches update preview editions behind the ``/v/`` URL path.
Click on the **Switch editions** or **Change version** link from your published technote to get links for other editions.

.. _technote-rst:

Working with reStructuredText or Markdown technotes
---------------------------------------------------

See the `Documenteer technote documentation <https://documenteer.lsst.io/technotes/index.html>`__ for information on writing and building reStructuredText or Markdown technotes.

.. _technote-latex:

Working with LaTeX-formatted technotes
--------------------------------------

The `lsst-texmf documentation <https://lsst-texmf.lsst.io/lsstdoc.html>`__ explains how to write ``lsstdoc``-based documents.
