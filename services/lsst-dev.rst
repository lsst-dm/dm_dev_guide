#########################
Using the lsst-dev Server
#########################

``lsst-dev`` is the development cluster of servers run by NCSA for LSST DM development work.
The cname ``lsst-dev.ncsa.illinois.edu`` directs to ``lsst-dev01.ncsa.illinois.edu`` and this system serves as the primary development server for the team. There are currently 3 identical development servers to choose from:

- ``lsst-dev01.ncsa.illinois.edu``
- ``lsst-dev02.ncsa.illinois.edu``
- ``lsst-dev03.ncsa.illinois.edu``

To get an account, see the :doc:`Onboarding Checklist </team/onboarding>`.

This page is designed to assist developers in their work on the ``lsst-dev`` servers:

#. :ref:`lsst-dev-overview`
#. :ref:`lsst-dev-password`
#. :ref:`lsst-dev-ssh-keys`
#. :ref:`lsst-dev-tools`
#. :ref:`lsst-dev-loadlsst`
#. :ref:`lsst-dev-testdata`
#. :ref:`lsst-dev-gitlfs`
#. :ref:`lsst-dev-xpra`

.. _lsst-dev-overview:

Overview of Cluster Resources
=============================

- List of `available development servers <https://confluence.lsstcorp.org/display/LDMDG/DM+Development+Servers>`_ and their intended use.
- `Service status <https://confluence.lsstcorp.org/display/DM/LSST+Service+Status+page>`_ including announcements of upcoming planned down-time.
- `Real-time system status <https://monitor-ncsa.lsst.org/>`_ (requires login).
- All of the ``lsst-dev`` systems have access to the :ref:`verification-gpfs`, including:

  - Reference/test data from SDSS DR7 for Stripe82, which is located at :file:`/datasets/sdss/preprocessed/dr7`.
  - Several other datasets available in :file:`/datasets`.  See README files in each dataset.

- To report system issues, `file a JIRA ticket <https://jira.lsstcorp.org/secure/CreateIssueDetails!init.jspa?pid=12200&issuetype=10901&priority=10000&customfield_12211=12223&components=14213>`_ in the IT Helpdesk Support (IHS) project.

.. _lsst-dev-password:

Account Password
================

You can log into LSST development servers at NCSA with your NCSA account and password. You can reset your NCSA password at the following URL:

   - https://identity.lsst.org/reset

.. _lsst-dev-ssh-keys:

Set up SSH Keys
===============

You can establish public/private keys to access NCSA development machines via SSH.
Here's how to set up your SSH client to use keys:

1. Generate a key pair
----------------------

If you haven't already, generate your key pair on your local machine (you should always use a strong password for your passphrase). On most machines, you can use OpenSSH:

.. prompt:: bash

   mkdir ~/.ssh
   chmod 700 ~/.ssh
   ssh-keygen -t rsa

Enter your passphrase at the prompts:

.. prompt:: bash $ auto

   Generating public/private rsa key pair.
   Enter file in which to save the key (/home/username/.ssh/id_rsa):
   Enter passphrase (empty for no passphrase):
   Enter same passphrase again:
   Your identification has been saved in /home/username/.ssh/id_rsa.
   Your public key has been saved in /home/username/.ssh/id_rsa.pub.
   The key fingerprint is:
   a1:b2:c3:45:67:89:d1:e2:f3:54:76:98:00:aa:bb:01 username@hostname.lsstcorp.org

.. note::

   If you used a program other than OpenSSH for this step, make sure your public key is formatted as a single line (most SSH clients provide it as an option). Otherwise, the next step will not work.

2. Install the public key on lsst-dev01
---------------------------------------

Install the public key on the remote server, :file:`~/.ssh/id_rsa.pub`, to ``lsst-dev01.ncsa.illinois.edu``:

.. prompt:: bash

   scp .ssh/id_rsa.pub lsst-dev01.ncsa.illinois.edu:mymachine_rsa.pub
   ssh lsst-dev01.ncsa.illinois.edu

On ``lsst-dev01.ncsa.illinois.edu``:

.. prompt:: bash

   touch ~/.ssh/authorized_keys
   chmod 600 ~/.ssh/authorized_keys
   cat mydevmachine_rsa.pub >> ~/.ssh/authorized_keys
   exit

3. Login
--------

Login without a password to ``lsst-dev01``:

.. prompt:: bash $ auto

   $ ssh lsst-dev01.ncsa.illinois.edu
   Enter passphrase for key '/home/username/.ssh/id_rsa': # type your key passphrase

For more information on using SSH public/private keys:

- `SSH Keygen Wikipedia Article <http://en.wikipedia.org/wiki/Ssh-keygen>`_
- `OpenSSH Public and Private Keys (from Ubuntu) <https://help.ubuntu.com/community/SSH/OpenSSH/Keys>`_
- `Using SSH Public Key Authentication <http://macnugget.org/projects/publickeys/>`_
- `SSH Public Key Based Authentication Howto <http://www.cyberciti.biz/tips/ssh-public-key-based-authentication-how-to.html>`_

.. _lsst-dev-tools:

Select Appropriate Developer Tools
==================================

