###############################################
Development Tutorial with lsstsw and lsst-build
###############################################

This page describes a complete workflow for developing the LSST Data Management software using the ``lsstsw`` build tool.

1. :ref:`lsstsw-workflow-obtaining-lsstsw-stack`
2. :ref:`lsstsw-workflow-working-ticket`
3. :ref:`lsstsw-workflow-jenkins`
4. :ref:`lsstsw-workflow-pr`
5. :ref:`lsstsw-workflow-rebuild`
6. :ref:`lsstsw-workflow-ext`

Developers should also consult the :doc:`workflow` page for development policies and procedures, along with other pages of the :ref:`developer guide <part-developer-guide>`.

.. TODO once more workflows are published, link to them here as well

.. _lsstsw-workflow-prerequisites:

Prerequisites
=============

Before embarking on Stack development, ensure you have all software dependencies installed on your system.
These dependencies are listed in the :doc:`guide to installing the stack from source </install>`.
Additionally, you should follow our guide to :ref:`configuring Git, Git LFS and GitHub` to work with DM repositories.

.. _lsstsw-workflow-obtaining-lsstsw-stack:

Obtaining a Development Stack with lsstsw
=========================================

Code for the LSST Stack is distributed across many Git repositories (see `github.com/lsst <https://github.com/lsst>`_).
`lsstsw <https://github.com/lsst/lsstsw>`_ is a tool that helps you manage the codebase by automating the process of cloning all of these repositories and building that development Stack for testing.

.. _lsstsw-workflow-obtaining-lsstw-stack-get:

Step 1. Get lsstsw
------------------

Begin by choosing a work directory, then clone ``lsstsw`` into it:

.. prompt:: bash

   git clone https://github.com/lsst/lsstsw.git
   cd lsstsw

.. _lsstsw-workflow-obtaining-lsstw-stack-deploy:

Step 2. Deploy lsstsw
---------------------

Prepare the development environment by running two commands in the :file:`lsstsw/` directory:

.. prompt:: bash

   ./bin/deploy
   . bin/setup.sh

The ``deploy`` script automates several things for you:

1. installs a miniconda_ Python environment specific to this lsstsw workspace,
2. installs EUPS_ in :file:`eups/current/`,
3. clones `lsst-build`_, which will run the build process for us,
4. clones versiondb_, a robot-made Git repository of package dependency information, and
5. creates an empty Stack *installation* directory, :file:`stack/`.

By default, ``lsstsw`` `clones repositories using HTTPS <https://github.com/lsst/lsstsw/blob/master/etc/repos.yaml>`_.
:ref:`Setting up a Git credential helper <git-credential-helper>` will allow you to push new commits up to GitHub without repeatedly entering your GitHub credentials.

The ``setup.sh`` step enables EUPS_, the package manager used by LSST.
**Whenever you open a new terminal session, you need to run '. bin/setup.sh' to activate your lsstsw environment.**

.. _lsst-build: https://github.com/lsst/lsst_build
.. _versiondb: https://github.com/lsst/versiondb
.. _EUPS: https://github.com/RobertLuptonTheGood/eups
.. _miniconda: http://conda.pydata.org/miniconda.html

.. _lsstsw-workflow-obtaining-lsstw-stack-rebuild:

Step 3. Download and build the stack
------------------------------------

Run

.. prompt:: bash

   rebuild lsst_apps

Initially this will ``git clone`` all of the Stack repositories.
A high-bandwidth connection is helpful since the stack contains a non-trivial amount of code and test data.

.. TODO suggest keeping a separate clone of afwdata and linking it when necessary (put in git recipes page)

Next, ``rebuild`` will run our Scons-based build process to compile C++, make Swig bindings, and ultimately create the ``lsst`` Python package.
The Stack is built and installed into the :file:`stack/` directory inside your :file:`lsstsw/` work directory.

Note that we ran ``rebuild lsst_apps`` since `lsst_apps`_ is a meta package that depends on the entire Stack, thus ensuring you have a complete Stack to develop on.

.. _lsst_apps: https://github.com/lsst/lsst_apps

.. _lsstsw-workflow-obtaining-lsstw-stack-current:

Step 4. Tag the current build
-----------------------------

Once the ``rebuild`` step finishes, take note of the build number printed on screen.
It is formatted as "``bNNNN``."
Tell EUPS this is the current build by making a clone of the build's EUPS tag and calling it "``current``:"

.. prompt:: bash

   eups tags --clone bNNNN current

