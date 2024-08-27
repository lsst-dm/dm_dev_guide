######################################
Common Dataset Organization and Policy
######################################

This document covers the specific :ref:`format <datasets_format_usdf>` and :ref:`policies <datasets_policy_usdf>` governing the shared datasets at the USDF, including space available on the :doc:`login nodes </usdf/lsst-login>` and on all of the compute nodes of the :doc:`Batch Systems </usdf/batch>`.

Datasets covered by this policy include raws, calibration files, and refcats. "Refcats" refers to reference catalogs that are used for calibration (astrometric or photometric). Other types of catalogs may be used as references (e.g. DC2 truth tables) but will be referred to as external catalogs.

.. _datasets_file_paths_usdf:

File Paths
==========

The following file paths contain shared datasets:

- ``/sdf/group/rubin/datasets`` (henceforth ``/datasets`` for short) is a symlink to ``/sdf/data/rubin/shared/ncsa-datasets``, containing datasets previously stored at NCSA under the now-defunct ``/datasets`` path (i.e. the ``/datasets`` symlink no longer exists at S3DF).
- ``/sdf/group/rubin/shared`` (henceforth ``/shared`` for short) is a symlink to ``/sdf/data/rubin/shared`` and is the preferred path for new shared datasets, as well as for migrating older datasets.
- ``/sdf/group/rubin/user`` is a symlink to ``/sdf/data/rubin/user`` and contains user home directories. Shared datasets may reside here temporarily for prototyping but should be moved to ``/shared`` once they start being used by multiple users.

.. _datasets_policy_usdf:

Policy
======

New shared datasets should be added to ``/shared``.
Any additions or changes to datasets to be included in a shared butler and/or used in regular (re-)processing must have a corresponding RFC.
Other datasets must include an implementation ticket.

The RFC and/or implementation ticket should contain information about:

- Description and reason for addition/change/deletion
- Target top-level-directory for location of addition/change/deletion
- Organization of data
- Required disk space
- Other necessary domain knowledge as identified by project members relating to the contents of the data

External datasets not yet used in regular reprocessing should have a corresponding Jira ticket with similar information.

All newly-added datasets, including external datasets, must follow the guidelines for supplying a :ref:`README <datasets_readme_guidelines_usdf>` file. Updates to the readme should be reviewed on subsequent Jira tickets.

Requests for new shared directories should be emailed to ``usdf-help@slac.stanford.edu``.
Members of the ``rubinmgr`` group will handle these, including having quotas applied.
Requesting users are often given initial ownership of the shared directory and are responsible for setting appropriate permissions.
If the shared dataset needs central curation, ownership may be set to ``rubinmgr`` after it is initially populated.
More sophisticated options to grant temporary unlocks for modification or to permanently allow curation by a group of users are available on request.

.. _datasets_format_usdf:

Format
======

Most data in ``/datasets`` adheres to the following Gen2 format conventions (caps are tokens):
``/datasets/<camera>/[REPO|RERUN|PREPROCESSED|SIM|RAW|CALIB] | /datasets/REFCATS`` where

- REPO = repo
  (:lmod:`butler` root)
- SIM = <ticket>_<date>/ | <user>/<ticket>/
- CALIB = calib/<date>
  (ex. master20161025)
- RAW = raw/<survey-name>/
  (where actual files live)
- REFCATS = refcats/<type>/<version>/<label>
  (ex. astrometry_net_data/sdss-dr8, htm/v1/gaia_DR1_v1)

The datasets still in use have been ingested via symlink to current Gen3 Butler repositories, and users generally will not need to interact with them.
Additional legacy datasets may reside under the RERUN and PREPROCESSED tags, as well as under ``/datasets/all-sky``.

.. _datasets_reference-catalogs_usdf:

Reference Catalogs
------------------

Gen2 reference catalogs in ``/datasets`` were ingested into a version subdirectory (e.g. ``v0/``, ``v1``) matching the ``REFCAT_FORMAT_VERSION`` set by the refcat ingestion task. New refcats should follow the policies to be detailed in `DM-31704 <https://rubinobs.atlassian.net/browse/DM-31704>`_.

Here is a template for what each refcat's readme should contain:

::

    Reference Catalog: Example
    ##########################

    Sky coverage: full sky (or give ra/dec range)
    Number of sources: 1,234,567
    Magnitude range: 10 - 20 (G magnitude)
    Disk space: 100 GB

    Original data: https://www.example.com/DataRelease9000
    Jira ticket or Epic: https://rubinobs.atlassian.net/browse/DM-Example
    Jira acceptance RFC: https://rubinobs.atlassian.net/browse/RFC-Example
    Contact: Example name, email@example.com, Slack: examplename

    This is a brief paragraph summarizing this reference catalog.

    Citations/acknowledgements
    ==========================
    Users of this reference catalog should follow the citation and
    acknowledgement instructions from this website:
    https://www.example.com/citations

    Catalog creation
    ================
    This catalog was created by following the instructions on this page:
    https://pipelines.lsst.io/modules/lsst.meas.algorithms/creating-a-reference-catalog.html
    The configuration that was used to ingest the data is included in this
    directory as `IngestIndexedReferenceTask.py`.

.. _datasets_butler_ingest_usdf:

Butler Ingest
=============

Shared datasets to be ingested to shared Gen3 Butler repositories should follow established conventions (also to be clarified in `DM-31704 <https://rubinobs.atlassian.net/browse/DM-31704>`_).
Existing repos generally contain instrument-specific datasets in a collection prefixed by the instrument name (e.g. ``HSC/raw``).
Instrument-agnostic datasets may be prefixed by a relevant name, e.g. ``injection`` for source injection datasets or ``pretrained_models``.

External datasets should be included with an ``external`` prefix, e.g. ``external/catalogs`` or ``external/imaging``.
The RFC/ingestion ticket should determine whether external datasets need corresponding dimensions.
For example, a multi-band, multi-instrument catalog covering a small area like COSMOS needs no dimensions, whereas larger catalogs may benefit from htm spatial sharding.
Pre-processed images could benefit from an instrument and filter; best practices for dataset type specification and spatial sharding are TBD.

.. _datasets_readme_guidelines_usdf:

README Guidelines
=================

- Ticket creator is responsible for butler-ization of dataset (or delegation of responsibility).
- Responsibility for maintaining usable datasets is a DM-wide effort.

Regardless of the reason for the RFC (implementation or maintenance), as part of implementing the RFC, any relevant information from the RFC should be transferred to a ``README.txt`` file at the root level of the dataset.
There is no limit to how much information can be put in ``README.txt``, however at the minimum, it should contain:

- A description of the instrument and observatory that produced the data
- The intended purpose of the dataset
- At least a high level summary of the selection criteria for the dataset
- The primary point of contact for questions about the dataset. Name is sufficient, but email would be appreciated.
- If preprocessed, a description of the preprocessed data products available
- If a subset is preprocessed, a description of how the subset was created (and why)

For butler repository datasets, the root level is the directory just above the butler repository: e.g. ``/datasets/hsc/README.txt``.
For reference catalogs, there should be one ``README.txt`` for all reference catalogs of a particular type: e.g. ``/datasets/refcats/htm/README.txt`` with a brief description of the available reference catalogs of that type.
Separately, each reference catalog should also contain a ``README.txt`` with details about that reference catalog's contents.
See `datasets_reference-catalogs_usdf`_ for a template for the contents of those respective readme files.