The ``lsst-dev`` systems are configured with the latest CentOS 7.x as its operating system.
This release of CentOS provides an old set of development tools, centered around version 4.8.5 of the `GNU Compiler Collection`_ (GCC).
Updated toolchains are made available through the “Software Collection” system.
The following Software Collections are currently available:

================ ================================================
Name             Description
================ ================================================
``devtoolset-3`` Updated compiler toolchain providing GCC 4.9.2.
``devtoolset-4`` Updated compiler toolchain providing GCC 5.3.1.
``devtoolset-6`` Updated compiler toolchain providing GCC 6.3.1.
``devtoolset-7`` Updated compiler toolchain providing GCC 7.1.1.
``devtoolset-8`` Updated compiler toolchain providing GCC 8.3.1.
``git19``        The `Git`_ version control system version 1.9.4.
``rh-git29``     The `Git`_ version control system version 2.9.3.
================ ================================================

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
   In particular, if you are using a :ref:`shared stack <lsst-dev-loadlsst>` you *must* use the matching toolchain.

You may wish to automatically enable a particular software collection every time you log in to ``lsst-dev01`` and other LSST systems.
Take care if you do this: it's easy to accidentally to either start recursively spawning shells and run out of resources or lock yourself out of machines which don't have the particular collection you're interested in installed.
If you are using `Bash`_ — the default shell on ``lsst-dev`` servers — try placing the following at the end of :file:`~/.bash_profile` and customising the list of ``desired_scls``.

.. code-block:: bash

   # User-specified space-delimited list of SCLs to enable.
   desired_scls="rh-git29 devtoolset-8"

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

.. _lsst-dev-loadlsst:

Load the LSST Environment
=========================

We provide a ready-to-use “shared” version of the LSST software stack to enable developers to get up and running quickly with no installation step.
The shared stack includes a fully-fledged Miniconda-based Python environment, a selection of additional development tools, and a selection of builds of the lsst_distrib meta-package.
It is located on GPFS-based network storage; as such, it is cross-mounted across a variety of LSST systems at the Data Facility including those configured as part of the `HTCondor pool`_ and :doc:`Verification Cluster <verification>`.
The currently stack is regularly updated to include the latest weekly release, which is tagged as ``current``.

The following stacks are currently being updated:

======================================= ================ =============================================================================================
Path                                    Toolchain        Description
======================================= ================ =============================================================================================
:file:`/software/lsstsw/stack_20190330` ``devtoolset-6`` Provides weekly ``w_2019_12`` and later. Based on the post-:jira:`RFC-584` Conda environment.
======================================= ================ =============================================================================================

The following stacks are not currently being updated, but remain available.

.. note::

   When using a shared stack, you *must* use the corresponding developer toolchain. See above for details on how to :ref:`lsst-dev-tools`.

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

======================================= ================ ==========================================================================================================================================================================================================================
Path                                    Toolchain        Description
======================================= ================ ==========================================================================================================================================================================================================================
:file:`/software/lsstsw/stack_20171023` ``devtoolset-6`` Provides a selection of weekly and release builds dating between October 2017 and October 2018.
:file:`/software/lsstsw/stack_20181012` ``devtoolset-6`` Provides weeklies ``w_2018_41`` through ``w_2019_12``; release candidates ``v17_0_rc1``, ``v17_0_rc2``, and ``v17_0_1_rc1``; and releases ``v_17_0`` and ``v_17_0_1``. Based on the pre-:jira:`RFC-584` Conda environment.
======================================= ================ ==========================================================================================================================================================================================================================

Administrators may wish to note that the shared stack is automatically updated using the script :file:`~lsstsw/shared-stack/shared_stack.py`, which is executed nightly by Cron.

.. _HTCondor pool: https://confluence.lsstcorp.org/display/DM/Orchestration

.. _lsst-dev-testdata:

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

.. _lsst-dev-gitlfs:

Configure Git LFS
=================

After you have initialized a shared stack, you can enable Git LFS using EUPS:

.. code-block:: bash

   setup git_lfs

The first time you use Git LFS you'll need to configure it by following these steps from DM's :doc:`Git LFS guide </git/git-lfs>`:

1. :ref:`git-lfs-basic-config`
2. :ref:`git-lfs-config`

.. _lsst-dev-xpra:

Configure Remote Display with :command:`xpra`
=============================================

:command:`xpra` can be thought of as "screen for X" and offers advantages over VNC.
It can be very handy and efficient for remote display to your machine from the LSST cluster (e.g., debugging with :command:`ds9`) because it is much faster than a regular X connection when you don't have a lot of bandwidth (e.g., working remotely), and it saves state between connections.
Here's how to use it:

On ``lsst-dev01``:

.. prompt:: bash

   xpra start :10
   export DISPLAY=:10

You may have to choose a different display number (>10) if ``:10`` is already in use.

On your local machine, do:

.. prompt:: bash

   xpra attach ssh:lsst-dev01.ncsa.illinois.edu:10

You may leave that running, or put it in the background and later use:

.. prompt:: bash

   xpra detach

Then you can open windows on ``lsst-dev01`` (with ``DISPLAY=:10``) and they will appear on your machine.
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
