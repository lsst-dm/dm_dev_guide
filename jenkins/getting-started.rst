###########################################
Jenkins rubin-ci.slac.stanford.edu Overview
###########################################

Data Management operates a Jenkins continuous integration cluster at https://rubin-ci.slac.stanford.edu.
You will typically use Jenkins to run the ``stack-os-matrix`` job to build and run unit tests in the LSST Stack as part of `DM's development workflow <processes/workflow.rst>`_.
See :doc:`/stack/jenkins-stack-os-matrix` for details.

Logging in
==========

Log into Jenkins by visiting https://rubin-ci.slac.stanford.edu/blue and authenticate with your GitHub credentials.
Any member of the `lsst`_, `lsst-dm`_, or `lsst-sqre`_ GitHub organizations is authorized to use https://rubin-ci.slac.stanford.edu.
See the :doc:`/team/onboarding` for more information.

Using the Jenkins dashboard
===========================

This section summarizes how to use the Jenkins dashboard, which is the first view you see when browsing to https://rubin-ci.slac.stanford.edu/blue.
`Jenkins's own dashboard documentation <https://jenkins.io/doc/book/blueocean/dashboard/>`_ provides additional information.

Browsing Jenkins jobs
---------------------

From https://rubin-ci.slac.stanford.edu/blue, you see a listing of Jenkins jobs.
Each job fulfills a different purpose, see :ref:`jenkins-jobs`.

To access a job, click on the job's name.
This takes you to a page where you can run the job and review past runs.

Favoriting Jenkins jobs
-----------------------

From the https://rubin-ci.slac.stanford.edu/blue dashboard, you can click on the star icon next to any job.
This will favorite the Job.
Favorited jobs appear at the top of the homepage, before other jobs.

We recommend that you favorite the ``stack-os-matrix`` job.

Searching for Jenkins jobs
--------------------------

From the https://rubin-ci.slac.stanford.edu/blue dashboard, you can filter the listing of jobs by using the search box at the top of the page.

Jenkins jobs are organized in directories, so it's helpful to search by directory prefix to find the right job.
The directories are:

- ``qserv``
- ``release``
- ``science-pipelines``
- ``sims``
- ``sqre``

Understanding the weather icons
-------------------------------

Jenkins represents a job's historical patterns of run successes and failures with weather icons throughout the dashboard interface.

.. |img-sunny| image:: jenkins-sunny.svg
   :width: 50px
   :height: 50px
   :align: middle
   :alt: Sunny

.. |img-partially-sunny| image:: jenkins-partially-sunny.svg
   :width: 50px
   :height: 50px
   :align: middle
   :alt: Partially sunny

.. |img-cloudy| image:: jenkins-cloudy.svg
   :width: 55px
   :height: 35.5px
   :align: middle
   :alt: Cloudy

.. |img-raining| image:: jenkins-raining.svg
   :width: 55px
   :height: 39px
   :align: middle
   :alt: Raining

.. |img-storm| image:: jenkins-storm.svg
   :width: 55px
   :height: 44.5px
   :align: middle
   :alt: Storm

===================== ==============================
Icon                  Percent of recent runs passing
===================== ==============================
|img-sunny|           >80%
|img-partially-sunny| 61% – 80%
|img-cloudy|          41% — 60%
|img-raining|         21% – 40%
|img-storm|           <21%
===================== ==============================

Getting Job status in Slack
===========================

When jobs start and end (either as a success or failure), Jenkins posts a message to the `#dm-jenkins`_ channel in the LSSTC Slack team.
Jenkins also mentions developers in specific notification channels, see :ref:`jenkins-slack-notifications`.

.. _jenkins-jobs:

Jenkins job listing
===================

This section describes the Jenkins jobs that are important for most DM developers.

.. _jenkins-job-stack-os-matrix:

stack-os-matrix
---------------

`stack-os-matrix`_ is the job that DM developers must run to ensure tests pass before merging changes to any LSST EUPS Stack package.
For details on how to run this job, see :doc:`/stack/jenkins-stack-os-matrix`.

