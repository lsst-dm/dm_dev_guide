########################################################
Using Git LFS (Large File Storage) for data repositories
########################################################

This page describes how to use Git LFS for DM development.

DM uses Git LFS to manage test datasets within our :doc:`normal Git workflow </work/flow>`.
`Git LFS is developed by GitHub <https://git-lfs.github.com/>`_, though DM uses its own backend storage infrastructure (see `SQR-001: The Git LFS Architecture <http://sqr-001.lsst.io>`_ for background).

All DM repositories should use Git LFS to store binary data, such as FITS files, for :abbr:`CI (Continuous Integration)`.
Examples of LFS-backed repositories are `lsst/afwdata <https://github.com/lsst/afwdata>`_, `lsst/testdata_ci_hsc <https://github.com/lsst/testdata_ci_hsc>`_, `lsst/testdata_decam <https://github.com/lsst/testdata_decam>`_ and `lsst/testdata_cfht <https://github.com/lsst/testdata_cfht>`_.

**On this page**

- :ref:`git-lfs-install`
- :ref:`git-lfs-config`
- :ref:`git-lfs-auth`
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
The *minimum* usable client version for LSST is :command:`git-lfs` 2.3.4.

.. Generally our stated Git LFS version requirements should track what's used in CI:
.. https://github.com/lsst/lsstsw/blob/main/bin/deploy

Git LFS requires Git version 1.8.2 or later to be installed.

Before you can use Git LFS with LSST data you'll need to configure it by following the next section.

.. _git-lfs-config:

Configuring Git LFS
===================

.. _git-lfs-basic-config:

Basic configuration
-------------------

Run this command to add a ``filter "lfs"`` section to :file:`~/.gitconfig`.
This command, and the LSST configuration below, have to be done once on every machine you are planning to work with LSST LFS repos on.

.. code-block:: bash

   git lfs install

.. _git-lfs-config-lsst:

Configuration for LSST
----------------------

LSST uses its own Git LFS servers.
This section describes how to configure Git LFS to pull from LSST's servers.

First, add these lines into your :file:`~/.gitconfig` file:

.. literalinclude:: samples/git_lfs_gitconfig.txt
   :language: text

Then add these lines into your :file:`~/.git-credentials` files (create one, if necessary):

.. literalinclude:: samples/git_lfs_git-credentials.txt
   :language: text

Trying cloning a small data repository to test your configuration:

.. code-block:: bash

   git clone https://github.com/lsst/testdata_subaru

*That's it.*

.. _git-lfs-auth:

Authenticating for push access
==============================

If you want to push to a LSST Git LFS-backed repository you'll need to configure and cache your credentials.

Due to GitHub's authentication interface, you must use a personal access token instead of a password, regardless of whether or not you have two-factor authentication enabled.
You can set up a personal token at https://github.com/settings/tokens with ``public_repo`` and ``read:org`` permissions.

First, set up a credential helper to manage your GitHub credentials (Git LFS won't use your SSH keys).
:ref:`We describe how to set up a credential helper for your system in the Git set up guide <git-credential-helper>`.

Then the next time you run a Git command that requires authentication, Git may ask you to authenticate with both GitHub (for the push via HTTPS) and with LSST's Git LFS server (for authentication of the LFS upload)::

   Username for 'https://github.com': <GitHub username>
   Password for 'https://<user>@github.com': <GitHub token>
   Username for 'https://git-lfs.lsst.codes': <GitHub username>
   Password for 'https://<user>@git-lfs.lsst.codes': <GitHub token>

At the prompts, enter your GitHub username and token.

Once your credentials are cached, you won't need to repeat this process on your system (:ref:`unless you opted for the cache-based credential helper <git-credential-helper>`).

If you find that ``git push`` is not working but also not asking you for credentials, you may need to manually insert the username/password or token into the credential store or macOS keychain.

.. _git-lfs-using:

Using Git LFS-enabled repositories
==================================

Git LFS operates transparently to the user.
*Just use the repo as you normally would any other Git repo.*
All of the regular Git commands just work, whether you are working with LFS-managed files or not.

There are three caveats for working with LFS: HTTPS is always used, Git LFS must be told to track new binary file types, and you usually need enough memory to hold the largest file.

First, DM's LFS implementation mandates the HTTPS transport protocol.
Developers used to working with `ssh-agent <http://www.openbsd.org/cgi-bin/man.cgi?query=ssh-agent&sektion=1>`_ for passwordless GitHub interaction should use a :ref:`Git credential helper <git-credential-helper>`, and follow the :ref:`directions above <git-lfs-auth>` for configuring their credentials.

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
        url = https://git-lfs.lsst.codes

Next, track some files types.
For example, to have FITS and ``*.gz`` files tracked by Git LFS,

.. code-block:: bash

   git lfs track "*.fits"
   git lfs track "*.gz"

Add and commit the :file:`.lfsconfig` and :file:`.gitattributes` files to your repository.

You can then push the repo up to GitHub with

.. code-block:: bash

   git remote add origin <remote repository URL>
   git push origin main

We also recommend that you include a link to this documentation page in your :file:`README` to help those who aren't familiar with DM's Git LFS.

In the repository's :file:`README`, we recommend that you include this section:

.. code-block:: text

   Git LFS
   -------

   To clone and use this repository, you'll need Git Large File Storage (LFS).

   Our [Developer Guide](https://developer.lsst.io/tools/git_lfs.html)
   explains how to set up Git LFS for LSST development.

.. _Homebrew: http://brew.sh
