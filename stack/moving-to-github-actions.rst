####################################
Moving to GitHub Actions from Travis
####################################

GitHub Actions execute faster and more reliably than Travis jobs, so we are converting existing repositories to use them.
This document describes how to accomplish this transition for existing packages.
New packages should start with GitHub Actions by default; additional customizations that may be useful are suggested in :doc:`the new package documentation</stack/adding-a-new-package>`.

**Note:** you must have administrator rights to the repository to follow this procedure.

Travis uses a ``.travis.yml`` file that specifies the workflow to be executed when events such as pushes or pull requests occur for the repository.
GitHub Actions use ``.github/workflows/*.yaml`` files instead.
These workflows execute in parallel.
Migrating a package consists of replacing the ``.travis.yml`` file with one or more appropriate GitHub Actions workflows files.

If the ``.travis.yml`` file contains only the default execution of ``flake8`` for Python "lint" checking, this can be done entirely in :ref:`the GitHub web interface <github-actions-web-interface>`, or it can be done a bit more cleanly from :ref:`the command line <github-actions-command-line>`.

If your ``.travis.yml`` does more than run ``flake8``, please consult an expert for assistance.


.. _github-actions-web-interface:

GitHub web interface
====================

#. Go to the repository you are transitioning at ``https://github.com/lsst/{repo}``.
#. Go to the "Settings" page of the repository.
   This may be under the right-side "..." menu depending on your window width.
#. Choose "Branches" in the left sidebar.
#. Under "Branch protection rules", click "Edit" next to branch "main".
#. Under "Require branches to be up to date before merging", uncheck any status checks that contain "travis-ci".
#. Click "Save changes" at the bottom of the page.
#. Go back to the "Code" page and select ``.travis.yml``.
#. Select the "trash can" icon to delete this file.
#. Add a commit comment such as "Remove Travis workflow." and choose a branch name.
   This branch name doesn't need to follow our ``tickets/`` convention; a name like ``u/{user}/remove-travis`` is adequate.
#. Commit the change, create a pull request, and merge it.
#. Go to the "Actions" page (between "Pull Requests" and "Projects" at the top of the GitHub page).
#. Choose the "LSST DM Python lint Workflow" and click on "Set up this workflow".
#. Choose "Start commit".
#. Add a commit comment such as "Add Python lint workflow." and choose a branch name.
   Again, something like ``u/{user}/add-lint-workflow`` is sufficient as a branch name.
#. Commit the change, create a pull request, and merge it.
#. Go back to the "Settings" page, "Branches", "Branch protection rules", and "Edit" next to branch "main".
#. Under "Require branches to be up to date before merging", check the new "lint" checkbox.
#. Click "Save changes" at the bottom of the page.
#. If you like, you may choose "Webhooks" in the left sidebar and delete the ``https://notify.travis-ci.org/`` entry, but it does no harm to leave it.


.. _github-actions-command-line:

Command line
============

#. Clone the repository you are transitioning from ``git@github.com:lsst/{repo}``.
#. Create a branch: ``git checkout -b u/{user}/migrate-to-gha``
#. ``git rm .travis.yml``
#. ``mkdir -p .github/workflows; cd .github/workflows``
#. ``curl -LO https://raw.githubusercontent.com/lsst/.github/main/workflow-templates/lint.yaml``
#. ``git add lint.yaml``
#. ``git commit`` and add a commit message such as "Migrate from Travis to GitHub Actions."
#. ``git push -u origin u/{user}/migrate-to-gha``
#. Create a pull request from your branch.
#. Go to the "Settings" page of the repository.
   This may be under the right-side "..." menu depending on your window width.
#. Choose "Branches" in the left sidebar.
#. Under "Branch protection rules", click "Edit" next to branch "main".
#. Under "Require branches to be up to date before merging", uncheck any status checks that contain "travis-ci".
   Check any other status checks, in particular ``lint``.
#. Click "Save changes" at the bottom of the page.
#. Merge your pull request.
#. If you like, you may choose "Webhooks" in the left sidebar and delete the ``https://notify.travis-ci.org/`` entry, but it does no harm to leave it.


.. _github-actions-further-reading:

Further reading
===============

- `LSST workflow templates <https://github.com/lsst/.github/tree/main/workflow-templates>`__
- `GitHub Actions <https://docs.github.com/en/free-pro-team@latest/actions>`__
