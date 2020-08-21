#########################
Using the lsst-dev Server
#########################

.. ATTENTION::
  **The lsst-dev servers will be turned off on Oct 1, 2020.**

  Developers should instead use :doc:`lsst-login <lsst-login>` and/or :doc:`lsst-devl <lsst-devl>` nodes.

The material presented below is for historical reference and will be removed in the future.

------------

``lsst-dev`` is a set of servers run by NCSA for Rubin Observatory development work.
The cname ``lsst-dev.ncsa.illinois.edu`` directs to ``lsst-dev01.ncsa.illinois.edu`` and this system serves as the primary development server for the team. There are currently 3 identical development servers to choose from:

- ``lsst-dev01.ncsa.illinois.edu``
- ``lsst-dev02.ncsa.illinois.edu``
- ``lsst-dev03.ncsa.illinois.edu``

To get an account, see the :doc:`Onboarding Checklist </team/onboarding>`.

This page is designed to assist developers in their work on the ``lsst-dev`` servers:

#. :ref:`lsst-dev-overview`
#. :ref:`lsst-dev-password`
#. :ref:`lsst-dev-ssh-keys`
#. :ref:`lsst-dev-software`

.. _lsst-dev-overview:

Overview of Cluster Resources
=============================

Refer to :ref:`lsst-login-overview` for a general overview of LDF cluster resources.

- All of the ``lsst-dev`` systems have access to the :ref:`verification-gpfs`, including:

  - Reference/test data from SDSS DR7 for Stripe82, which is located at :file:`/datasets/sdss/preprocessed/dr7`.
  - Several other datasets available in :file:`/datasets`.  See README files in each dataset.

.. _lsst-dev-password:

Account Password
================

You can log into Rubin development servers at NCSA with your NCSA account and password. You can reset your NCSA password at the following URL:

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


.. _lsst-dev-software:

Common Software Available
=========================

Refer to :doc:`software` for more details about software available for use on ``lsst-dev`` nodes.