*Note:* this command will print ``eups tags: local variable 'tagNames' referenced before assignment``; this is a known EUPS bug that doesn't affect functionality.

You now have a working Stack, ready for development.

.. _lsstsw-workflow-working-ticket:

Working on a Ticket
===================

At LSST Data Management, we use tickets on `JIRA`_ to track work.
You might be assigned an existing ticket, or you might create a new ticket to work on.
These tickets are named "``DM-MMMMM``."

.. _JIRA: https://jira.lsstcorp.org

.. TODO link to in-depth guide on JIRA workflows

When beginning any Stack development work, ensure lsstsw is setup in your terminal sessions.
From the ``lsstsw/`` directory:

.. prompt:: bash

   . bin/setup.sh

.. _lsstsw-workflow-working-ticket-branch:

Step 1. Create ticket branches for repositories in development
--------------------------------------------------------------

Make a :ref:`ticket branch <git-branching>` for each repository involved in your ticket work.
From a package's repository in ``lsstsw/build``:

.. prompt:: bash

   git checkout -b tickets/DM-MMMM

*(repeat for other packages in development)*

Note that you can do local work on arbitrarily-named branches, but all commits that you intend to make a pull request for must be in ``tickets/DM-MMMM`` branches.
If you want to push non-ticket work up an LSST repository on GitHub you can prefix your branch's name with ``u/{{username}}/`` (as in, your GitHub username).
:ref:`Our developer workflow page explains DM's Git branch policy. <git-branching>`

Next, create this branch on the GitHub remote.
From a package's repository in ``lsstsw/build``:

.. prompt:: bash

   git push -u

*(repeat for other packages in development)*

This initial push will create a remote branch ``origin/tickets/DM-MMMM`` and *track* it so that you can simply ``git push`` and ``git pull`` without arguments between the ticket branch on the ``origin`` remote and your local clone.

.. _lsstsw-workflow-working-ticket-declare:

Step 2. Declare these repositories to EUPS
------------------------------------------

We need to tell EUPS_ about these development repositories (with ``eups declare``) and set them up for building (with ``setup``).
From a package's repository in ``lsstsw/build``:

.. prompt:: bash

   eups declare -r . -t $USER {{package_name}} git
   setup -r . -t $USER

*(repeat for other packages in development)*

Unpacking the ``eups declare`` arguments:

- ``-r .`` is the path to the package's repository, which is the current working directory.
  You don't *need* to be in the repository's directory if you provide the path appropriately.
- ``-t $USER`` sets the EUPS *tag*.
  We use this because your username (``$USER``) is an allowed EUPS tag.
- ``git`` is used as an EUPS *version*.
  Semantically we default to calling the version "``git``" to indicate this package's version is the HEAD of a Git development branch.

In the above ``eups declare`` command we associated the package version "``git``" with the tag "``$USER``."
In running ``setup``, we told EUPS to setup the package *and its dependencies* with the version associated to the ``$USER`` tag.
If the ``$USER`` tag isn't found for dependencies, EUPS will revert to using versions of dependencies linked to the ``current`` tag.
This is why we initially declared the entire lsstsw repository to have the version ``current``.

.. why not setup -j? Means setup *just* this package, no dependencies

.. _lsstsw-workflow-working-ticket-scons:

Step 3. Compile and test with SCons
-----------------------------------

Develop the package(s) as you normally would.
To build the Stack with the newly-developed package, run SCons from the repository of a package being developed:

.. prompt:: bash

   scons -Q -j 6 opt=3 

These flags tell SCons to build with flags:

- ``-Q``: reduce logging to the terminal,
- ``-j 6``: build in parallel (e.g., with '6' CPUs),
- ``opt=3``: build with level 3 optimization.

This ``scons`` command will run several targets by default, in sequence:

1. ``lib``: build the C++ code and SWIG interface layer
2. ``python``: install the Python code
3. ``tests``: run the test suite
4. ``example``: compile the examples,
5. ``doc``: compile Doxygen-based documentation, and
6. ``shebang``: convert the ``#!/usr/bin/env`` line in scripts for OS X compatibility (see `DMTN-001 <http://dmtn-001.lsst.io>`_).

You can build a subset of these targets by specifying one explicitly.
To simply compile C++, SWIG, build the Python package and run tests:

.. prompt:: bash

   scons -q -j 6 opt=3 tests

If you are developing multiple packages simultaneously on the same ticket branch, you can compile and test all of them with the ``rebuild`` command from :file:`lsstsw/`:

