########################################################
Using Git LFS (Large File Storage) for data repositories
########################################################

This page describes how to use Git LFS for DM development.

DM uses Git LFS to manage test datasets within our :doc:`normal Git workflow </work/flow>`.
`Git LFS is developed by GitHub <https://git-lfs.github.com/>`_, though DM uses its own backend storage infrastructure (see `SQR-001: The Git LFS Architecture <http://sqr-001.lsst.io>`_ for background).

All DM repositories should use Git LFS to store sizeable binary data, such as FITS files, for :abbr:`CI (Continuous Integration)`.
Examples of LFS-backed repositories are `lsst/afwdata <https://github.com/lsst/afwdata>`_, `lsst/testdata_ci_hsc <https://github.com/lsst/testdata_ci_hsc>`_, `lsst/testdata_decam <https://github.com/lsst/testdata_decam>`_ and `lsst/testdata_cfht <https://github.com/lsst/testdata_cfht>`_.

**On this page**

- :ref:`git-lfs-install`
- :ref:`git-lfs-config`
- :ref:`git-lfs-auth`
- :ref:`git-lfs-historical`
- :ref:`git-lfs-using`
- :ref:`git-lfs-tracking`
- :ref:`git-lfs-create`

.. _git-lfs-install:

Installing Git LFS
==================

In most Science Pipelines installations, including those in the Rubin Science Platform, :command:`git lfs` is already installed as part of the ``rubin-env`` conda metapackage.

Otherwise, you can download and install the :command:`git-lfs` client by visiting the `Git LFS <https://git-lfs.github.com>`_ homepage.
Many package managers, like Homebrew_ on the Mac, also provide :command:`git-lfs` (``brew install git-lfs`` for example).

We recommend using the latest Git LFS client.
The *minimum* usable client version for Rubin Observatory is :command:`git-lfs` 2.3.4.

.. Generally our stated Git LFS version requirements should track what's used in CI:
.. https://github.com/lsst/lsstsw/blob/main/bin/deploy

Git LFS requires Git version 1.8.2 or later to be installed.

Before you can use Git LFS with Rubin Observatory data you'll need to configure it by following the next section.

.. _git-lfs-config:

Configuring Git LFS
===================

.. _git-lfs-basic-config:

Basic configuration
-------------------

Run this command to add a ``filter "lfs"`` section to :file:`~/.gitconfig`.
This command has to be done once on every machine you are planning to
read or write Rubin Observatory LFS repos on.

.. code-block:: bash

   git lfs install

.. _git-lfs-config-lsst:

Configuration for Rubin Observatory
-----------------------------------

Read-Only
---------

You're done.  The ``git lfs install`` command that you just ran will
allow you to access everything in Large File Storage.

Try cloning a small data repository to test your configuration:

.. code-block:: bash

   git clone https://github.com/lsst/testdata_subaru

If the resulting new directory is about 220MB in size, as measured by ``du -sh testdata_subaru``, you are correctly configured for Git LFS use.

If you are a developer who will need to update those files, read on.

.. _git-lfs-rw:

Read-Write
----------

This section describes how to configure Git LFS to write to the Rubin
Observatory Large File Storage repositories.

You will first need to acquire a token from Roundtable.  Go to
https://roundtable.lsst.cloud/auth/tokens and request a token with scope
``write:git-lfs``.  It would be best practice to request a token with
a finite lifetime, but on your own conscience be it if you ask for one
that never expires.

Copy that token, because this is the only time Gafaelfawr will show it
to you, and you will need it to push content.

next, add these lines into your :file:`~/.gitconfig` file:

.. code-block:: text

    # Cache auth for write access to DM Git LFS
    [credential "https://git-lfs-rw.lsst.cloud"]
        helper = store

Then edit your :file:`~/.git-credentials` file (create one, if
necessary).  Add a line:

.. code-block:: text

    https://<username>:<token>@git-lfs-rw.lsst.cloud

Where ``<username>`` is the username you used to authenticate to
Roundtable, and ``<token>`` is the token with ``write:git-lfs`` scope
you just acquired.

.. _git-lfs-auth:

Authenticating for push access
==============================

If you want to push LFS-backed files to a Rubin Observatory Git
LFS-backed repository you'll need to configure and cache your
credentials, as described at :ref:`git-lfs-rw`.

For each repository you intend to push to, there is a one-time setup
process you must do when you clone it.

Clone the repository, ``cd`` into it, and update the git LFS URL to use
the read-write URL for that repository, which will be
``https://git-lfs-rw.lsst.cloud/`` followed by the last two components
of the repository (that is, organization and repository name).

For instance, if you were working with
``https://github.com/lsst/testdata_subaru``, you'd just type:

.. code-block:: bash

    git clone https://github.com/lsst/testdata_subaru
    cd testdata_subaru
    git config lfs.url https://git-lfs-rw.lsst.cloud/lsst/testdata_subaru
    git config lfs.locksverify false

.. _git-lfs-historical:

