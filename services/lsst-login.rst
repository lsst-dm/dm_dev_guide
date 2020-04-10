############################
Using the lsst-login Servers
############################

The following login nodes are run by NCSA for access to select LSST DM development resources:
- ``lsst-login01.ncsa.illinois.edu``
- ``lsst-login02.ncsa.illinois.edu``
- ``lsst-login03.ncsa.illinois.edu``

To get an account, see the :doc:`Onboarding Checklist </team/onboarding>`.

This page is designed to assist developers in use of the ``lsst-login`` servers:

#. :ref:`lsst-login-overview`
#. :ref:`lsst-login-password`
#. :ref:`lsst-login-htcondor`
#. :ref:`lsst-login-slurm`
#. :ref:`lsst-login-development`

.. _lsst-login-overview:

Overview
========

The ``lsst-login`` servers are primarily intended as bastions used to access other resources at NCSA. Additional capabilities are planned to include:
- submission of HTCondor jobs (workflows should not be run here outside of HTCondor)
- submission of Slurm jobs
- light development work with short-running processes that require modest resources (e.g., build docs)

Users are encouraged to submit batch jobs to perform work that requires more significant resources.

The ``lsst-login`` nodes have access to the :doc:`LDF file systems <storage>`.

For system status and issues:
- `Service status <https://confluence.lsstcorp.org/display/DM/LSST+Service+Status+page>`_ including announcements of upcoming planned down-time.
- `Real-time system status <https://monitor-ncsa.lsst.org/>`_ (requires login).
- To report system issues, `file a JIRA ticket <https://jira.lsstcorp.org/secure/CreateIssueDetails!init.jspa?pid=12200&issuetype=10901&priority=10000&customfield_12211=12223&components=14213>`_ in the IT Helpdesk Support (IHS) project.


.. _lsst-login-password:

Account Password
================

You can log into LSST development servers at NCSA with your NCSA account and password along with NCSA Duo.

You can reset your NCSA password at the following URL:

   - https://identity.lsst.org/reset

Information on setting up NCSA Duo is available at the following URL:
   - https://wiki.ncsa.illinois.edu/display/cybersec/Duo+at+NCSA


.. _lsst-login-htcondor:

HTCondor Job Submission
=======================

Job submission to the NCSA HTCondor DAC cluster will be possible from the ``lsst-login`` nodes in the near future.


.. _lsst-login-slurm:

Slurm Job Submission
====================

Job submission to the NCSA Slurm :doc:`Verification Cluster <verification>` will be possible from the ``lsst-login`` nodes in the near future.


.. _lsst-login-development:

Development Work
================

``lsst-login`` nodes can be used for (light) development work in a manner to the :doc:`lsst-dev <lsst-dev>` nodes. (Users are encouraged to utilize batch compute nodes when more significant resources are required.)

The ``lsst-login`` systems are configured with the latest CentOS 7.x as their operating system. This release of CentOS provides an old set of development tools, centered around version 4.8.5 of the GNU Compiler Collection (GCC). Several updated toolchains are made available through the “Software Collection” system as described in the docs for `lsst-dev <lsst-dev>` servers (specific toolchains available on ``lsst-login`` nodes may vary).

A ready-to-use “shared” version of the LSST software stack is provided to enable developers to get up and running quickly with no installation step. See the docs for `lsst-dev <lsst-dev>` servers for more information.
