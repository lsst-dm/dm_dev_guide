.. _stack-documentation-overview:

##########################################
Overview of the Stack documentation system
##########################################

This overview helps developers understand the system that builds and publishes user documentation for LSST’s EUPS-managed Stack products.
This page includes links to further documentation on how to contribute to the documentation.

`pipelines.lsst.io`_ is the documentation site for the ``lsst_distrib`` Stack (the LSST Science Pipelines).

.. _stack-docs-system-main-repo:

Main documentation repository
=============================

Each Stack documentation site has a corresponding **main documentation repository.**
For the `pipelines.lsst.io`_ site, the main documentation repository is `pipelines_lsst_io`_.

The role of the main documentation repository is to set up the structure of the `Sphinx`_ documentation project.
The main documentation repository provides high-level content, such as installation guides, introductory guides and tutorials, and release notes.

Besides its own content, the main documentation repository also creates links into content from :doc:`packages’s doc/ directories <layout-of-doc-directory>` (and see :doc:`add-a-package-to-pipelines-lsst-io`).
The primary examples are the *Modules* and *Packages* sections of the `pipelines_lsst_io`_ homepage that link to :doc:`module homepages <module-homepage-topic-type>` and :doc:`package homepages <package-homepage-topic-type>`, respectively.
These sections are automatically populated by ``module-toctree`` and ``package-toctree``, which are specializations of Sphinx_\ ’s own `toctree`_ directive.
In other words, the *Modules* and *Packages* sections are where package documentation content is added to the main content hierarchy of the `pipelines_lsst_io`_ Sphinx project.

In addition to the *Modules* and *Packages* sections, the :ref:`plan <stack-docs-system-further-reading>` for the `pipelines_lsst_io`_ repository is to also have sections called *Processing* and *Frameworks*. 
The *Processing* section will collect Task documentation and tutorials around specific data processing contexts (single-frame processing, for example).
The *Frameworks* section will gather content from modules and packages around different API themes, called *frameworks,* to help make the package-based codebase easier to rationalize and navigate.
For example, one framework would be the “Task framework,” consisting of APIs from `pipe_base`_, `pipe_supertask`_, and `pex_config`_.
You can think of the *Processing* and *Frameworks* sections as *content playlists* that organize information across multiple packages along topical lines, outside the strict *Modules* and *Packages* hierarchy.

.. _stack-docs-system-packages:

Package documentation
=====================

Packages include their own documentation content in their :doc:`doc/ directories <layout-of-doc-directory>`.
By maintaining documentation in the same repository as the code content, it is easier to keep documentation up-to-date with the implementation.

Documentation for packages is split into two type types of directories, depending on the nature of the package:

- Packages that provide one or more Python modules have corresponding :ref:`module documentation directories <docdir-module-doc-directories>`.

- Packages that do not provide Python modules have :ref:`package documentation directories <docdir-package-doc-directory>` that document the contents of the package.

Content within a package’s :doc:`doc/ directory <layout-of-doc-directory>` is written in :doc:`reStructuredText </restructuredtext/style>`.
Each page conforms to a *topic type* (a template, essentially) that defines the style and structure of the content (see :doc:`package-documentation-topic-types`).
By maintaining consistent information structures, documentation content is both easier to write and easier for readers to use and navigate.

.. _stack-docs-system-build-overview:

The documentation build process
===============================

Documenteer_ is the Python package that provides tooling for LSST DM’s Sphinx-based documentation projects, including Stack user guides such as `pipelines.lsst.io`_.
See :ref:`documenteer:pipelines-build-overview` in the Documenteer documentation for an overview of how the documentation is built.

.. _stack-docs-system-build-deployment:

Documentation deployment
========================

Stack documentation is deployed to the web with LSST the Docs (`SQR-006`_).
The homepage for the LSST Science Pipelines documentation is `pipelines.lsst.io`_.

LSST the Docs hosts multiple editions of documentation that reflect different versions of the project, including releases and development versions.
Jenkins CI, through different release pipelines and the standalone `sqre/infrastructure/documenteer`_ Job, automatically builds and publishes documentation editions for each major, weekly, and daily release.
We also intend to support development branches, though this hasn’t been built into the :doc:`stack-os-matrix <jenkins-stack-os-matrix>` job yet.

The main documentation edition, which is published at https://pipelines.lsst.io without a ``/v/`` path prefix, is the most recent major version of the LSST Science Pipelines.

.. _stack-docs-system-further-reading:

Further reading about the documentation architecture
====================================================

`DMTN-030 Science Pipelines Documentation Design`_ describes the architecture for the Stack documentation system, and content design for the LSST Science Pipelines documentation in particular.
See that technote to understand the design decisions behind the Stack documentation system.

.. note::

   Where information in the Developer Guide and `DMTN-030`_ conflict, follow the guidelines in the Developer Guide.
   `DMTN-030`_ is a design document, whereas the Developer Guide contains practical, up-to-date information on how to implement the design.

.. _`pipelines.lsst.io`: https://pipelines.lsst.io
.. _`pipelines_lsst_io`: https://github.com/lsst/pipelines_lsst_io
.. _Sphinx: http://www.sphinx-doc.org/en/master
.. _toctree: http://www.sphinx-doc.org/en/master/usage/restructuredtext/directives.html#directive-toctree
.. _`pipe_base`: https://github.com/lsst/pipe_base
.. _`pipe_supertask`: https://github.com/lsst/pipe_supertask
.. _`pex_config`: https://github.com/lsst/pex_config
.. _`Documenteer`: https://documenteer.lsst.io/v/DM-14852/
.. _`sqre/infrastructure/documenteer`: https://ci.lsst.codes/blue/organizations/jenkins/sqre%2Finfrastructure%2Fdocumenteer/activity
.. _`SQR-006`: https://sqr-006.lsst.io
.. _`DMTN-030`:
.. _`DMTN-030 Science Pipelines Documentation Design`: https://dmtn-030.lsst.io
