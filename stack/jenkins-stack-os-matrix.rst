##############################################################
Testing the LSST DM Stack with the Jenkins stack-os-matrix Job
##############################################################

`stack-os-matrix`_ is the continuous integration (CI) job that DM developers must run to ensure tests pass before merging changes to any LSST EUPS Stack package.
This page explains how to run the `stack-os-matrix`_ job and find build and test logs.

For more information about the DM's Jenkins continuous integration service, see :doc:`/jenkins/getting-started`.

Running a stack-os-matrix job
=============================

1. Open the `stack-os-matrix dashboard`_ in a browser directly or by clicking on the **stack-os-matrix** job from the main dashboard at https://ci.lsst.codes.

2. Click on the **Run** button near the top of the page.

3. Configure the run in the pop-up dialog:

   - **Set the list of Git refs** (branch or tag names) to check out from Stack Git repositories.

     For example, if you enter ``tickets/DM-2 tickets/DM-1``, the build system will attempt to check out the ``tickets/DM-2`` branch in Stack packages.
     If a package does not have a ``tickets/DM-2`` branch, it will attempt to check out the ``tickets/DM-1`` branch.
     If a package has neither branch, it falls back to checking out the ``master`` branch.

   - **Set the list of EUPS packages** to build.
     Use the default (``lsst_distrib``) to build and test your changes with a full Stack.
     To improve build times you can instead specify the name of the package you are actively developing and check the **Skip Demo** box.

   - **Check the Skip Demo** option only if you are testing your package alone (in conjunction with specifying your package in the prior text box).

     Before you merge a ticket branch to ``master``, **you must** run a stack-os-matrix Job without **Skip Demo** enabled so that the full Stack is built and tested with your changes.

     When the ``demo`` is run, the `lsst_ci`_ top-level package is automatically added to the build and the `lsst_dm_stack_demo`_ is run to test a simple :command:`processCcd.py`\ -based pipeline.

4. Click the **Run** button in the dialog to start the build.

Monitoring the run status
=========================

Your new job is added to the top of the table on the `stack-os-matrix dashboard`_.
Click on the row to see a detail page for the run.

The pipeline diagram at the top of the detail page shows the status of the build on each supported platform.
Click on the icon for the platform you're interested in.

The progress for each build step is listed on the run detail page.
The most important build step is ``./buildbot-scripts/jenkins_wrapper.sh`` where the lsstsw rebuild is run.
Click on that step to see build and test progress for each package.

Getting stack-os-matrix notifications in Slack
==============================================

Jenkins sends status notifications to the `#dmj-stack-os-matrix`_ channel on Slack when your job starts and finishes.
See :ref:`jenkins-slack-notifications` for more information.

Viewing build and test results
==============================

Click on the **Tests** tab from the run detail pages to see the status of individual tests.

For more complex build and test failures, it may be most efficient to inspect the full build logs and :file:`*.failed` files that show unit test failures.
You can find these :file:`*.failed` files, along with build logs, under the **Artifacts** tab from the run detail pages.
You can even download all the logs and :file:`*.failed` files for a build by scrolling to the bottom and clicking on the **Download All** button.

.. _`stack-os-matrix dashboard`:
.. _`stack-os-matrix`: https://ci.lsst.codes/blue/organizations/jenkins/stack-os-matrix/activity
.. _`lsst_ci`: https://github.com/lsst/lsst_ci
.. _`lsst_dm_stack_demo`: https://github.com/lsst/lsst_dm_stack_demo
.. _`#dmj-stack-os-matrix`: https://lsstc.slack.com/messages/C9A31S9MG
