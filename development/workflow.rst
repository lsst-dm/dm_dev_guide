#######################################
DM's Collaborative Development Workflow
#######################################

This page describes our procedures for collaborating on LSST DM software and documentation development with `Git <http://git-scm.org>`_, `GitHub <https://github.com>`_ and `JIRA <https://jira.lsstcorp.org/>`_.

You can also read the :doc:`lsstsw Stack Development Tutorial </development/lsstsw_tutorial>` to see how our processes work in a holistic stack development workflow.

.. _git-setup:

Git & GitHub Setup
==================

You need to install Git version 1.8.2, or later, and the Git LFS client to work with our data repositories.
See the :doc:`DM Git LFS documentation </development/git_lfs>` for more information on how to install and setup the Git LFS client for your machine.

We use Git commit authorship metadata to audit copyrights in DM code.
Ensure that Git is setup to use your *institution-hosted* email address (only AURA employees should use their ``lsst.org`` email addresses) in the :file:`~/.gitconfig` file.
You can do this from the command line:

.. code-block:: bash

   git config --global user.name "Your Name"
   git config --global user.email "your_email@institution.edu"

Likewise, in your `GitHub account email settings <https://github.com/settings/emails>`_, add your institution-hosted email.
We recommend that you set this institutional email as your **Primary GitHub** email address.
This step ensures that Git commits you make `directly on GitHub.com <https://help.github.com/articles/github-flow-in-the-browser/>`_ (such as quick documentation fixes) and merges made via the 'big green button' have proper authorship metadata.

*See also*: :ref:`git-setup-best-practices`.
