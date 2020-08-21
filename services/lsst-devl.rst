###########################
Using the lsst-devl Servers
###########################

``lsst-devl`` is a set of servers run by NCSA for Rubin Observatory development work.

This page is designed to assist developers in their work on the ``lsst-devl`` servers:

#. :ref:`lsst-devl-overview`
#. :ref:`lsst-devl-connect`
#. :ref:`lsst-devl-software`
#. :ref:`lsst-devl-cron`

.. _lsst-devl-overview:

Overview
========

The ``lsst-devl`` nodes can be used for software development, new batch job submission, and longer running interactive work.
Intensive work requiring high CPU/memory usage, long running jobs, storage IO, etc. should be performed from ``lsst-devl`` nodes rather than the ``lsst-login`` nodes.
There are 3 nearly identical ``lsst-devl`` servers to choose from:

- ``lsst-devl01.ncsa.illinois.edu`` (Intel, 24core, 256G RAM)
- ``lsst-devl02.ncsa.illinois.edu`` (Intel, 24core, 256G RAM) (available Sep 14, 2020)
- ``lsst-devl03.ncsa.illinois.edu`` (AMD, 32core, 256G RAM) (available Sep 14, 2020)

To report system issues, please submit an :doc:`IHS ticket <ldf-tickets>` tagging NCSA as the responsible organization.

.. _lsst-devl-connect:

Connecting and Authenticating
=============================

The ``lsst-devl`` nodes can be accessed after first connecting to the :doc:`lsst-login <lsst-login>` nodes. Once connected to an ``lsst-login`` node a user can connect to a ``lsst-devl`` node via its short hostname (e.g., ``lsst-devl01``) without having to enter a password (Kerberos authentication should be used by default; if your Kerberos ticket expires on the login node you may need to ``kinit`` again before proceeding to the ``lsst-devl`` node).

For various suggestions on streamlining connections through the ``lsst-login`` nodes ("jump host" configuration, port forwarding, Kerberos) see :doc:`related documentation <lsst-login>`.

If you using an ``lsst-login`` node as a "jump host" and are authenticating to a ``lsst-devl`` node using a Kerberos ticket from your local machine (workstation/laptop), you may not have a Kerberos ticket when you arrive on the ``lsst-devl`` node itself. You may wish to configure ``GSSAPIDelegateCredentials yes`` in your local ``~/.ssh/config`` file in order to forward your Kerberos credentials to the ``lsst-devl`` node and automatically create a ticket there upon connection.

.. _lsst-devl-software:

Common Software Available
=========================

Refer to :doc:`software` for more details about software available for use on ``lsst-devl`` nodes.


.. _lsst-devl-cron:

CRON Jobs
=========

CRON jobs are disabled by default for users of the ``lsst-devl`` nodes. If a CRON job is necessary, please submit an :doc:`IHS ticket <ldf-tickets>`.

