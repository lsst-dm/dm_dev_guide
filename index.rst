#######################
LSST DM Developer Guide
#######################

`LSST Data Management (DM) <http://dm.lsst.org>`_ is building the software that will enable scientific discovery with the Large Synoptic Survey Telescope (`LSST <http://www.lsst.org>`_).
LSST will collect over 50 PB of raw data, resulting in over 30 trillion observations of 40 billion astronomical sources.

All LSST DM code is open source and available on `GitHub <https://github.com/lsst>`_.
Our `LSST Science Pipelines <https://github.com/lsst>`_ will implement the core image processing and data analysis algorithms needed to process optical survey imaging data at low latency and unprecedented scale and accuracy.
`Qserv <http://slac.stanford.edu/exp/lsst/qserv/>`_ is a distributed, shared-nothing SQL database query system to efficiently store, query, and analyze catalogs running into trillions of rows and petabytes of data the LSST will generate.
`Firefly <https://github.com/lsst/firefly>`_, and other tools, will enable astronomers to query, download, visualize, and analyze LSST data.

This Guide will help you in contributing to the DM development effort.

DM Developers can make this guide better by contributing to the https://github.com/lsst-dm/dm_dev_guide repo.
The `README <https://github.com/lsst-dm/dm_dev_guide/blob/master/README.md>`__ will get you started.

.. TEAM SECTION ==============================================================

.. Hidden toctree to manage the sidebar navigation. Match the contents list below.

.. toctree::
   :maxdepth: 1
   :caption: Team
   :hidden:

   team/onboarding
   team/code-of-conduct
   team/empowerment
   team/drp

.. Table of contents published on the homepage.
.. Mirror changes here to team/index.rst (temporary workflow)

.. _part-team:

Team
====

Basic information about the LSST Data Management Subsystem and our culture.
Learn more about the Data Management Subsystem in :ldm:`294`.

- :doc:`team/onboarding`
- :doc:`team/code-of-conduct`
- :doc:`team/empowerment`

Team-specific pages:

- :doc:`team/drp`

.. COMMUNICATIONS SECTION ====================================================

.. Hidden toctree to manage the sidebar navigation. Match the contents list below.

.. toctree::
   :maxdepth: 1
   :caption: Communications
   :hidden:

   communications/slack-github-username.rst
   communications/rfc.rst
   communications/rfd.rst
   communications/wiki.rst
   communications/presenting-at-conferences.rst

.. Table of contents published on the homepage.
.. Mirror changes here to team/index.rst (temporary workflow)

.. _part-communications:

Communications
==============

How to use DM's communication channels.

- :doc:`communications/slack-github-username`
- :doc:`communications/rfc`
- :doc:`communications/rfd`
- :doc:`communications/wiki`
- :doc:`communications/presenting-at-conferences`

.. PROJECT DOCS SECTION ======================================================

.. Hidden toctree to manage the sidebar navigation. Match the contents list below.

.. toctree::
   :maxdepth: 1
   :caption: Project docs
   :hidden:

   project-docs/change-controlled-docs.rst
   project-docs/publication-policy.rst
   project-docs/technotes.rst

.. _part-project-docs:

Project documentation
=====================

Controlled documentation and publications.

- :doc:`project-docs/change-controlled-docs`
- :doc:`project-docs/publication-policy`

Technical notes.

- :doc:`project-docs/technotes`

.. WORK MANAGEMENT SECTION ===================================================

.. Hidden toctree to manage the sidebar navigation. Match the contents list below.

.. toctree::
   :maxdepth: 1
   :caption: Work
   :hidden:

   work/flow.rst
   work/project-planning.rst
   work/jira-agile.rst
   work/jira-tips.rst

.. _part-work:

Work management
===============

How DM coordinates work and gets things done.

- :doc:`work/flow`
- :doc:`work/project-planning`
- :doc:`work/jira-agile`
- :doc:`work/jira-tips`

.. -------------------

.. _part-guides:

Development guides
==================

.. DEVELOPMENT OVERVIEW SECTION ==============================================

.. Hidden toctree to manage the sidebar navigation. Match the contents list below.

.. toctree::
   :maxdepth: 1
   :caption: Code Style Guides
   :hidden:

   coding/intro.rst
   coding/unit-test-policy.rst

.. _part-dev-guides-overview:

Overview of Code Style Guides & Policies
----------------------------------------

- :doc:`coding/intro`
- :doc:`coding/unit-test-policy`

.. C++ SECTION ===============================================================

.. Hidden toctree to manage the sidebar navigation. Match the contents list below.

