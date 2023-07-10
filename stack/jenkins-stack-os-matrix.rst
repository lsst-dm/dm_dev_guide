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

     If a package has neither branch, it falls back to checking out the ``main`` branch or the branch configured in ``repos.yaml`` in the case of forked third-party packages.
     Because of those third-party packages, you *never* want to specify ``main`` explicitly in this field.
     To check that a ``main``-only build passes, leave the refs box entirely blank.

   - **Set the list of EUPS packages** to build.
     Use the default (``lsst_distrib lsst_ci``) to build and test your changes with a full Stack.
     To improve build times you can instead specify the name of the package you are actively developing.
     Before you merge a ticket branch to ``main``, **you must** run a stack-os-matrix Job with at least the default packages so that the full Stack is built and tested with your changes.

     There are also several packages that can be appended to the default to do more thorough testing at the cost of much longer build times:

     - ``ci_cpp`` exercises the Calibration Products Pipeline in ways that are too computationally expensive for unit tests in ``cp_pipe``.
       It is run as part of the nightly ``lsst_distrib`` Jenkins job, and it takes about 20 minutes.
     - ``ci_hsc`` runs a variant of the Data Release Production (DRP) pipeline, including single-frame processing and coaddition, on HSC engineering data. This package is run in a separate nightly Jenkins job, and it takes about 2 hours.
     - ``ci_imsim`` runs a slightly simplified version of the DRP pipeline on simulated Rubin Observatory data. Like ``ci_hsc``, it's run nightly in its own nightly Jenkins job, and also takes about 2 hours.
     - ``ci_middleware`` runs a few variants of the DRP pipeline in a "mocked" mode in which the algorithmic code and true I/O routines are replaced by simple placeholders that just exercise the overall flow of datasets between tasks (i.e. whether the pipelines are self-consistently defined) and the middleware tooling for predicting and running task execution.  It is run nightly with ``ci_cpp`` in the ``lsst_distrib`` Jenkins job, and it takes about 20 minutes.

     DM developers should use their own judgement when determining which of these to run when testing a ticket branch, but the general expectation is that at least one of ``ci_hsc`` and ``ci_imsim`` (and often both) is run for changes to algorithmic or data structure code that is included in the DRP pipelines.
     Changes to ``ip_isr`` or ``cp_pipe`` should be tested with ``ci_cpp``.
     Middleware changes and changes to DRP pipeline *structure* (new tasks or changes to connections) should be tested with ``ci_middleware``, and major middleware changes should be tested with all ``ci_*`` packages.

   - **Set the conda environment** to run on.
     The default is the latest ``rubin-env`` package.
     You should only need to change this when testing a new environment, or to temporarily work around bugs introduced in the latest version.

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
