.. _jenkins-pipelines-lsst-io-build:

#########################################################################
Building pipelines.lsst.io with Jenkins (sqre/infrastructure/documenteer)
#########################################################################

The `sqre/infrastructure/documenteer`_ Jenkins CI job enables you to create a new build of `pipelines.lsst.io`_.
Since `pipelines.lsst.io`_ is published through LSST the Docs, builds for development branches appear as new editions from the `pipelines.lsst.io/v <https://pipelines.lsst.io/v>`__ version dashboard.

.. important::

   You can't use this Jenkins CI job to test development branches of packages with the `pipelines.lsst.io`_ site build.
   This Jenkins CI job always uses packages corresponding to a released EUPS tag (such as a daily, weekly, or stable release).
   Only the branch of the `pipelines_lsst_io`_ repository can be modified.

   If you need to build and test your package’s documentation, you can do so locally with these methods:

   - :doc:`building-pipelines-lsst-io-locally`
   - :doc:`building-single-package-docs`

.. _jenkins-pipelines-lsst-io-build-running:

Running the documenteer Jenkins CI job
======================================

Go to the `sqre/infrastructure/documenteer`_ job’s page, then click the **Run** button.

The following sections describe how to set each form field.

.. _jenkins-pipelines-lsst-io-build-eups-distrib-tag-name:

EUPS distrib tag name
---------------------

This is the EUPS tag of the ``lsst_distrib`` Stack.
You can set this to a stable release, weekly release, or a daily release.

This means that you can only build documentation for tags of Stack packages that have been released by Jenkins CI.

.. _jenkins-pipelines-lsst-io-build-ltd-edition-slug:

LTD edition slug
----------------

Set this field to either a Git ref or an EUPS tag.
Follow these guidelines:

- If you are building with a non-\ ``master`` Git ref of the `pipelines_lsst_io`_ repository (see :ref:`jenkins-pipelines-lsst-io-build-github-repo-ref`), set this field to the name of the `pipelines_lsst_io`_ branch being built.
- If you are building with a ``master`` Git ref of the `pipelines_lsst_io`_ repository, set this to the :ref:`jenkins-pipelines-lsst-io-build-eups-distrib-tag-name`.

LSST the Docs uses this information to populate the version slug of the edition (the part of the URL after ``/v/``).

.. _jenkins-pipelines-lsst-io-build-github-repo-slug:

github repo slug
----------------

This is the GitHub repository slug for the :ref:`main documentation repository <stack-docs-system-main-repo>`.
This should always be ``lsst/pipelines_lsst_io``.

.. _jenkins-pipelines-lsst-io-build-github-repo-ref:

git repo ref
------------

This is the name of the Git branch or tag of the :ref:`main documentation repository <stack-docs-system-main-repo>` (`pipelines_lsst_io`_) that you want to build.

.. note::

   During development, ``tickets/DM-11216`` is the integration branch for the Jenkins-enabled `pipelines_lsst_io`_\ -enabled repository.
   The ``master`` branch currently doesn’t work with the Jenkins CI-based build.

.. _jenkins-pipelines-lsst-io-docker-image:

Explicit name of release docker image including tag
---------------------------------------------------

Leave this field blank.

.. _jenkins-pipelines-lsst-io-build-run-job:

Run the Job
-----------

Ensure that the **Publish** option is checked so that the build site is published as a development branch on `pipelines.lsst.io`_.

.. _jenkins-pipelines-lsst-io-build-view-results:

Viewing the results
===================

Once the job successfully finishes, open `pipelines.lsst.io/v`_ and find the corresponding edition that you just built.

.. _`pipelines.lsst.io`: https://pipelines.lsst.io
.. _`pipelines.lsst.io/v`: https://pipelines.lsst.io/v
.. _`pipelines_lsst_io`: https://github.com/lsst/pipelines_lsst_io
.. _`sqre/infrastructure/documenteer`: https://ci.lsst.codes/blue/organizations/jenkins/sqre%2Finfrastructure%2Fdocumenteer/activity