.. _jenkins-job-science-pipelines-lsst-distrib:

science-pipelines/lsst\_distrib
-------------------------------

`science-pipelines/lsst_distrib`_ is automatically run nightly to test the ``main`` branches of all packages in the ``lsst_distrib`` stack.
This job runs from a clean slate to discover issues that might be hidden by the caching behavior of the stack-os-matrix job.

.. _jenkins-job-qserv-dax-webserv:

qserv/dax\_webserv
------------------

`qserv/dax_webserv`_ is automatically run nightly to test the ``main`` branches of all packages in the ``dax_webserv`` stack.
This job runs from a clean slate to discover issues that might be hidden by the caching behavior of the stack-os-matrix job.

.. _jenkins-job-qserv-distrib:

qserv/qserv\_distrib
--------------------

`qserv/qserv_distrib`_ is automatically run nightly to test the ``main`` branches of all packages in the ``qserv_distrib`` stack.
This job runs from a clean slate to discover issues that might be hidden by the caching behavior of the stack-os-matrix job.

.. _jenkins-slack-notifications:

Slack job notifications
=======================

You can get Slack notifications when a Jenkins job starts and stops.

Configuring Slack to be "@"-mentioned
-------------------------------------

We recommend that you add your GitHub username to your Slack profile.
This allows the Jenkins bot to send you an "@"-mention specifically for the Jenkins jobs that you trigger.
The bot will also invite you to the notification channel if necessary.

To do this, follow :doc:`../communications/slack-github-username`.

Jenkins notification channels
-----------------------------

Each Jenkins job has its own notification channel.
Each channel name starts with a ``#dmj-`` prefix.
Due to length constrains, these channels have abbreviated names based on the Jenkins job.

To find the channel corresponding to a job, `search the channel listing`_ for ``#dmj-`` channels.
The full name of the Jenkins job is included in the channel's description.

Controlling notifications from Jenkins channels
-----------------------------------------------

Jenkins notification Slack channels can be noisy.
Typically you'll want to notice activity for only the jobs that you trigger.

The best way to do this is to `mute the channel`_.
The channel will still be highlighted when your jobs run because you will be ``@``-mentioned.

More resources
==============

- `Jenkins documentation`_.
  The `Jenkins dashboard documentation`_ includes additional information about the Jenkins interface.
- The `lsst-dm/jenkins-dm-jobs`_ GitHub repository is where DM's Jenkins jobs are defined.

.. _`lsst`: https://github.com/lsst
.. _`lsst-dm`: https://github.com/lsst-dm
.. _`lsst-sqre`: https://github.com/lsst-sqre
.. _`stack-os-matrix`: https://rubin-ci.slac.stanford.edu/blue/organizations/jenkins/stack-os-matrix/activity
.. _`science-pipelines/lsst_distrib`: https://rubin-ci.slac.stanford.edu/blue/organizations/jenkins/science-pipelines%2Flsst_distrib/activity
.. _`qserv/dax_webserv`: https://rubin-ci.slac.stanford.edu/blue/organizations/jenkins/qserv%2Fdax_webserv/activity
.. _`qserv/qserv_distrib`: https://rubin-ci.slac.stanford.edu/blue/organizations/jenkins/qserv%2Fqserv_distrib/activity
.. _`Jenkins documentation`: https://jenkins.io/doc/book/blueocean/
.. _`Jenkins dashboard documentation`: https://jenkins.io/doc/book/blueocean/dashboard/
.. _`lsst-dm/jenkins-dm-jobs`: https://github.com/lsst-dm/jenkins-dm-jobs
.. _`#dm-jenkins`: https://lsstc.slack.com/messages/C2NCSTY3A
.. _`search the channel listing`: https://get.slack.help/hc/en-us/articles/205239967-Browse-and-join-channels
.. _`mute the channel`: https://get.slack.help/hc/en-us/articles/204411433-Mute-a-channel
