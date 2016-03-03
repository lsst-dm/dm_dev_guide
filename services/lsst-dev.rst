#########################
Using the lsst-dev Server
#########################

``lsst-dev`` is a cluster of servers run by NCSA for LSST DM development work.
To get an account, see the :doc:`Onboarding Checklist </getting-started/onboarding>`.

This page help you get started on lsst-dev:

1. :ref:`Setting up SSH Keys <lsst-dev-ssh-keys>`
2. :ref:`Load the LSST Environment <lsst-dev-loadlsst>`
3. Setting up developer tools; we recommend the :ref:`alternate toolset <lsst-dev-alt-tools>`
4. :ref:`Configuring xpra <lsst-dev-xpra>`

Overview of Cluster Resources
=============================

- List of `available development servers <https://confluence.lsstcorp.org/display/LDMDG/DM+Development+Servers>`_ and their intended use.
- `System announcements <https://confluence.lsstcorp.org/display/LDMDG/DM+System+Announcements>`_ of the status and planned down-time.
- `Real-time system status <http://lsst-web.ncsa.illinois.edu/nagios>`_ (requires login).
- Reference/test data from SDSS DR7 for Stripe82 is located at: :file:`/lsst7/stripe82/dr7/runs`.
- Report system issues to ``lsst-admin _at_ ncsa.illinois.edu``

.. _lsst-dev-ssh-keys:

Setting up SSH Keys
===================

You will need to establish public/private keys to access NCSA development machines via SSH.
Here's how to set up your SSH client to use keys:

1. Generate a key pair
----------------------

If  you haven't already, generate your key pair on your local machine (you should always use a strong password for your passphrase): 

.. code-block:: bash

   mkdir ~/.ssh
   chmod 700 ~/.ssh
   ssh-keygen -t rsa

Enter your passphrase at the prompts:

.. code-block:: bash

   Generating public/private rsa key pair.
   Enter file in which to save the key (/home/username/.ssh/id_rsa):
   Enter passphrase (empty for no passphrase):
   Enter same passphrase again:
   Your identification has been saved in /home/username/.ssh/id_rsa.
   Your public key has been saved in /home/username/.ssh/id_rsa.pub.
   The key fingerprint is:
   a1:b2:c3:45:67:89:d1:e2:f3:54:76:98:00:aa:bb:01 username@hostname.lsstcorp.org

2. Install the public key on lsst-dev
-------------------------------------

Install the public key on the remote server, :file:`~/.ssh/id_rsa.pub`, to ``lsst-dev.ncsa.illinois.edu``:

.. code-block:: bash

   % scp .ssh/id_rsa.pub lsst-dev.ncsa.illinois.edu:mymachine_rsa.pub
   % ssh lsst-dev.ncsa.illinois.edu

On ``lsst-dev.ncsa.illinois.edu``:

.. code-block:: bash

   % touch ~/.ssh/authorized_keys
   % chmod 600 ~/.ssh/authorized_keys
   % cat mydevmachine_rsa.pub >> ~/.ssh/authorized_keys
   % exit

3. Login
--------

Login without a password to ``lsst-dev``:

.. code-block:: bash

   % ssh lsst-dev.ncsa.illinois.edu
   Enter passphrase for key '/home/username/.ssh/id_rsa':    # type your key passphrase

For more information on using SSH public/private keys:

- `SSH Keygen Wikipedia Article <http://en.wikipedia.org/wiki/Ssh-keygen>`_
- `OpenSSH Public and Private Keys (from Ubuntu) <https://help.ubuntu.com/community/SSH/OpenSSH/Keys>`_
- `Using SSH Public Key Authentication <http://macnugget.org/projects/publickeys/>`_
- `SSH Public Key Based Authentication Howto <http://www.cyberciti.biz/tips/ssh-public-key-based-authentication-how-to.html>`_

.. _lsst-dev-loadlsst:

Load the LSST Environment
=========================

