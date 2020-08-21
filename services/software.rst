##############################
Software Common to LDF Servers
##############################

LSST developers have a set of common software packages and tools that are installed and available on many servers in the LDF.

#. :ref:`software-overview`
#. :ref:`software-connect`
#. :ref:`software-system`
#. :ref:`software-stack`
#. :ref:`software-data`
#. :ref:`software-processing`
#. :ref:`software-cron`

.. _software-overview:

Overview
========

This page is designed to assist developers with common software available on :doc:`lsst-login <lsst-login>`, :doc:`lsst-devl <lsst-devl>`, and :doc:`batch <batch>` servers.

To report system issues, please submit an :doc:`IHS ticket <ldf-tickets>` tagging NCSA as the responsible organization.

.. _software-connect:

Connecting and Authenticating
=============================

Most LDF server nodes can be accessed after first connecting to the :doc:`lsst-login <lsst-login>` nodes. Once connected to an ``lsst-login`` node a user can connect to a node via its short hostname (e.g., ``lsst-devl01``) without having to enter a password (Kerberos authentication should be used by default; if your Kerberos ticket expires on the login node you may need to ``kinit`` again before proceeding to the second node).

For various suggestions on streamlining connections through the ``lsst-login`` nodes ("jump host" configuration, port forwarding, Kerberos) see :ref:`related documentation <lsst-login-connect>`.

If you using an ``lsst-login`` node as a "jump host" and are authenticating to another server node using a Kerberos ticket from your local machine (workstation/laptop), you may not have a Kerberos ticket when you arrive on the second node. You may wish to configure ``GSSAPIDelegateCredentials yes`` in your local ``~/.ssh/config`` file in order to forward your Kerberos credentials to the second node and automatically create a ticket there upon connection.

.. _software-system:

System Level Software
=====================

.. _software-editors:

Text Editors
------------

The following basic text editors are installed and available: ``vim``, ``emacs``, ``nano``

.. tip::

   Several developers have setup integrations with their remote editors to connect to LSST server nodes (e.g. rsub/rmate, :doc:`VSCode </editors/vscode>`, :doc:`SublimeText </editors/sublime>`, tramp integrations). Ask peers for advice on how they do this.


.. _software-git:

Git
---

While most developers use ``git`` from the :ref:`software-stack`, a relatively recent version of ``git`` (2.24.x) is also installed as a package from `IUS YUM repo <https://ius.io/>`_ on the host. 

.. _software-terminal-multiplex:

Terminal Multiplexers
---------------------

We install both ``screen`` and ``tmux`` for attaching and managing several pseudoterminal-based sessions.
Here are some tutorials for each:

 - `How to use screen <https://linuxize.com/post/how-to-use-linux-screen/>`_
 - `Getting started with tmux <https://linuxize.com/post/getting-started-with-tmux/>`_

.. _software-compilers:

Compilers, Debuggers, & Build Tools
-----------------------------------

In addition to developer tools provided by the :ref:`software-stack`, the following tools are installed as system level packages:

- **Compilers**: ``c``, ``c++``, and ``fortran`` from gcc 4.8.5
- **Debuggers**: ``glibc-debuginfo`` (i.e. ``gdb``)
- **Build Tools**: ``autoconf``, ``automake``, ``bison``, ``blas``, ``byacc``, ``cmake``, ``flex``, ``fontconfig``, ``make``, ``valgrind``, ``yum-utils``, etc.

.. _software-devtoolset:

Using SCL devtoolsets
---------------------

.. note::

   Although the material presented below remains valid, the shared stack from May 2020 onwards (:file:`/software/lsstsw/stack_20200504`) provides the complete toolchain required for Science Pipelines development.
   It is no longer necessary to load a software collection to work with the shared stack.

The LDF server nodes are configured with the latest CentOS 7.x as its operating system.
This release of CentOS provides an old set of development tools, centered around version 4.8.5 of the `GNU Compiler Collection`_ (GCC).
Updated toolchains are made available through the “Software Collection” system.
The following Software Collections are currently available:

================ ===========
Name             Description
================ ===========
``devtoolset-8`` Updated compiler toolchain providing GCC 8.3.1.
================ ===========

To enable a particular Software Collection use the ``scl`` command. For example:

.. prompt:: bash $ auto

   $ scl enable devtoolset-8 bash
   $ gcc --version
   gcc (GCC) 8.3.1 20190311 (Red Hat 8.3.1-3)
   Copyright (C) 2018 Free Software Foundation, Inc.
   This is free software; see the source for copying conditions.  There is NO
   warranty; not even for MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.

