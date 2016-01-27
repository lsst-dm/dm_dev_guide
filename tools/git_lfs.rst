########################################################
Using Git Large File Storage (LFS) for Data Repositories
########################################################

DM uses Git LFS to manage test datasets within our :doc:`normal Git workflow </processes/workflow>`.
`Git LFS is developed by GitHub <https://git-lfs.github.com/>`_, though DM uses its own backend storage infrastructure (see `SQR-001: The Git LFS Architecture <http://sqr-001.lsst.io>`_ for background).

All DM repositories should use Git LFS to store binary data, such as FITS files, for :abbr:`CI (Continuous Integration)`.
Examples of LFS-backed repositories are `lsst/afw <https://github.com/lsst/afw>`_, `lsst/hsc_ci <https://github.com/lsst/ci_hsc>`_, `lsst/testdata_decam <https://github.com/lsst/testdata_decam>`_ and `lsst/testdata_cfht <https://github.com/lsst/testdata_cfht>`_.

This page describes how to use Git LFS for DM development.

.. _git-lfs-install:

Installing Git LFS
==================

Git LFS requires Git version 1.8.2 or later to be installed.

Download and install the ``git-lfs`` client by visiting the `Git LFS <https://git-lfs.github.com>`_ homepage.
If you downloaded the binary release, install ``git-lfs`` by running the provided :file:`install.sh`.

Most package managers also provide the ``git-lfs`` client.
Since, LFS is a rapidly evolving technology, package managers will help you keep up with new ``git-lfs`` releases.
For example, Mac users with Homebrew_ can simply run ``brew install git-lfs`` and ``brew upgrade git-lfs``.

.. _git-lfs-config:

Configuring Git and Git LFS
===========================

Once ``git-lfs`` is installed, run

.. code-block:: bash

   git config --global lfs.batch false
   git lfs install

to install the necessary configuration in your :file:`~/.gitconfig` file.

Next add credentials for our git-lfs secondary storage systems to your :file:`~/.gitconfig` file.

.. code-block:: text

   [credential "https://lsst-sqre-prod-git-lfs.s3-us-west-2.amazonaws.com"]
           helper = store
   [credential "https://s3.lsst.codes"]
           helper = store

Next add their authentication information to your :file:`~/.git-credentials` file.

.. code-block:: text
   
   https://:@lsst-sqre-prod-git-lfs.s3-us-west-2.amazonaws.com
   https://:@s3.lsst.codes

.. _git-lfs-anonymous:

.. note::

   Anonymous authentication with the Git LFS server is optional. You will only be able to pull and clone the repository with this configuration.

If you are anonymously authenticating then you must configure git to use an empty username and password with the git-lfs server. Add this to your :file:`~/.gitconfig` file.

.. code-block:: text

   [credential "https://git-lfs.lsst.codes"]
           helper = store

Add this to your :file:`~/.git-credentials` file.

.. code-block:: text
   
   https://:@git-lfs.lsst.codes

.. _git-lfs-auth:

Setting up Git LFS authentication
=================================

Credentials are required to push to an LFS-based repository on GitHub.
Only GitHub users in the LSST GitHub organization can authenticate with DM's storage service.
(Credentials *are not needed to clone or pull* from LFS-backed repositories.)

Git LFS mandates the HTTPS transport protocol.
Since many HTTPS authentications happen during a single clone, push or fetch operation, it is essential that you use a Git credential helper to work effectively with Git LFS.
:ref:`We describe how to setup a credential helper for your system in the deverloper workflow documentation <git-credential-helper>`.

Once a helper is setup, you can cache your credentials by cloning any of DM's LFS-backed repositories.
For example, run:

.. code-block:: bash

   git clone https://github.com/lsst/testdata_decam.git

``git clone`` will ask you to authenticate with DM's git-lfs server::

   Username for 'https://git-lfs.lsst.codes': <GitHub username>
   Password for 'https://<git>@git-lfs.lsst.codes': <GitHub password>

- If you are a member of the LSST GitHub organization you can use your GitHub username and password.
- If you *also* have `GitHub's two-factor authentication <https://help.github.com/articles/about-two-factor-authentication/>`_ enabled, use a personal access token instead of a password. You can setup a personal token at https://github.com/settings/tokens.
- If you are only interested in cloning or pulling, :ref:`configure anonymous authentication <git-lfs-anonymous>` for the git-lfs server.

Once your credentials are cached, you won't need to repeat this process on your system (:ref:`unless you opted for the cache-based credential helper <git-credential-helper>`).

.. _git-lfs-using:

Using Git LFS-enabled repositories
==================================

Git LFS operates transparently to the user.
*Just use the repo as you normally would any other Git repo.*
All of the regular Git commands just work, whether you are working with LFS-managed files or not.

There are two caveats for working with LFS: HTTPS is always used, and Git LFS must be told to track new binary file types.

First, DM's LFS implementation mandates the HTTPS transport protocol.
Developers used to working with `ssh-agent <http://www.openbsd.org/cgi-bin/man.cgi?query=ssh-agent&sektion=1>`_ for passwordless GitHub interaction should use a :ref:`Git credential helper <git-credential-helper>`, and follow the directions above for configuring their credentials.

Note this *does not* preclude using ``git+git`` or ``git+ssh`` for working with a Git remote itself; it is only the LFS traffic that always uses HTTPS.

Second, in an LFS-backed repository, you need to specify what files are stored by LFS rather than regular Git storage.
You can run

.. code-block:: bash

   git lfs track

to see what file types are being tracked by LFS in your repository.
:ref:`We describe how to track additional file types below <git-lfs-tracking>`.

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
        batch = false

Next, track some files types.
For example, to have FITS and ``*.gz`` files tracked by Git LFS,

.. code-block:: bash

   git lfs track "*.fits"
   git lfs track "*.gz"

Add and commit the :file:`.lfsconfig` and :file:`.gitattributes` files to your repository.

Note that older versions of Git LFS used :file:`.gitconfig` rather than :file:`.lfsconfig`.
As of Git LFS version 1.1 `.gitconfig has been deprecated <https://github.com/github/git-lfs/pull/837>`_, but support will not be dropped until LFS version 2.
New LFS-managed repos should use :file:`.lfsconfig`.

We also recommend that you include a link to this documentation page in your :file:`README` to help those who aren't familiar with DM's Git LFS.

.. _Homebrew: http://brew.sh
