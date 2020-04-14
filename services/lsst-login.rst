############################
Using the lsst-login Servers
############################

.. ATTENTION:: The lsst-login servers are still being developed and access is currently restricted to select project users and IP addresses.

The following login nodes are run by NCSA for access to select LSST DM development resources:

- ``lsst-login01.ncsa.illinois.edu``
- ``lsst-login02.ncsa.illinois.edu``
- ``lsst-login03.ncsa.illinois.edu``

A round-robin DNS hostname ``lsst-login.ncsa.illinois.edu`` also exists for convenience.

To get an account, see the :doc:`Onboarding Checklist </team/onboarding>`.

This page is designed to assist developers in use of the ``lsst-login`` servers:

#. :ref:`lsst-login-overview`
#. :ref:`lsst-login-connect`
#. :ref:`lsst-login-htcondor`
#. :ref:`lsst-login-slurm`
#. :ref:`lsst-login-development`

.. _lsst-login-overview:

Overview
========

The ``lsst-login`` servers are primarily intended as bastions used to access other resources at NCSA. Additional capabilities are planned to include:

- submission of HTCondor jobs (workflows should not be run here outside of HTCondor)
- submission of Slurm jobs
- light development work with short-running processes that require modest resources (e.g., build docs, short compilations against LSST software stack)
- view files (e.g., FITS files)

Users are encouraged to submit batch jobs to perform work that requires more significant resources.

The ``lsst-login`` nodes have access to the :doc:`LDF file systems <storage>`.

For system status and issues:

- `Service status <https://confluence.lsstcorp.org/display/DM/LSST+Service+Status+page>`_ including announcements of upcoming planned down-time.
- `Real-time system status <https://monitor-ncsa.lsst.org/>`_ (requires login).
- To report system issues, `file a JIRA ticket <https://jira.lsstcorp.org/secure/CreateIssueDetails!init.jspa?pid=12200&issuetype=10901&priority=10000&customfield_12211=12223&components=14213>`_ in the IT Helpdesk Support (IHS) project.

.. _lsst-login-connect:

Connecting and Authenticating
=============================

.. ATTENTION:: The lsst-login servers are still being developed and access is currently restricted to select project users and IP addresses.

You can log into LSST development servers at NCSA with your NCSA account as follows:

   - NCSA username and password **OR** valid Kerberos ticket from workstation/laptop, **AND**
   - NCSA Duo authentication

You can reset your NCSA password at the following URL:

   - https://identity.lsst.org/reset

Information on setting up NCSA Duo is available at the following URL:

   - https://wiki.ncsa.illinois.edu/display/cybersec/Duo+at+NCSA

If you are using OpenSSH on your local machine and you wish to use Kerberos from your local machine (instead of entering your password on the login node), you could add something like this to your local ~/.ssh/config file:

.. prompt:: bash $ auto

  GSSAPIAuthentication yes
  PreferredAuthentications gssapi-with-mic,keyboard-interactive,password

You may wish to use an ``lsst-login`` node as a "jump host". If using OpenSSH on your local machine you can do this as follows:

.. prompt:: bash $ auto

   Host lsst-someinternalhost.ncsa.illinois.edu
      User ncsausername
      ProxyJump lsst-login.ncsa.illinois.edu

When using an ``lsst-login`` node as a "jump host" you may also wish to configure port forwarding through the lsst-login node to the internal cluster node. To do that you would include something like this in your OpenSSH config file:

.. prompt:: bash $ auto

   Host lsst-someinternalhost.ncsa.illinois.edu
      User ncsausername
      ProxyJump lsst-login.ncsa.illinois.edu
      DynamicForward yourportnumber

You may also wish to reuse a single connection to/through an ``lsst-login`` node via a control socket/multiplexing. See for example
`OpenSSH Cookbook - Multiplexing <https://en.wikibooks.org/wiki/OpenSSH/Cookbook/Multiplexing>`_.

.. _lsst-login-htcondor:

HTCondor Job Submission
=======================

Job submission to the NCSA HTCondor DAC cluster will be possible from the ``lsst-login`` nodes in the near future. See :doc:`lsst-condor` for more information.

.. _lsst-login-slurm:

Slurm Job Submission
====================

Job submission to the NCSA Slurm :doc:`Verification Cluster <verification>` will be possible from the ``lsst-login`` nodes in the near future.

.. _lsst-login-development:

Development Work
================

``lsst-login`` nodes can be used for (light) development work in a manner to the :doc:`lsst-dev <lsst-dev>` nodes. (Users are encouraged to utilize batch compute nodes when more significant resources are required.)

The ``lsst-login`` systems are configured with the latest CentOS 7.x as their operating system. This release of CentOS provides an old set of development tools, centered around version 4.8.5 of the GNU Compiler Collection (GCC). Several updated toolchains are made available through the “Software Collection” system as described in the docs for :doc:`lsst-dev <lsst-dev>` servers (specific toolchains available on ``lsst-login`` nodes may vary).

A ready-to-use “shared” version of the LSST software stack is provided to enable developers to get up and running quickly with no installation step. See the docs for :doc:`lsst-dev <lsst-dev>` servers for more information.
