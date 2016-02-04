#########################
Using the lsst-dev Server
#########################

``lsst-dev`` is a cluster of servers run by NCSA for LSST DM development work.
To get an account, see the :doc:`Onboarding Checklist </getting-started/onboarding>`.

Overview of Cluster Resources
=============================

- List of `available development servers <https://confluence.lsstcorp.org/display/LDMDG/DM+Development+Servers>`_ and their intended use.
- `System announcements <https://confluence.lsstcorp.org/display/LDMDG/DM+System+Announcements>`_ of the status and planned down-time.
- `Real-time system status <http://lsst-web.ncsa.illinois.edu/nagios>`_ (requires login).
- Reference/test data from SDSS DR7 for Stripe82 is located at: :file:`/lsst7/stripe82/dr7/runs`.
- Report system issues to ``lsst-admin _at_ ncsa.illinois.edu``

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

Load the LSST Environment
=========================

Do the following to set up your shell for development on the LSST cluster (``lsst-dev``, etc.).
You can also following in the `~/.bashrc` file (this is the jist of the :file:`loadLSST.sh` script in the distribution):

.. code-block:: bash

   source ~lsstsw/eups/bin/setups.sh   # bash users
   setup anaconda
   setup git
   setup lsst

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
