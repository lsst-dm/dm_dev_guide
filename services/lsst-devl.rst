###########################
Using the lsst-devl Servers
###########################

``lsst-devl`` is a set of servers run by NCSA for Rubin Observatory development work.

This page is designed to assist developers in their work on the ``lsst-devl`` servers:

#. :ref:`lsst-devl-overview`
#. :ref:`lsst-devl-connect`
#. :ref:`lsst-devl-gpfs`
#. :ref:`lsst-devl-tools`
#. :ref:`lsst-devl-loadlsst`
#. :ref:`lsst-devl-testdata`
#. :ref:`lsst-devl-gitlfs`
#. :ref:`lsst-devl-xpra`

.. _lsst-devl-overview:

lsst-devl: Overview
=============================

The ``lsst-devl`` nodes can be used for software development, new batch job submission, and longer running interactive work.
Any intensive work requiring high CPU/memory usage, long running jobs, storage IO, etc. should be performed from ``lsst-devl`` nodes, rather than the ``lsst-login`` nodes.
There are 3 nearly identical ``lsst-devl`` servers to choose from:

- ``lsst-devl01.ncsa.illinois.edu`` (Intel, 24core, 256G RAM)
- ``lsst-devl02.ncsa.illinois.edu`` (Intel, 24core, 256G RAM) (available Sep 14, 2020)
- ``lsst-devl03.ncsa.illinois.edu`` (AMD, 32core, 256G RAM) (available Sep 14, 2020)

To report system issues, log into `LSST JIRA <https://jira.lsstcorp.org/>`_ and file a `JIRA ticket in the IT Helpdesk Support <https://ls.st/ihsticket>`_ project tagging NCSA as the responsible organization.

.. _lsst-devl-connect:

lsst-devl: Connecting and Authenticating
==================================================

The ``lsst-devl`` nodes can be accessed after first connecting to the :doc:`lsst-login <lsst-login>` nodes. Once connected to an ``lsst-login`` node a user can connect to a ``lsst-devl`` node via its short hostname (e.g., ``lsst-devl01``) without having to enter a password (Kerberos authentication should be used by default; if your Kerberos ticket expires on the login node you may need to ``kinit`` again before proceeding to the ``lsst-devl`` node).

For various suggestions on streamlining connections through the ``lsst-login`` nodes ("jump host" configuration, port forwarding, Kerberos) see :doc:`related documentation <lsst-login>`.

If you using an ``lsst-login`` node as a "jump host" and are authenticating to a ``lsst-devl`` node using a Kerberos ticket from your local machine (workstation/laptop), you may not have a Kerberos ticket when you arrive on the ``lsst-devl`` node itself. You may wish to configure ``GSSAPIDelegateCredentials yes`` in your local ``~/.ssh/config`` file in order to forward your Kerberos credentials to the ``lsst-devl`` node and automatically create a ticket there upon connection.

.. _lsst-devl-gpfs:

lsst-devl: GPFS Directory Spaces
==========================================

The ``lsst-devl`` nodes utilize the General Parallel File System (GPFS) to provide shared storage across all of the nodes.

For convenience the bind mounts  :file:`/scratch` , :file:`/project` , :file:`/datasets` ,  and :file:`/software`  have been created to provide views into corresponding spaces in GPFS.

Please see :doc:`Storage Resources <storage>` for more general information.

To add/change/delete datasets, see :doc:`Common Dataset Organization and Policy </services/datasets>`.

.. _lsst-devl-tools:

Select Appropriate Developer Tools
==================================

Refer to :ref:`lsst-login-tools` for general notes on setting up software collection developer tools.

.. _lsst-devl-loadlsst:

Load the LSST Environment
=========================

Refer to :ref:`lsst-login-loadlsst` for notes on loading the LSST environment.

.. _lsst-devl-testdata:

Validation/Test Data Sets
=========================

Refer to :ref:`lsst-login-testdata` for notes on our validation and test data sets.

.. _lsst-devl-gitlfs:

Configure Git LFS
=================

Refer to :ref:`lsst-login-gitlfs` for notes on configuring Git LFS.

.. _lsst-devl-xpra:

Configure Remote Display with :command:`xpra`
=============================================

Refer to :ref:`lsst-login-xpra` for notes on configuring remote display with :command:`xpra`.