.. prompt:: bash

   rebuild -r tickets/DM-MMMM lsst_apps

This will build all Stack repositories within the ``lsst_apps`` umbrella using the ``tickets/DM-MMMM`` ticket branch if available (falling back to the ``master`` branch).

.. _lsstsw-workflow-jenkins:

Continuous Integration with Jenkins
===================================

We use a Jenkins instance to run continuous integration tests on the LSST Stack.
Jenkins tests the Stack against multiple environments, ensuring that your code is robust.

Step 1. Ensure the code is pushed
---------------------------------

``git push`` all commits in development branches of packages to the remote development branches on GitHub.

Step 2. Log into ci.lsst.codes
------------------------------

Open https://ci.lsst.codes/job/stack-os-matrix/build?delay=0sec in a browser and setup an account if you have not already done so.
Once logged in you will see the Jenkins job submission page.
On that page:

1. Enter the name(s) of development branches to include in the build in the **BRANCHES** field.
2. Click the **Submit** button and wait.

You can monitor builds in the `"Bot: Jenkins" HipChat room <https://lsst.hipchat.com/rooms/show/1648522>`_.

.. _lsstsw-workflow-pr:

Making a Pull Request and Merging
=================================

Once your code is passing tests, it's ready to be packaged, sent for review, and ultimately merged.

.. _lsstsw-workflow-pr-rebase:

Step 1. Rebase Your commits
---------------------------

Before you push to GitHub, you should clean up your Git history.

First, ensure that you are working against the latest ``master`` branch.
(If you are using an *integration branch*, such as ``release``, replace mentions of ``master`` with that integration branch in what follows).

.. based on RFC-21 https://jira.lsstcorp.org/browse/RFC-21

.. prompt:: bash

   git fetch

If ``git fetch`` shows that new commits on ``master`` are available, pull them into master

.. prompt:: bash

   git checkout master
   git pull
   git checkout {{your work branch}}

Then rebase your work against ``master``:

.. prompt:: bash

   git rebase -i master

This command will open an editor (matching ``$EDITOR`` by default) and allow you to squash and re-word commit messages as necessary.
`See the section "Interactive Mode" of Git manual for in information on interactive Git rebase. <https://git-scm.com/docs/git-rebase>`_
For advice on writing Git commit messages, `Tim Pope wrote a good article <http://tbaggery.com/2008/04/19/a-note-about-git-commit-messages.html>`_.

.. TODO link to our own policy on commit message; link to Pope's article from there

If you were working on a personal branch, create a ticket branch (using the naming convention ``tickets/DM-MMMM``) from your personal branch:

.. prompt:: bash

   git checkout -b tickets/DM-MMMM

While you're cleaning up your commits, you should also check that your work adheres to our code standards:

1. Did I add unit tests to validate new functionality?
2. Did I follow the `Python <https://confluence.lsstcorp.org/display/LDMDG/Python+Coding+Standard>`_ and `C++ code <https://confluence.lsstcorp.org/pages/viewpage.action?pageId=16908666>`_ style guides?
3. Did I update the documentation to reflect this work (package user guide and the *in situ* API documentation)?

.. TODO link to our style guides once they're in the docs.

.. _lsstsw-workflow-pr-push:

Step 2. Push and create a pull request
--------------------------------------

Once your work is ready,

.. prompt:: bash

   git push

your ticket branch to the remote ticket branch on GitHub
(or ``git push -u`` if you have not already created the remote branch).

Open the package's GitHub page and create a pull request.
Your pull request includes a message; use this message as an opportunity to briefly introduce the reviewer to the work you are doing.
Follow `GitHub's help on creating pull requests <https://help.github.com/articles/creating-a-pull-request/>`_ if you are unfamiliar with the process.

.. _lsstsw-workflow-pr-assign:

Step 3. Assign a reviewer
-------------------------

On JIRA, use the *Workflow* button to switch the ticket's state to *In Review.*

JIRA will ask you to assign reviewers.
Good reviewers might be experts in the package or domain your are developing.
But also don't overload a small group of people with code reviews.
It's also a good idea to distribute your review assignments across the collaboration.
In particular, asking junior team members to review code is a good way to have them broaden their knowledge of the LSST Stack.

JIRA will also ask you to write a comment associated with the review request.
Simply use the message from your GitHub pull request.

.. _lsstsw-workflow-pr-respond:

Step 4. Respond to the reviewer's comments
------------------------------------------