.. warning::

   Code compiled by different versions of GCC may not be compatible: it is generally better to stick to a particular toolchain for a given project.
   In particular, if you are using a :ref:`shared stack <software-stack-shared>` you *must* use the matching toolchain.

You may wish to automatically enable a particular software collection every time you log in to systems at NCSA.
Take care if you do this: it's easy to accidentally to either start recursively spawning shells and run out of resources or lock yourself out of machines which don't have the particular collection you're interested in installed.
If you are using `Bash`_ — the default shell on ``lsst-dev`` servers — try placing the following at the end of :file:`~/.bash_profile` and customising the list of ``desired_scls``.

.. code-block:: bash

   # User-specified space-delimited list of SCLs to enable.
   desired_scls="devtoolset-8"

   # Only do anything if /usr/bin/scl is executable.
   if [ -x /usr/bin/scl ]; then

       # Select the union of the user's desired SCLs with those which are both
       # available and not currently enabled.
       avail_scls=$(scl --list)
       for scl in $desired_scls; do
           if [[ $avail_scls =~ $scl && ! $X_SCLS =~ $scl ]]; then
               scls[${#scls[@]}]=$scl
           fi
       done

       # Use `tty -s` to output messages only if connected to a terminal;
       # avoids causing problems for non-interactive sessions.
       if [ ${#scls[@]} != 0 ]; then
           tty -s && echo "Enabling ${scls[@]}."
           exec scl enable ${scls[@]} bash
       else
           tty -s && echo "No software collections to enable."
       fi
   fi

.. _GNU Compiler Collection: https://gcc.gnu.org/
.. _prerequisites for building the LSST stack: https://confluence.lsstcorp.org/display/LSWUG/OSes+and+Prerequisites
.. _Red Hat Developer Toolset: http://developers.redhat.com/products/developertoolset/overview/
.. _Git: https://www.git-scm.com/
.. _Bash: https://www.gnu.org/software/bash/

.. _software-x11-xpra:

Configure Remote Display with :command:`xpra`
---------------------------------------------

:command:`xpra` can be thought of as "screen for X" and offers advantages over VNC.
It can be very handy and efficient for remote display to your machine from Rubin Observatory development compute nodes (e.g., debugging with :command:`ds9`) because it is much faster than a regular X connection when you don't have a lot of bandwidth (e.g., working remotely), and it saves state between connections.
Here's how to use it:

On ``lsst-login01``:

.. prompt:: bash

   xpra start :10
   export DISPLAY=:10

You may have to choose a different display number (>10) if ``:10`` is already in use.

On your local machine, do:

.. prompt:: bash

   xpra attach ssh:lsst-login01.ncsa.illinois.edu:10

   ## IF YOU EXPERIENCE AUTHENTICATION ISSUES, TRY THE FOLLOWING INSTEAD TO SPECIFY AUTH METHODS OF SSH
   xpra attach --ssh="ssh -vvv -o='PreferredAuthentications=gssapi-with-mic,keyboard-interactive,password'" ssh:lsst-login01.ncsa.illinois.edu:10

You may leave that running, or put it in the background and later use:

.. prompt:: bash

   xpra detach

Then you can open windows on ``lsst-login01`` (with ``DISPLAY=:10``) and they will appear on your machine.
If you now kill the :command:`xpra attach` on your machine, you'll lose those windows.
When you reattach, they'll reappear.

.. note::

   :command:`xpra` requires the use of Python 2.

   If you are using a Python 3 LSST Stack, you'll encounter a error like the following:

   .. code-block:: bash

      [...]
      File "/ssd/lsstsw/stack3_20171021/stack/miniconda3-4.3.21-10a4fa6/Linux64/pyyaml/3.11.lsst2/lib/python/yaml/__init__.py", line 284
        class YAMLObject(metaclass=YAMLObjectMetaclass):
                                  ^
      SyntaxError: invalid syntax

   The solution in this case is to start ``xpra`` in a separate shell where you haven't yet ``setup`` the Python 3 LSST Stack.

.. note::

   If you run into issues getting :command:`xpra` to authenticate when you attempt to attach, you may find that including explicit authentication options helps:

   .. code-block:: bash

      xpra attach -ssh="ssh -o='PreferredAuthentications=gssapi-with-mic,keyboard-interactive,password'" ssh:lsst-login01.ncsa.illinois.edu:100

.. note::

   It is possible to use xpra through a tunneled connection to an "interior" node that also has xpra, e.g., when using a login nodes as a "jump host" to reach a submit node, as described above, you may wish to use xpra on the submit node.

   First, make your tunneled connection to the destination host (as detailed above).

   Then attach xpra to the submit host by also telling xpra to jump/tunnel through the login node:

   .. code-block:: bash

      xpra attach ssh:lsst-devl01.ncsa.illinois.edu:10 --ssh="ssh -J lsst-login01.ncsa.illinois.edu"


.. _software-misc:

Miscellaneous Packages
----------------------

A few other developer resources are also installed directly as system level packages:

- ImageMagick
- Midnight Commander
- PostgreSQL client
- The Silver Searcher
- sqlite3


.. _software-stack:

LSST Software Stack
===================

Refer to :doc:`/stack/index` for more details on using the LSST Software Stack.

.. _software-stack-shared:

Shared Software Stack
---------------------

A shared software stack on the GPFS file systems has been provided and is maintained by Science Pipelines and is available under :file:`/software/lsstsw`.

We provide a ready-to-use “shared” version of the LSST software stack to enable developers to get up and running quickly with no installation step.
The shared stack includes a fully-fledged Miniconda-based Python environment, a selection of additional development tools, and a selection of builds of the lsst_distrib meta-package.
It is located on GPFS-based network storage; as such, it is cross-mounted across a variety of Rubin Observatory development systems at the Data Facility including those configured as part of the `HTCondor pool`_ and :doc:`Verification Cluster <verification>`.
The currently stack is regularly updated to include the latest weekly release, which is tagged as ``current``.

The following stacks are currently being updated:

======================================= ================ ===========
Path                                    Toolchain        Description
======================================= ================ ===========
:file:`/software/lsstsw/stack_20200515` Internal (Conda) Provides weekly ``w_2020_19`` and later of lsst_distrib and ``w_2020_20`` and later of lsst_sims.
                                                         Based on `scipipe_conda_env`_ ``46b24e8`` with the following additional packages installed:

                                                         - bokeh
                                                         - cx_Oracle
                                                         - dask-jobqueue
                                                         - datashaderpyct
                                                         - fastparquet
                                                         - holoviews
                                                         - hvplot
                                                         - ipdb
                                                         - jupyter
                                                         - numba
                                                         - panel
                                                         - pep8
                                                         - psycopg2
                                                         - pyflakes
                                                         - pyviz_comms
======================================= ================ ===========

.. _scipipe_conda_env: https://github.com/lsst/scipipe_conda_env

.. note::

   When using a shared stack, you *must* use the corresponding developer toolchain.
   If this is listed in the table above as “Internal (Conda)” then no further action on your part is required; otherwise, see above for details of how to :ref:`software-devtoolset`.

In addition, the following symbolic links point to particular versions of the stack:

=============================== ================================
Path                            Description
=============================== ================================
:file:`/software/lsstsw/stack`  The latest version of the stack.
=============================== ================================

Add a shared stack to your environment and set up the latest build of the LSST applications by running, for example:

.. prompt:: bash

  source /software/lsstsw/stack/loadLSST.bash
  setup lsst_apps

(substitute :file:`loadLSST.csh`, :file:`loadLSST.ksh` or :file:`loadLSST.zsh`, depending on your preferred shell).

.. tip::

   Initializing the stack will prepend the string ``(lsst-scipipe)`` to your prompt.
   If you wish, you can disable this by running

   .. prompt:: bash

      conda config --set changeps1 false

Although the latest weeklies of LSST software are regularly installed into the shared stacks, the rest of their contents is held fixed (to avoid API or ABI incompatibilities with old stack builds).
We therefore periodically retire old stacks and replace them with new ones.
The following retired stacks are currently available:

======================================= ================ ===========
Path                                    Toolchain        Description
======================================= ================ ===========
:file:`/software/lsstsw/stack_20171023` ``devtoolset-6`` Provides a selection of weekly and release builds dating between October 2017 and October 2018.
:file:`/software/lsstsw/stack_20181012` ``devtoolset-6`` Provides weeklies ``w_2018_41`` through ``w_2019_12``; release candidates ``v17_0_rc1``, ``v17_0_rc2``, and ``v17_0_1_rc1``; and releases ``v_17_0`` and ``v_17_0_1``. Based on the pre-:jira:`RFC-584` Conda environment.
:file:`/software/lsstsw/stack_20190330` ``devtoolset-6`` Provides weekly ``w_2019_12`` through ``w_2019_38`` and daily ``d_2019_09_30``. Based on the post-:jira:`RFC-584` Conda environment.
:file:`/software/lsstsw/stack_20191001` ``devtoolset-8`` Provides weeklies ``w_2019_38`` through ``w_2019_42``.
:file:`/software/lsstsw/stack_20191101` ``devtoolset-8`` Provides weekly ``w_2019_43`` through ``w_2020_09`` of lsst_distrib, and ``w_2019_43`` through ``w_2020_07`` of lsst_sims.
                                                         Based on `scipipe_conda_env`_ ``4d7b902`` (:jira:`RFC-641`).
:file:`/software/lsstsw/stack_20200220` ``devtoolset-8`` Provides weekly ``w_2020_07`` through ``w_2020_17`` of lsst_distrib, and weekly ``w_2020_10`` through ``w_2020_16`` of lsst_sims.
                                                         Based on `scipipe_conda_env`_ ``984c9f7`` (:jira:`RFC-664`).
:file:`/software/lsstsw/stack_20200504` Internal (Conda) Provides weeklies ``w_2020_18`` and ``w_2020_19`` of lsst_distrib.
                                                         Based on `scipipe_conda_env`_ ``2deae7a`` (:jira:`RFC-679`).
======================================= ================ ===========

Administrators may wish to note that the shared stack is automatically updated using the script :file:`~lsstsw/shared-stack/shared_stack.py`, which is executed nightly by Cron.

.. _HTCondor pool: https://confluence.lsstcorp.org/display/DM/Orchestration


.. _software-stack-setup:

LSST Stack Setup
----------------

Refer to :doc:`/stack/eups-tutorial` and :doc:`/stack/lsstsw` for more details on setting up the LSST Stack and customizing it.

.. _software-stack-python:

LSST Stack Python
-----------------

Refer to :doc:`/python/index` for more details on using Python from the LSST Stack.


.. _software-data:

Accessing Data
==============

.. _software-data-gpfs:

GPFS Directory Spaces
---------------------

Most LDF nodes utilize the General Parallel File System (GPFS) to provide shared storage across all of the nodes.

For convenience the bind mounts  :file:`/home` , :file:`/scratch` , :file:`/project` , :file:`/datasets` ,  and :file:`/software`  have been created to provide views into corresponding spaces in GPFS.

Refer to :doc:`Storage Resources <storage>` for more general information.

To add/change/delete datasets, see :doc:`Common Dataset Organization and Policy </services/datasets>`.

.. _software-data-sets:

Validation/Test Data Sets
-------------------------

There are two ``cron`` jobs that will update a set of validation data repositories and test data repositories.
These updates will trigger overnight on the ``lsst-dev`` system.
In most cases, this will be a fairly straightforward ``git pull``, but if corruption is detected, the repository will be cloned afresh.
The verification data are currently being used primarily by ``validate_drp`` to measure various metrics on the reduced data.
The test data serve a variety of purposes, but generally are included via a ``setupOptional`` in a package table file.

Test data location is: ``/project/shared/data/test_data``

Included test data repositories are::

  testdata_jointcal
  testdata_cfht
  testdata_subaru
  testdata_decam
  testdata_lsst
  ap_verify_testdata
  ap_pipe_testdata
  ci_hsc
  afwdata

Validation data location is: ``/project/shared/data/validation_data``

Included validation data repositories are::

  validation_data_hsc
  validation_data_decam
  validation_data_cfht

These are maintained by the ``lsstsw`` user (this is the same user that curates the shared stack on the ``lsst-dev`` system).
Please ask in the ``#dm-infrastructure`` Slack channel in case of problems.


.. _software-processing:

Processing Data
===============

Users are encouraged to submit batch jobs to perform work that requires more significant resources. Refer to :doc:`batch` for more information.

.. _software-processing-interactive:

Interactive Batch Jobs
----------------------

Refer to :ref:`batch-htcondor-interactive-job` for details on how to submit simple, interactive batch jobs.

.. _software-processing-batch:

Submit Batch Jobs
-----------------

Refer to :doc:`batch` for details on how to submit batch jobs.


.. _software-cron:

CRON Jobs
=========

CRON jobs are disabled by default for normal users. If a CRON job is necessary, please submit an :doc:`IHS ticket <ldf-tickets>`.

