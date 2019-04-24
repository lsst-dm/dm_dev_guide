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

Follow these steps to create a new technote:

1. Identify the next-available technote handle in the series you are creating a technote for.
   You can do this by searching the series's GitHub organization.

   For example, to identify the next-available DMTN repository, search the `lsst-dm <https://github.com/lsst-dm>`__ organization:

   https://github.com/search?o=desc&q=org%3Alsst-dm+dmtn-&s=updated&type=Repositories

   For discussion, the highest-numbered repository in the search result might be ``https://github.com/lsst-dm/dmtn-100``.
   Try to go to the *next* repository, ``https://github.com/lsst-dm/dmtn-101``:

   - If the page is a 404 (Not Found), that URL corresponds to the next-available repository.

   - If the page exists, keep incrementing the serial number in the URL until you find a page that is unavailable (try visiting ``https://github.com/lsst-dm/dmtn-102``, ``https://github.com/lsst-dm/dmtn-103``, and so on).

2. `Create a GitHub repository <https://help.github.com/articles/creating-a-new-repository/>`_ in the GitHub organization corresponding to the handle you identified in the previous step.
   Leave the repo empty — don't seed it with a ``.gitignore`` or ``README``.

3. Create a Git repository from a template.
   Which template you use depends on the technote's format:

   - If you are creating a reStructuredText-based technote that is built with Sphinx into HTML, run the following commands in a shell:

     .. code-block:: sh

        git clone https://github.com/lsst/templates
        pip install -r templates/requirements.txt
        templatekit make technote_rst

   - If you are creating a LaTeX-formatted technote that is built into a PDF, follow the `lsst-texmf documentation <https://lsst-texmf.lsst.io/templates/document.html>`_

   Be sure to commit and push the new technote to GitHub.
   GitHub provides instructions on how to push to GitHub when you create a new GitHub repository.

4. Message the `#dm-docs <https://lsstc.slack.com/archives/dm-docs>`__ Slack channel so that the Travis integration for your technote can be activated.

   Don't wait to configure your document's deployment.
   By configuring your technote's deployment early on, it's easier for collaborators to view your content.

.. _technote-rst-bib:

Using bibliographies in reStructuredText technotes
==================================================

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
==============================================

ReStructuredText-format technotes use a :file:`metadata.yaml` in their repositories to describe attributes like the document's title, author list, and abstract.
To change the technote's title or author list, for example, commit a change to the :file:`metadata.yaml` file.
See the comments in :file:`metadata.yaml` for a description of these fields.
