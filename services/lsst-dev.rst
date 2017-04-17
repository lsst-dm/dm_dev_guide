#########################
Using the lsst-dev Server
#########################

``lsst-dev`` is the development server/cluster of servers run by NCSA for LSST DM development work.
The cname ``lsst-dev.ncsa.illinois.edu`` directs to ``lsst-dev01.ncsa.illinois.edu`` and this system serves as the primary development server for the team.

To get an account, see the :doc:`Onboarding Checklist </getting-started/onboarding>`.

This page is designed to assist developers in their work on ``lsst-dev01``:

#. :ref:`lsst-dev-overview`
#. :ref:`lsst-dev-password`
#. :ref:`lsst-dev-ssh-keys`
#. :ref:`lsst-dev-tools`
#. :ref:`lsst-dev-loadlsst`
#. :ref:`lsst-dev-xpra`

.. _lsst-dev-overview:

Overview of Cluster Resources
=============================

- List of `available development servers <https://confluence.lsstcorp.org/display/LDMDG/DM+Development+Servers>`_ and their intended use.
- `System announcements <https://confluence.lsstcorp.org/display/LDMDG/DM+System+Announcements>`_ of the status and planned down-time.
- `Real-time system status <http://lsst-web.ncsa.illinois.edu/nagios>`_ (requires login).
- Reference/test data from SDSS DR7 for Stripe82 is located at: :file:`/lsst7/stripe82/dr7/runs`.
- Report system issues to ``lsst-sysadm _at_ ncsa.illinois.edu``.

.. _lsst-dev-password:

Account Password
================

You can log into LSST development servers at NCSA with your NCSA account and password. You can reset your NCSA password at the following URL:

   - https://identity.ncsa.illinois.edu/reset

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

The ``lsst-dev01`` system is configured with the latest CentOS 7.x as its operating system.
This release of CentOS provides an old set of development tools, centered around version 4.8.5 of the `GNU Compiler Collection`_ (GCC).
While this version of GCC does satisfy the `prerequisites for building the LSST stack`_, it is still rather out of date.
However, this version of GCC is used for building the :ref:`shared stacks <lsst-dev-loadlsst>` available on the machine and must be used if building against those stacks.
It is also used by the ``lsstsw`` account that builds releases.

If you prefer, you can enable the `Red Hat Developer Toolset`_ version 3 (``devtoolset-3``) which has been pre-installed.
This provides an updated toolchain, including GCC 4.9.2.
If you enable this, you must not use the shared stack; instead you must build your own version of the entire stack using this toolchain.

Enable and test ``devtoolset-3`` using the ``scl`` command as follows (replacing ``bash`` with your shell of choice if necessary):

.. prompt:: bash $ auto

   $ scl enable devtoolset-3 bash
   $ gcc --version
   gcc (GCC) 4.9.2 20150212 (Red Hat 4.9.2-6)
   Copyright (C) 2014 Free Software Foundation, Inc.
   This is free software; see the source for copying conditions.  There is NO
   warranty; not even for MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.

The Developer Toolset includes version 1.9.3 of the `Git`_ version control system.
If you prefer the (slightly) more recent version 1.9.4, you may also wish to enable the ``git19`` package.
This may be done at the same time as enabling ``devtoolset-3``.

.. prompt:: bash

   scl enable devtoolset-3 git19 bash

You may wish to automatically enable ``devtoolset-3`` every time you log in to ``lsst-dev01`` by adding it to your shell initialization files.
For example, try adding the following to :file:`~/.profile`:

.. code-block:: bash

   exec scl enable devtoolset-3 bash

.. _GNU Compiler Collection: https://gcc.gnu.org/
.. _prerequisites for building the LSST stack: https://confluence.lsstcorp.org/display/LSWUG/OSes+and+Prerequisites
.. _Red Hat Developer Toolset: http://developers.redhat.com/products/developertoolset/overview/
.. _Git: https://www.git-scm.com/

.. _lsst-dev-loadlsst:

Load the LSST Environment
=========================

Two ‘shared’ installations of the LSST software stack are available on ``lsst-dev01``:

:file:`/ssd/lsstsw/stack/`
   This is installed on local (SSD) storage.
   It provides for maximum performance when executing jobs on ``lsst-dev01`` directly.

:file:`/software/lsstsw/stack/`
   This is installed on networked storage (GPFS).
   As such, it may be slightly slower than local storage when running on ``lsst-dev01``.
   However, the ``/software`` GPFS disk is cross-mounted to `other development servers at NCSA`_, including those configured as part of the `HTCondor pool`_ and :doc:`Verification Cluster <verification>`.
   This stack can therefore be relied upon to be consistent when launching jobs across the cluster.

.. _other development servers at NCSA: https://confluence.lsstcorp.org/display/LDMDG/DM+Development+Servers
.. _HTCondor pool: https://confluence.lsstcorp.org/display/DM/Orchestration

This installation is regularly updated to recent releases and weekly builds of the ``lsst_distrib`` top-level package; the most recent build is tagged as ``current``.
Add this shared stack to your environment and set up the latest build of the LSST applications by running:

.. prompt:: bash

  source /ssd/lsstsw/stack/loadLSST.bash
  setup lsst_apps

(substitute :file:`loadLSST.csh`, :file:`loadLSST.ksh` or :file:`loadLSST.zsh`, depending on your preferred shell, and use :file:`/software/lsstsw/stack/loadLSST.bash` to access the GPFS-backed stack).

Since this stack is shared, all members of the ``lsst`` group have permission to declare products within it, thereby making new products and versions available for other users.
For example, to share ``myVersion`` of ``myProduct``, which you have built and installed in directory ``productDir``, run:

.. prompt:: bash

   eups declare myProduct myVersion -r productDir

To declare a product for your own use without making it available for others to ``setup``, tag it with your username:

.. prompt:: bash

   eups declare myProduct myVersion -t $(whoami) -r productDir

Please make use of this capability responsibly: make public declarations only of those products which are of general use, and remove them when they become obsolete:

.. prompt:: bash

   eups undeclare myProduct myVersion

Refer to the :doc:`/build-ci/eups_tutorial` for more information on working with EUPS product stacks.

Note that the SSD and GPFS-backed stacks are independent: while both will automatically contain the latest LSST software releases, other products declared in a given stack will not automatically become available in the other.

Administrators may wish to note that the shared stack is automatically updated using the script :file:`~lsstsw/shared-stack/shared_stack.py`, which is executed nightly by Cron.

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
