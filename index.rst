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

- :doc:`communications/rfc`
- :doc:`communications/rfd`
- :doc:`communications/wiki`
- :doc:`communications/presenting-at-conferences`

.. toctree::
   :maxdepth: 1
   :caption: Processes
   :name: part-processes

   processes/workflow.rst
   processes/transferring_code.rst
   processes/project_planning.rst
   processes/jira_agile.rst
   processes/publication-policy.rst

.. seealso::

   `DMTN-027: Renaming an LSST git Repository <https://dmtn-027.lsst.io>`_.

.. toctree::
   :maxdepth: 1
   :caption: Coding Guides
   :name: part-coding

   coding/intro.rst
   coding/python_style_guide.rst
   coding/cpp_style_guide.rst
   coding/pybind11_style_guide.rst
   coding/using_cpp_templates.rst
   coding/using_boost.rst
   coding/using_astropy.rst
   coding/using_eigen.rst
   coding/unit_test_policy.rst
   coding/python_testing.rst
   coding/unit_test_private_functions.rst
   coding/unit_test_coverage.rst
   coding/profiling.rst
   coding/logging.rst
   coding/debug.rst
   coding/python_wrappers_for_cpp_with_pybind11.rst

.. toctree::
   :maxdepth: 1
   :caption: Writing Docs
   :name: part-docs

   docs/change-controlled-docs.rst   
   docs/technotes.rst
   docs/rst_styleguide.rst
   docs/package_docs.rst
   docs/py_docs.rst
   docs/cpp_docs.rst
   docs/jsdoc.rst

.. toctree::
   :maxdepth: 1
   :caption: Developer Tools
   :name: part-tools

   communications/slack-github-username.rst
   tools/git_setup.rst
   tools/git_lfs.rst
   tools/jira_tips.rst
   tools/clang_format.rst
   tools/sublime.rst
   tools/emacs.rst
   tools/vim.rst

.. toctree::
   :maxdepth: 1
   :caption: Build, Test, Release
   :name: part-build-ci

   build-ci/platforms.rst
   build-ci/eups_tutorial.rst
   build-ci/jenkins.rst
   build-ci/jenkins-stack-os-matrix.rst
   build-ci/lsstsw.rst
   build-ci/new_package.rst
   build-ci/third_party.rst

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