Checking out historical commits
===============================

If you want to check out a historical commit, you first need to know
that arbitrary commits are no longer available.  When we migrated from
``git-lfs.lsst.codes`` to ``git-lfs.lsst.cloud`` we only migrated LFS
objects that were either at the tip of the ``main`` branch or a release
branch (one whose name begins with ``v`` followed by a digit), or were
referenced in a Git tag.

If your proposed checkout meets these criteria, next you will will find
that the LFS object fetch fails, because only recent commits reference
``git-lfs.lsst.cloud`` rather than ``git-lfs.lsst.codes``, and the
checkout will reset ``.lfsconfig`` to its old value.  What you will need
to do in that case is the following.

#. Attempt the checkout as normal.  It will fail when it starts to
   smudge any files that differ from the previous checkout.
#. Next, you must edit ``.lfsconfig`` to reference
   ``https://git.lfs-rw.lsst.cloud/<org>/<repo>`` rather than
   ``https://git-lfs.lsst.codes``; you can do this either by simply editing
   the file, or with ``git config lfs.url
   https://git-lfs-rw.lsst.cloud/<org>/<repo>``.
#. Finally, execute ``git lfs fetch`` to download the LFS objects.

.. _git-lfs-using:

Using Git LFS-enabled repositories
==================================

Git LFS operates transparently to the user.
*Just use the repo as you normally would any other Git repo.*
All of the regular Git commands just work, whether you are working with LFS-managed files or not.

There are three caveats for working with LFS: HTTPS is always used, Git LFS must be told to track new binary file types, and you usually need enough memory to hold the largest file.

First, DM's LFS implementation mandates the HTTPS transport protocol.
Developers used to working with `ssh-agent <https://linux.die.net/man/1/ssh-agent>`_ for passwordless GitHub interaction should use a :ref:`Git credential helper <git-credential-helper>`, and follow the :ref:`directions above <git-lfs-auth>` for configuring their credentials.

Note this *does not* preclude using ``git+git`` or ``git+ssh`` for working with a Git remote itself; it is only the LFS traffic that always uses HTTPS.

Second, in an LFS-backed repository, you need to specify what files are stored by LFS rather than regular Git storage.
You can run

.. code-block:: bash

   git lfs track

to see what file types are being tracked by LFS in your repository.
:ref:`We describe how to track additional file types below <git-lfs-tracking>`.

Third, when cloning or fetching files in an LFS-backed repository, the git internals will expand each file into memory before writing it.
This can be a problem on notebook servers configured with smaller memories.
On these small servers, you can use the following workaround:

.. code-block:: bash

   GIT_LFS_SKIP_SMUDGE=1 git clone <url>
   cd <dir>
   git lfs fetch

This works by skipping the automatic extraction by ``git`` and then manually extracting the files using ``git lfs``, which does not have the same memory constraints.

.. _git-lfs-tracking:

Tracking new file types
=======================

Only file types that are specifically *tracked* are stored in Git LFS rather than the standard Git storage.

To see what file types are already being tracked in a repository:

.. code-block:: bash

   git lfs track

To track a *new* file type (FITS files, for example):

.. code-block:: bash

   git lfs track "*.fits"

Git LFS stores information about tracked types in the :file:`.gitattributes` file.
This file is part of the repo and tracked by Git itself.

You can ``git add``, ``commit`` and do any other Git operations against these Git LFS-managed files.

To see what files are being managed by Git LFS, run:

.. code-block:: bash

   git lfs ls-files

.. _git-lfs-create:

Creating a new Git LFS-enabled repository
=========================================

Configuring a new Git repository to store files with DM's Git LFS is easy.
First, initialize the current directory as a repository:

.. code-block:: bash

   git init .

Make a file called :file:`.lfsconfig` *within the repository*, and write these lines into it:

.. code-block:: text

   [lfs]
        url = https://git-lfs.lsst.cloud
	locksverify = false

Next, track some file types.
For example, to have FITS and ``*.gz`` files tracked by Git LFS,

.. code-block:: bash

   git lfs track "*.fits"
   git lfs track "*.gz"

Add and commit the :file:`.lfsconfig` and :file:`.gitattributes` files to your repository.

Add the remote repository that you're going to push to.

.. code-block:: bash

    git remote add origin <remote repository URL>

Configure your copy to have LFS write access--the LFS config you're
pushing has the read URL in it.

.. code-block:: bash

    git config lfs.url https://git-lfs-rw.lsst.cloud/<org>/<repo_name>
    git config lfs.locksverify false

You can then push the repo up to GitHub with

.. code-block:: bash

   git push origin main

In the repository's :file:`README.md`, we recommend that you include this section:

.. code-block:: text

   Git LFS
   -------

   To clone and use this repository, you'll need Git Large File Storage (LFS).

   Our [Developer Guide](https://developer.lsst.io/tools/git_lfs.html)
   explains how to set up Git LFS for Rubin Observatory development.

.. _Homebrew: http://brew.sh
