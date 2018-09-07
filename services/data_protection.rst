###########################
LSST Data Protection Policy
###########################

This policy is based, in part, on the understanding of the level of effort required for
implementation(s) and operation and combined with resource capabilities
(capacity, bandwidth) and likely user expectations.

#. :ref:`protection-overview`
#. :ref:`protection-capability`
#. :ref:`protection-dataprot`
#. :ref:`protection-purge`


.. _protection-overview:

Data Management Policy
======================

This document defines policies regarding acceptable use, data protection capabilities
and use restrictions.

.. _protection-capability:

Capability Acceptable Use
=========================
This policy defines acceptable use of the given capabilities below. In addition, all capability
use must adhere to the following restrictions:

  - Resource usage is restricted to activities directly associated with the project’s development and integration activities during construction.

  - Access is restricted to LSST project personnel and infrastructure personnel residing at NCSA.

  - All access is subject to vetting for security considerations.


Per-Capability Acceptable use
-----------------------------

 - ``/datasets`` - Long term storage of project-approved shared data. All contributions to this location are subject to change control procedures.

 - ``/home`` - Storage of individual-user data.

 - ``/software`` - Central location for maintenance of project-shared software installations that require access from multiple capabilities (ie batch, Nebula). Access is provided to all project members, however, maintenance of the software is based on project role which is subject to change control procedures.

 - ``/sui`` - Shared storage for ephemeral data for the purpose of supporting SUI/T in the PDAC enclave.

 - ``/scratch`` - Ephemeral big-data storage for use in computation and other project-related activities.

 - ``/project`` - Long term big-data storage for use in computation and other project-related activities.

.. _protection-dataprot:

Data Protection Capabilities
============================

NCSA’s Data Management Policy provides for limited recovery from data loss in accordance with the
description and applications as defined below. NCSA does not further warranty the availability of
data than as described. Data owners requiring a greater level of assurance should make other arrangements.

Protection Capabilities
-----------------------

30 day self-serve restore:
    Data locations supporting this tier of protection allow for users to retrieve,
    at their discretion and leisure, a previous data copy limited to a maximum age
    of 30 days. Data set versions are captured at a maximum of one per day.
    
    Those wanting to use this self-serve data retrieval service can go to:
    ``/home/.snapshots/home_YYYYMMDD_0001/<username>/``
    to browse snapshots of their home area on date YYYYMMDD.  These snapshots are
    available for the filesystems listed below (and possibly others). 

Disaster Recovery:
    Data locations supporting this tier of protection provide disjoint-technology protection
    from data loss, accidental or otherwise, to restore to a point-in-time no greater
    than 30 days old. The particular point-in-time is subject to capability limitations.
    This tier does not allow for user-requested data restoration; it is a recovery mechanism
    for catastrophic failure only and limits project value loss due to the failure.

No Protection:
    Data in this tier comes with no integrity or availability assurance beyond standard,
    best-practice data storage techniques.


Note that these capability offerings, although in conformance with data storage best
practices, are limited to the proper service of underlying technology and supporting
infrastructure. NCSA makes no claims nor accepts further liability for loss of data within these offerings.


.. _protection-purge:

Purge Policies
==============

A purge policy defines how and when specific files will be removed from
the filesystem. Purges operate on files only; directories will never be removed by an automated purge.

180-day Purge:
    **Effective October 1, 2017,** a weekly automated process will delete files in :file:`/scratch` and its subdirectories with modification dates > 180 days.
    Please keep in mind that :file:`/scratch` is a place for ephemeral files.
    Use :file:`/datasets` or :file:`/project`  as appropriate for data you need to keep.


Per File System Data Protection
-------------------------------

 - ``/datasets`` - Disaster Recovery only, no purging
 - ``/home`` - 30 day self-serve restore + Disaster Recovery, no purging
 - ``/software`` - 30 day self-serve restore + Disaster Recovery, no purging
 - ``/sui`` - No Protection, no purging
 - ``/scratch`` -  No Protection, 180-day purge policy
 - ``/project`` -  No Protection, no purging

Capacity Restrictions
---------------------

In order to guarantee sufficient capacity in support of LSST development and
integration efforts during the construction phase, quotas are imposed, as shown
below, in order to limit resource consumption and encourage project staff
members to further consider retention of ephemeral data.

 - ``/datasets`` - No quota. Usage subject to project approval procedures.
 - ``/home``- 1TB per user
 - ``/software`` - No quota. Usage subject to project approval procedures.
 - ``/sui`` - No quota. Usage limited to current allocation.
 - ``/scratch`` - No quota. Usage limited by purge procedures.
 - ``/project`` - No quota.


