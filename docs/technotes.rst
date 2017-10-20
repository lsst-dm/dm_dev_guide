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
- Propose an architecture, possibly becoming the subject of a :ref:`request for comment (RFC) <decision-making-rfc>`.

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
   You can update the title later by modifying the metadata file.

description
   Short abstract for the technote.
   The description is used both as an abstract in the technote itself and in the technote's README.
   You can update the description later by editing the technote and the metadata file.

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