Do the following to set up your shell for development on the LSST cluster (``lsst-dev``, etc.).
You can also following in the `~/.bashrc` file (this is the jist of the :file:`loadLSST.sh` script in the distribution):

.. code-block:: bash

   source ~lsstsw/eups/current/bin/setups.sh   # bash users
   setup anaconda
   setup git
   setup lsst
.. _lsst-dev-tools:

Developer Tools on lsst-dev
===========================

Two sets of developer tools are available on ``lsst-dev``.
DM developers should generally use :ref:`alternate <lsst-dev-alt-tools>` set to get have versions of GCC and Git that are capable of building the Stack and using Git LFS.

.. _lsst-dev-default-tools:

Default Development Tools
-------------------------

Currently the development servers hosted at NCSA are configured with CentOS 6.x as their operating system.

The following developer packages are installed on each of these servers in their default environment:

- gcc/g++/gfortran - GNU Compiler Collection - version 4.4.7
- gdb - GNU Debugger - version 7.2
- gcc-debuginfo
- glibc-debuginfo
- compat-glibc
- compat-gcc-34
- compat-gcc-34-c++
- compat-gcc-34-g77
- compat-libstdc++-296
- compat-libstdc++-33
- git - GIT - version 1.7.1
- valgrind - Tool for finding memory management bugs in programs - version 3.8.1
- python - version 2.6.6
- bison - GNU Bison - version 2.4.1
- byacc - version 1.9
- flex - flex 2.5.35

.. _lsst-dev-alt-tools:

Alternate Development Tools
---------------------------

Developer Toolset is an offering for developers on EL (Red Hat, CentOS, SCL) distributions.
Using a framework called Software Collections, an additional set of tools is installed into the /opt directory, as recommended by the UNIX Filesystem Hierarchy Standard.
These tools are enabled by the user on demand using the supplied scl utility.

Developer Toolset 3.x provides following tools:

- gcc/g++/gfortran - GNU Compiler Collection - version 4.9.2
- git - GIT - version 1.9.3
- gdb - GNU Debugger - version 7.8.2
- binutils - A GNU collection of binary utilities - version 2.24
- elfutils - A collection of utilities and DSOs to handle compiled objects - version 0.161
- dwz - DWARF optimization and duplicate removal tool - version 0.11
- systemtap - Programmable system-wide instrumentation system - version 2.6
- valgrind - Tool for finding memory management bugs in programs - version 3.10.1
- oprofile - System wide profiler - version 0.9.9

To test the alternate devtoolset environment:

.. code-block:: bash

   $ scl enable devtoolset-3 bash
   $ gcc --version
   gcc (GCC) 4.9.2 20150212 (Red Hat 4.9.2-6)
   Copyright (C) 2014 Free Software Foundation, Inc.
   This is free software; see the source for copying conditions.  There is NO
   warranty; not even for MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.

To make use of Git 1.9.x you can also use the Git 1.9 software collection.
You can enable multiple software collections at the same time, so the following will enable both the ``devtoolset-3`` and ``git19``: 

.. code-block:: bash

   scl enable devtoolset-3 git19 bash

.. _lsst-dev-xpra:

Remote Display with xpra
========================

:command:`xpra` can be thought of as "screen for X" and offers advantages over VNC.
It can be very handy and efficient for remote display to your machine from the LSST cluster (e.g., debugging with :command:`ds9`) because it is much faster than a regular X connection when you don't have a lot of bandwidth (e.g., working remotely), and it saves state between connections.
Here's how to use it:

On ``lsst-dev``:

.. code-block:: bash

   xpra start :10
   export DISPLAY=:10

You may have to choose a different display number (>10) if ``:10`` is already in use.

On your local machine, do:

.. code-block:: bash

   xpra attach ssh:lsst-dev:10

You may leave that running, or put it in the background and later use:

.. code-block:: bash

   xpra detach

Then you can open windows on lsst-dev (with DISPLAY=:10) and they will appear on your machine.
If you now kill the ``xpra attach`` on your machine, you'll lose those windows.
When you reattach, they'll reappear.

