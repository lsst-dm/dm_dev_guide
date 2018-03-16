#############################################
Github Branch Protection, TravisCI and Flake8
#############################################

DM recommends using `Github branch protection <https://help.github.com/articles/about-protected-branches/>`_, `TravisCI <https://travis-ci.org/>`_ and `Flake8 <http://flake8.pycqa.org/en/stable/>`_ on repositories.

.. _branch-protection:

Github Branch Protection
========================

All DM repositories should protect the master branch. Protected branches block some features of Git. Specifically DM protected branches can't be edited from the web, force pushed, deleted or merged until their status checks pass. Furthermore status checks must pass using the latest base branch code.

.. _travisci:

Travis CI
=========

TravisCI is a service that provides continuous integration for Github repositories. This service must be enabled for the repository before it will work. After it is enabled there will be a page available with the TravisCI status for the repository. For example lsst.utils `https://travis-ci.org/lsst/utils <https://travis-ci.org/lsst/utils>`_.

.. _flake8:

Flake8
======

`Flake8 <http://flake8.pycqa.org/en/stable/manpage.html>`_ is a command-line utility for enforcing style consistency across Python projects. It includes `PyFlakes <https://launchpad.net/pyflakes>`_ and `PEP-0008 <https://www.python.org/dev/peps/pep-0008/>`_ lint checks by default. DM uses the repository's :file:`setup.cfg` file to configure flake8. The :doc:`python style guide <../coding/python_style_guide#pep-8-is-the-baseline-coding-style>` has further details on specific lint check exceptions. The following :file:`setup.cfg` file implements DM's lint check exceptions:

.. code-block:: text
   [flake8]
   max-line-length = 110
   ignore = E133, E226, E228, N802, N803
   exclude =
       __init__.py,
       .tests

.. _sqre-gtf:

sqre-gtf
========

`sqre-gtf <https://github.com/lsst-sqre/sqre-gtf>`_ provides command line interfaces to use Github branch protection, TravisCI and Flake8. sqre-gtf runs on Python 2.7, 3.5 and 3.6. You can install it with

.. code-block:: bash

   pip install sqre-gtf

If you haven't used `sqre-codekit <https://github.com/lsst-sqre/sqre-codekit>`_ or sqre-gtf before you will need to create a `Github personal access token <https://github.com/settings/tokens>`_ and put it in :file:`~/.sq_github_token`. The ``github-auth`` script can do this on your behalf.

.. code-block:: bash

   github-auth -u <your_github_login>

           Type in your password to get an auth token from github
           It will be stored in ~/.sq_github_token
           and used in subsequent occasions.

   Password for <your_github_login>: <your_github_password>
   Enter 2FA code: <your_github_2FA>
   Token written to ~/.sq_github_token

There are three core features that sqre-gtf provides. Configuration of Github branch protection, enabling the TravisCI webhook and configuring your repository to use TravisCI to run Flake8 validation.

An example of using sqre-gtf on `lsst.utils <https://github.com/lsst/utils>`_ follows

.. code-block:: bash

   github-protect --owner lsst --repo utils --branch_name master # Add Github branch protection.
   github-travis --owner lsst --repo utils # Enable the TravisCI webhook
   github-update --owner lsst --repo utils --task stack --branch_name tickets/DM-NNNNN --commit_message "DM-NNNNN: Add .travis.yml and setup.cfg to run flake8." --pull --pull_message "DM-NNNNN: Add .travis.yml and setup.cfg to run flake8." # Create a commit and pull request adding .travis.yml and setup.cfg.

Now Github branch protection is enabled and TravisCI is enabled for the repository. The last command creates a PR with `a single commit similar to lsst/utils #33 <https://github.com/lsst/utils/pull/33/commits/9b6411caf561495e8bf169095a8f8b757169ec33>`_. From there, if the repository does not meet the requirements of RFC-162 it will `fail TravisCI <https://travis-ci.org/lsst/utils/builds/228149573>`_. Additional changes may be required to pass TravisCI. @timj made such changes on `lsst/utils #33 <https://github.com/lsst/utils/pull/33>`_.

.. _things-to-be-aware-of:

Things to be Aware of Before Making Changes
===========================================

When updating a repository it is time sensitive. As soon as TravisCI is enabled for your repository it will attempt to run a default TravisCI script on your repository which will likely fail until the ``sqre-gtf`` PR is merged. Another notable change is enabling Github's branch protection. Users will be unable merge PRs until they pass TravisCI. This can always be disabled in `the repository's settings <https://github.com/lsst/utils/settings/branches/master>`_ by `an Overlord <https://github.com/orgs/lsst/teams/overlords>`_.

