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
#. :ref:`lsst-login-connect`
#. :ref:`lsst-login-development`
#. :ref:`lsst-login-tools`
#. :ref:`lsst-login-loadlsst`
#. :ref:`lsst-login-testdata`
#. :ref:`lsst-login-gitlfs`
#. :ref:`lsst-login-xpra`

.. _lsst-login-overview:

Overview
========

The ``lsst-login`` servers are primarily intended as bastions used to access other resources at NCSA. Additional capabilities include:

- light :ref:`lsst-login-development` with short-running processes that require modest resources (e.g., build docs, short compilations against LSST software stack)
- view files (e.g., FITS files)

Users are encouraged to submit batch jobs to perform work that requires more significant resources. Please see :doc:`/services/batch` for more information.

The ``lsst-login`` nodes have access to the :doc:`LDF file systems <storage>`.

For system status and issues:

- `Service status <https://confluence.lsstcorp.org/display/DM/LSST+Service+Status+page>`_ including announcements of upcoming planned down-time.
- `Real-time system status <https://monitor-ncsa.lsst.org/>`_ (requires login).
- To report system issues, log into `LSST JIRA <https://jira.lsstcorp.org/>`_ and file a `JIRA ticket in the IT Helpdesk Support <https://ls.st/ihsticket>`_ project tagging NCSA as the responsible organization.

.. _lsst-login-connect:

Connecting and Authenticating
=============================

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

The Kerberos domain for the ``lsst-login`` servers is ``NCSA.EDU``, so something like this may work to generate a Kerberos ticket on your local machine:

.. prompt:: bash $ auto

  kinit username@NCSA.EDU

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

.. _lsst-login-development:

Development Work
================

``lsst-login`` nodes can be used for (light) development work. Users are encouraged to utilize batch compute nodes when more significant resources are required. Please see :doc:`/services/batch` for more information.

.. _lsst-login-tools:

Select Appropriate Developer Tools
==================================

.. note::

   Although the material presented below remains valid, the shared stack from May 2020 onwards (:file:`/software/lsstsw/stack_20200504`) provides the complete toolchain required for Science Pipelines development.
   It is no longer necessary to load a software collection to work with the shared stack.

The ``lsst-login`` systems are configured with the latest CentOS 7.x as its operating system.
This release of CentOS provides an old set of development tools, centered around version 4.8.5 of the `GNU Compiler Collection`_ (GCC).
Updated toolchains are made available through the “Software Collection” system.
The following Software Collections are currently available:

================ ===========
Name             Description
================ ===========
``devtoolset-6`` Updated compiler toolchain providing GCC 6.3.1.
``devtoolset-7`` Updated compiler toolchain providing GCC 7.3.1.
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
   In particular, if you are using a :ref:`shared stack <lsst-login-loadlsst>` you *must* use the matching toolchain.

You may wish to automatically enable a particular software collection every time you log in to ``lsst-login01`` and other LSST systems.
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

.. _lsst-login-loadlsst:

Load the LSST Environment
=========================

We provide a ready-to-use “shared” version of the LSST software stack to enable developers to get up and running quickly with no installation step.
The shared stack includes a fully-fledged Miniconda-based Python environment, a selection of additional development tools, and a selection of builds of the lsst_distrib meta-package.
It is located on GPFS-based network storage; as such, it is cross-mounted across a variety of LSST systems at the Data Facility including those configured as part of the `HTCondor pool`_ and :doc:`Verification Cluster <verification>`.
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
   If this is listed in the table above as “Internal (Conda)” then no further action on your part is required; otherwise, see above for details of how to :ref:`lsst-login-tools`.

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

.. _lsst-login-testdata:

Validation/Test Data Sets
=========================

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

.. _lsst-login-gitlfs:

Configure Git LFS
=================

.. note::

   Although the material presented below remains valid, the shared stack from May 2020 onwards (:file:`/software/lsstsw/stack_20200504`) provides Git LFS as part of the environment: it is no longer necessary to explicitly run :command:`setup`, as described below (although it is still necessary to follow DM's :doc:`Git LFS guide </git/git-lfs>`.
   The :command:`setup` step is only necessary for older shared stacks — those marked with ``toolchain: devtoolset-8`` (or ``-6``) in the table above.    **For newer shared stacks (``toolchain: Internal (Conda)``), they are not relevant.**

After you have initialized a shared stack, you can enable Git LFS using EUPS:

.. code-block:: bash

   setup git_lfs

The first time you use Git LFS you'll need to configure it by following these steps from DM's :doc:`Git LFS guide </git/git-lfs>`:

1. :ref:`git-lfs-basic-config`
2. :ref:`git-lfs-config`

.. _lsst-login-xpra:

Configure Remote Display with :command:`xpra`
=============================================

:command:`xpra` can be thought of as "screen for X" and offers advantages over VNC.
It can be very handy and efficient for remote display to your machine from the LSST cluster (e.g., debugging with :command:`ds9`) because it is much faster than a regular X connection when you don't have a lot of bandwidth (e.g., working remotely), and it saves state between connections.
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

      xpra attach ssh:lsst-condorprod-sub01.ncsa.illinois.edu:10 --ssh="ssh -J lsst-login01.ncsa.illinois.edu"