.. toctree::
   :maxdepth: 1
   :caption: C++
   :hidden:

   cpp/style
   cpp/api-docs
   cpp/clang-format
   cpp/testing-private-functions
   cpp/templates
   cpp/boost
   cpp/eigen
   cpp/profiling

.. _part-cpp:

C++
---

- :doc:`cpp/style`
- :doc:`cpp/api-docs`
- :doc:`cpp/clang-format`
- :doc:`cpp/testing-private-functions`
- :doc:`cpp/templates`
- :doc:`cpp/boost`
- :doc:`cpp/eigen`
- :doc:`cpp/profiling`

.. PYTHON SECTION ============================================================

.. Hidden toctree to manage the sidebar navigation. Match the contents list below.

.. toctree::
   :maxdepth: 1
   :caption: Python
   :hidden:

   python/style
   python/testing
   python/numpydoc
   python/astropy
   python/profiling

.. _part-python:

Python
------

- :doc:`python/style`
- :doc:`python/testing`
- :doc:`python/numpydoc`
- :doc:`python/astropy`
- :doc:`python/profiling`

.. PYBIND11 SECTION ==========================================================

.. Hidden toctree to manage the sidebar navigation. Match the contents list below.

.. toctree::
   :maxdepth: 1
   :caption: Pybind11
   :hidden:

   pybind11/style
   pybind11/how-to

.. _part-pybind11:

Pybind11
--------

- :doc:`pybind11/style`
- :doc:`pybind11/how-to`

.. JAVASCRIPT SECTION ========================================================

.. Hidden toctree to manage the sidebar navigation. Match the contents list below.

.. toctree::
   :maxdepth: 1
   :caption: JavaScript
   :hidden:

   javascript/jsdoc

.. _part-javascript:

JavaScript
----------

- :doc:`javascript/jsdoc`

.. RESTRUCTUREDTEXT SECTION ==================================================

.. Hidden toctree to manage the sidebar navigation. Match the contents list below.

.. toctree::
   :maxdepth: 1
   :caption: ReStructuredText
   :hidden:

   restructuredtext/style

.. _part-rst:

ReStructuredText
----------------

- :doc:`restructuredtext/style`

.. STACK SECTION =============================================================

.. Hidden toctree to manage the sidebar navigation. Match the contents list below.

.. toctree::
   :maxdepth: 1
   :caption: DM Stack
   :hidden:

   stack/platforms
   stack/package-docs
   stack/transferring-code
   stack/logging
   stack/debug
   stack/jenkins-stack-os-matrix
   stack/unit-test-coverage.rst
   stack/lsstsw
   stack/eups-tutorial
   stack/adding-a-new-package
   stack/packaging-third-party-eups-dependencies
   stack/renaming-a-package

.. _part-dm-stack:

DM Stack
--------

- :doc:`stack/platforms`
- :doc:`stack/package-docs`
- :doc:`stack/transferring-code`
- :doc:`stack/logging`
- :doc:`stack/debug`
- :doc:`stack/jenkins-stack-os-matrix`
- :doc:`stack/unit-test-coverage`
- :doc:`stack/lsstsw`
- :doc:`stack/eups-tutorial`
- :doc:`stack/adding-a-new-package`
- :doc:`stack/packaging-third-party-eups-dependencies`
- :doc:`stack/renaming-a-package`

.. GIT SECTION ===============================================================

.. Hidden toctree to manage the sidebar navigation. Match the contents list below.

.. toctree::
   :maxdepth: 1
   :caption: Git
   :hidden:

   git/setup
   git/git-lfs

.. _part-git:

Git
---

- :doc:`git/setup`
- :doc:`git/git-lfs`

.. EDITORS SECTION ===========================================================

.. Hidden toctree to manage the sidebar navigation. Match the contents list below.

.. toctree::
   :maxdepth: 1
   :caption: Editors
   :hidden:

   editors/emacs
   editors/sublime
   editors/vim

.. _part-editors:

Editors
-------

Crowd-sourced recommendations for configuring editors for LSST development (listed alphabetically)

- :doc:`editors/emacs`
- :doc:`editors/sublime`
- :doc:`editors/vim`

.. -------------------

.. toctree::
   :maxdepth: 1
   :caption: Build, Test, Release
   :name: part-build-ci

   build-ci/jenkins.rst

.. toctree::
   :maxdepth: 1
   :caption: Developer Services
   :name: part-services

   services/lsst-dev.rst
   services/lsst-db.rst
   services/verification.rst
   services/datasets.rst
   services/data_protection.rst
   services/ncsa_bulk_transfer.rst
   services/nebula/index.rst
   services/orchestration/index.rst