The reviewer will provide comments on your work in the GitHub pull request page.
If the ticket spans several repositories, coordinating comments might be made on the JIRA ticket page as well.

Address the reviewer's comments by adding *new* commits to the pull request.
You can do this by simply pushing additional commits onto the ticket branch in the remote GitHub repository.

In you commit messages, mention the aspect of the code review that each commit addresses.

Avoid rebasing the ticket branch *until the reviewer signs off.*
The full commit history helps the reviewer verify that the issues have been addressed.

.. _lsstsw-workflow-pr-rebase-again:

Step 5. Rebase the Ticket Branch
--------------------------------

When the review is complete, you will want to rebase your ticket branch's commit history so that the history is useful, and able to be merged on the current ``master``/integration branch without conflicts.
Repeat the same steps as in :ref:`Step 1 <lsstsw-workflow-pr-rebase>` to accomplish this.

If you needed to resolve any rebase conflicts, re-run tests locally and on Jenkins.

Push the rebased work up to the ticket branch on GitHub:

.. prompt:: bash

   git push --force origin tickets/DM-MMMM

Our policy is to leave ticket branches on GitHub intact; do not delete the ticket branch on GitHub when you're done with the ticket.

.. _lsstsw-workflow-pr-merge:

Step 6. Merge the ticket branch and push master
-----------------------------------------------

Once the pull request is rebased against master, you can merge your ticket branch into the Package's ``master`` branch by clicking the green **Merge** button on the GitHub Pull Request page
Alternatively, you may do the merge on the command line:

.. prompt:: bash

   git checkout master
   git merge --no-ff tickets/DM-MMMM
   git push

Include the ticket name (``DM-MMMM``) in the merge commit message.

Again, ensure that your ticket branch can be *merged without conflicts.*
If there are, you may need to ``git rebase`` your ticket branch onto the package's ``master`` branch.
If this is the case, re-run tests locally and on Jenkins.

.. see RFC-21 https://jira.lsstcorp.org/browse/RFC-21

.. _lsstsw-workflow-pr-undeclare:

Step 7. Undeclare EUPS tags/versions
------------------------------------

Remove your EUPS username tag from the packages.
From the package's repository:

.. prompt:: bash

   eups undeclare -t $USER {{package_name}} git

Replace the version name as needed if you didn't use the default EUPS version 'git'
(from :ref:`Step 2 <lsstsw-workflow-working-ticket-declare>` of *Working on a Ticket*).

.. _lsstsw-workflow-pr-close:

Step 8. Close the JIRA ticket
-----------------------------

If this work was associated with a JIRA ticket, close this ticket now.
On the ticket's JIRA page, use the **Workflow** button and select **Done.**

Ensure that Story Points are correctly allocated to the ticket *before* closing it.

.. _lsstsw-workflow-rebuild:

Rebuilding your lsstsw development stack
========================================

Once your ticket is complete, you will need to refresh your lsstsw stack.
This involves pulling ``master`` branches for all Stack repositories and recompiling the Stack from source.
``lsstsw`` automates this with the ``rebuild`` command.
Before rebuilding, ensure that any work in any Git repository has been pushed to GitHub.
``rebuild`` wipes the existing repositories.
Unpushed work will be deleted.

From the ``lsstsw/`` directory:

.. prompt:: bash

   rebuild lsst_apps

Then re-tag the build as current (see :ref:`above <lsstsw-workflow-obtaining-lsstw-stack-current>`).

.. _lsstsw-workflow-ext:

Extending the lsstsw Workflow
=============================

The above workflow described an idealized case of working on a single ticket.
This section describes how to extend the basic workflow for more complex cases.

.. _lsstsw-workflow-ext-rebuild:

Refreshing the master for the entire stack
------------------------------------------

If the ticket is taking an extended time to develop, you may need to update the master branches of the entire Stack to reliably test and merge your ticket branch.
The most robust way to do this is by rebuilding the lsstsw environment completely (:ref:`see above <lsstsw-workflow-rebuild>`).

Before doing, ensure that all work is pushed to branches on GitHub.

After the rebuild, you will need to EUPS tag the current Stack, following :ref:`the instructions above <lsstsw-workflow-obtaining-lsstw-stack-current>`.

Finally, checkout your work branches from the GitHub remote and :ref:`declare these work repositories to EUPS following <lsstsw-workflow-working-ticket-declare>`.

..
  Working on Multiple Tickets in lsstsw
  -------------------------------------
  
  TODO
  
  - undeclare
  - declare
  - setup
