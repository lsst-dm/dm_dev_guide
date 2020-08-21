###########################
Using the lsst-devl Servers
###########################

``lsst-devl`` is a set of servers run by NCSA for Rubin Observatory development work.

This page is designed to assist developers in their work on the ``lsst-devl`` servers:

#. :ref:`lsst-devl-overview`
#. :ref:`lsst-devl-connect`
#. :ref:`lsst-devl-resources`
#. :ref:`lsst-devl-stack`
#. :ref:`lsst-devl-data`
#. :ref:`lsst-devl-processing`
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

To report system issues, log into `LSST JIRA <https://jira.lsstcorp.org/>`_ and file a `JIRA ticket in the IT Helpdesk Support <https://ls.st/ihsticket>`_ project tagging NCSA as the responsible organization.

.. _lsst-devl-connect:

Connecting and Authenticating
=============================

The ``lsst-devl`` nodes can be accessed after first connecting to the :doc:`lsst-login <lsst-login>` nodes. Once connected to an ``lsst-login`` node a user can connect to a ``lsst-devl`` node via its short hostname (e.g., ``lsst-devl01``) without having to enter a password (Kerberos authentication should be used by default; if your Kerberos ticket expires on the login node you may need to ``kinit`` again before proceeding to the ``lsst-devl`` node).

For various suggestions on streamlining connections through the ``lsst-login`` nodes ("jump host" configuration, port forwarding, Kerberos) see :doc:`related documentation <lsst-login>`.

If you using an ``lsst-login`` node as a "jump host" and are authenticating to a ``lsst-devl`` node using a Kerberos ticket from your local machine (workstation/laptop), you may not have a Kerberos ticket when you arrive on the ``lsst-devl`` node itself. You may wish to configure ``GSSAPIDelegateCredentials yes`` in your local ``~/.ssh/config`` file in order to forward your Kerberos credentials to the ``lsst-devl`` node and automatically create a ticket there upon connection.

.. _lsst-devl-resources:

Developer Resources
===================

.. _lsst-devl-editors:

Text Editors
------------

The following basic text editors are installed and available: ``vim``, ``emacs``, ``nano``

.. tip::

   Several developers have setup integrations with their remote editors to connect to ``lsst-devl`` nodes (e.g. rsub/rmate, VSCode, tramp integrations). Ask peers for advice on how they do this.


.. _lsst-devl-git:

Git
---

While most developers use ``git`` from the :ref:`lsst-devl-stack`, a relatively recent version of ``git`` (2.24.x) is also installed as a package from `IUS YUM repo <https://ius.io/>`_ on the host. 

.. _lsst-devl-terminal-multiplex:

Terminal Multiplexers
---------------------

We install both ``screen`` and ``tmux`` for attaching and managing several pseudoterminal-based sessions.
Here are some tutorials for each:

 - `How to use screen <https://linuxize.com/post/how-to-use-linux-screen/>`_
 - `Getting started with tmux <https://linuxize.com/post/getting-started-with-tmux/>`_

.. _lsst-devl-compilers:

Compilers, Debuggers, & Build Tools
-----------------------------------

In addition to developer tools provided by the :ref:`lsst-devl-stack`, the following tools are installed as OS packages:

- **Compilers**: ``c``, ``c++``, and ``fortran`` from gcc 4.8.5
- **Debuggers**: ``glibc-debuginfo`` (i.e. ``gdb``)
- **Build Tools**: ``autoconf``, ``automake``, ``bison``, ``blas``, ``byacc``, ``cmake``, ``flex``, ``fontconfig``, ``make``, ``valgrind``, ``yum-utils``, etc.

Refer to :ref:`lsst-login-tools` for details on using an optional ``devtoolset`` from SCL.

.. _lsst-devl-x11-xpra:

X11 & Xpra
----------

Refer to :ref:`lsst-login-xpra` for details on using X11 or Xpra.

.. _lsst-devl-misc:

Miscellaneous Packages
----------------------

A few other developer resources are also installed directly as OS packages:

- ImageMagick
- Midnight Commander
- PostgreSQL client
- The Silver Searcher
- sqlite3


.. _lsst-devl-stack:

LSST Software Stack
===================

.. _lsst-devl-stack-shared:

Shared Software Stack
---------------------

A shared software stack on the GPFS file systems has been provided and is maintained by Science Pipelines and is available under :file:`/software/lsstsw`.

Refer to :ref:`lsst-login-loadlsst` for details on loading and using the shared LSST software stack.

.. _lsst-devl-stack-setup:

LSST Stack Setup
----------------

(Add content related to ``setup``, ``eups``, ``conda``, etc.)

.. _lsst-devl-stack-python:

LSST Stack Python
-----------------

(Add content related to using ``python``, ``pip``, ``iPython``, ``jupyter``, etc. from the LSST Stack)
	
.. _lsst-devl-stack-tasks:

LSST Stack Tasks
----------------

(Add content related to using pipeline tasks from the LSST Stack)


.. _lsst-devl-data:

Accessing Data
==============

.. _lsst-devl-data-gpfs:

GPFS Directory Spaces
---------------------

The ``lsst-devl`` nodes utilize the General Parallel File System (GPFS) to provide shared storage across all of the nodes.

For convenience the bind mounts  :file:`/home` , :file:`/scratch` , :file:`/project` , :file:`/datasets` ,  and :file:`/software`  have been created to provide views into corresponding spaces in GPFS.

Refer to :doc:`Storage Resources <storage>` for more general information.

To add/change/delete datasets, see :doc:`Common Dataset Organization and Policy </services/datasets>`.

.. _lsst-devl-data-sets:

Validation/Test Data Sets
-------------------------

Refer to :ref:`lsst-login-testdata` for details on validation and test data sets available.


.. _lsst-devl-processing:

Processing Data
===============

Users are encouraged to submit batch jobs to perform work that requires more significant resources. Refer to :doc:`/services/batch` for more information.

.. _lsst-devl-processing-interactive:

Interactive Batch Jobs
----------------------

Refer to :ref:`batch-htcondor-interactive-job` for details on how to submit simple, interactive batch jobs.

.. _lsst-devl-processing-batch:

Submit Batch Jobs
-----------------

Refer to :doc:`batch` for details on how to submit batch jobs.


.. _lsst-devl-cron:

CRON Jobs
=========

CRON jobs are disabled by default for users of the ``lsst-devl`` nodes. If a CRON job is necessary, please submit an IHS ticket.

