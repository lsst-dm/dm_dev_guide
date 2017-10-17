.. note::

   Changes to this document must be approved by the System Architect (`RFC-24 <https://jira.lsstcorp.org/browse/RFC-24>`_).
   To request changes to these standards, please file an :ref:`RFC <decision-making-rfc>`.

.. _writing-ccd:

#######################################
Writing change-controlled documentation
#######################################

Change-controlled documents are documents that require approval from a Change Control Board (CCB) before they can be released.
The project-wide change control process is described in `LPM-19`_, with the process for managing documents being described in `LPM-51`_, and covers those documents using DocuShare handles ``LSE`` or ``LPM`` that must be approved by the Project `CCB`_.
For Data Management, these documents have the DocuShare handle ``LDM`` and must be approved by the DM CCB using the :ref:`RFC <decision-making-rfc>` process.
The DM document management process is formally described in `LDM-294`_.

Change-controlled documents can be written using the Word templates defined in `Document-9224`_, but the preference within Data Management is to write change-controlled documents in LaTeX using the `lsstdoc document class`_ provided by the `lsst-texmf`_ package and to develop these documents using Git repositories within the LSST organization on GitHub (https://github.com/lsst).

This page describes the development and release processes of change-controlled documents produced by DM:

- :ref:`ccd-drafting`
- :ref:`ccd-release`
- :ref:`ccd-hotfix`

Additional subprocedures and references:

- :ref:`ccd-docushare-upload`
- :ref:`ccd-git-api`

.. _CCB: https://project.lsst.org/groups/ccb/
.. _Document-9224: https://ls.st/Document-9224
.. _lsst-texmf: https://lsst-texmf.lsst.io
.. _lsstdoc document class: https://lsst-texmf.lsst.io/lsstdoc.html
.. _LPM-19: https://ls.st/LPM-19
.. _LPM-51: https://ls.st/LPM-51
.. _GitHub: https://github.com/lsst
.. _LDM-294: https://ls.st/LDM-294

.. _ccd-drafting:

Drafting workflow
=================

Write change-controlled documents using :doc:`DM's standard workflow <../processes/workflow>`.
That is:

1. Create a ticket branch from ``master``.
2. Work on the ticket branch.
3. Have the ticket peer-reviewed.
4. Rebase and merge the ticket branch to ``master``.

Merging to ``master`` does not denote acceptance by a CCB.
Instead, it adds to the changeset that will be included in the next CCB review (see next).

.. _ccd-release:

Releasing a new version from the master branch
==============================================

Follow these steps to submit a document to the CCB and release a new baselined version:

1. Check out the head of the ``master`` branch and follow the procedure in :ref:`ccd-docushare-upload`.

   You can get the PDF for the DocuShare upload either by building the document locally or downloading it from the document's landing page at ``https://<handle>.lsst.io/v/master``.

2. Submit a request to the CCB.
   The procedure depends on the CCB:

   - For project documents (such as ``LPM``, ``LSE``), create an `LCR <https://project.lsst.org/groups/ccb/>`_ with a pointer to the new document version in DocuShare.
   - For DM documents (``LDM``), create an :ref:`RFC <decision-making-rfc-creating>` with a pointer to the new document in DocuShare.
     Set the JIRA state to "flagged" to notify the DM CCB.

3. Create a release branch based off the same commit as the DocuShare tag:

   - For a project document:

     .. code-block:: bash

        git checkout -b tickets/LCR-<N>
        git push -u

   - For a DM document:

     .. code-block:: bash

        git checkout -b tickets/RFC-<N>
        git push -u

   Replace ``<N>`` with the LCR or RFC number.

4. When the CCB responds, they may ask for changes.
   For minor and straightforward changes, you may commit changes to the release branch.
   For more complex changes, or when multiple people  are working in parallel to address requests, use a ticket branch-based workflow instead.
   Create the ticket branch from the head of the release branch and merge back to the release branch.

   When issues are addressed, notify the CCB:

   - For a project document, :ref:`create a new DocuShare upload <ccd-docushare-upload>` and notify the CCB.

   - For a DM document, create a comment on the RFC confirming the changes and link to the ``https://<handle>.lsst.io/v/RFC-<n>`` landing page for the release branch.
     You don't need to create intermediate DocuShare versions for the DM CCB.

   Repeat this step for each round of CCB feedback.

5. When the CCB approves document you create a release:

   1. Make two commits to the head of the release branch.
      In the first commit:

      - Update `document's change record <https://lsst-texmf.lsst.io/lsstdoc.html#document-preamble>`_.
        The Project librarian or DM release manager, through the CCB, determines the document's semantic version.
      
      In the second commit:

      - Remove the ``lsstdraft`` option from the document class.
      - Set the ``\date`` command using a YYYY-MM-DD format.

   2. :ref:`Create a new DocuShare upload <ccd-docushare-upload>`.
      At this stage, the Project librarian will review the change record's content (for project documents).
      If changes are needed, repeat the previous step and this one.

   3. Once the Project librarian or DM documentalist has uploaded the document and made it the new preferred version, create a :ref:`semantic version tag <ccd-semantic-tag>` at the same commit as the DocuShare tag:

      .. code-block:: bash

         git tag -a v<major>.<minor>
         git push --tags

      In your command, replace ``<major>.<minor>`` with the semantic version.

      Format the Git tag message as:

      .. code-block:: text

         v<major.minor>

         https://docushare.lsst.org/docushare/dsweb/Get/Version-<...>

      The URL should point to the DocuShare version (same as the DocuShare tag).

   4. Backport the amendment commits made on the release branch back to the ``master`` branch:

      1. Create a user branch from the ``master`` branch:

         .. code-block:: bash

            git checkout master
            git checkout -b u/<username>/v<major>.<minor>-backport

      2. Cherry-pick commits from the release branch onto the new backport branch.
         For example:

         .. code-block:: bash

            git cherry-pick <commit-sha>
         
         **Do not** backport the commit that removed the ``lsstdraft`` option and set the ``\date``.

      3. Push the backport branch to GitHub for continuous integration validation, rebase, and merge to master.
         For example:

         .. code-block:: bash

            git checkout master
            git pull
            git checkout u/<username>/v<major>.<minor>-backport
            git rebase -i master
            git push -u  # --force
            git checkout master
            git merge --no-ff u/<username>/v<major>.<minor>-backport
            git push

.. _ccd-hotfix:

Hotfixing a released document
=============================

The procedure above (:ref:`ccd-release`) describes how to make a new version of a document from the ``master`` branch.
Sometimes it is necessary to hotfix a released document to fix a typo or make a similar minor change.
In these cases you may not want to make a new release from the ``master`` branch because ``master`` has substantive, and unrelated, new content.
Instead, you may hotfix a document from the release branch.

.. note::

   If no changes have been merged to ``master`` since the document was released, you can follow the regular procedure for :ref:`ccd-release`.

Follow these steps to hotfix a document:

1. Check out the head of the release branch for the version being fixed:

   - For a project document:

     .. code-block:: bash

        git checkout tickets/LCR-<prev>

   - For a DM document:

     .. code-block:: bash

        git checkout tickets/RFC-<prev>

   ``<prev>`` is the RFC or LCR number of the document release being fixed.

2. Create a ticket branch (the JIRA ticket is scoped for implementing the fix and coordinating the release):

   .. code-block:: bash

      git checkout -b tickets/DM-<N>
      git push -u

3. Commit fixes onto that ``tickets/DM-<N>`` branch and push to GitHub.

4. Follow the steps in :ref:`ccd-release`, noting that the base branch is now ``tickets/DM-<N>``, not ``master``.
   In the last step, the amendment commits (such as those on the ``tickets/DM-<N>`` branch and on the release branch) are still backported to ``master``.
   The hotfix release branch is not merged onto the previous release branch.

.. _ccd-docushare-upload:

Uploading to DocuShare
======================

Follow these steps to upload a draft or released document to DocuShare:

1. Send the PDF of the document to a person able to upload to DocuShare:

   - For project documents (such as LPM and LSE), email the PDF to the LSST librarian.

   - For DM documents (LDM), email the PDF to a DM documentalist.

2. Wait for the documentalist or librarian to upload the document and verify that it appears on the Version page of the document on DocuShare.
   You can find the document version page with the short link ``https://ls.st/<handle>*``.
   For example, `https://ls.st/ldm-151* <https://ls.st/ldm-151*>`_.

3. Tag the commit that produced the DocuShare upload.
   This tag is formatted as ``docushare-v<N>`` where ``<N>`` is the version number for that document’s handle.
   This is the number of the upload shown on the document’s DocuShare version page (see note).

   .. code-block:: bash

      git tag -a docushare-v<N>
      git push --tags

   Format the Git tag message as:

   .. code-block:: text

      DocuShare v<N>

      https://docushare.lsst.org/<version-URL>

   The version URL in the commit message is the URL of that version in DocuShare (see note).

.. note::

   The number ``<N>`` in the ``docushare-v<N>`` tag is the number that appears in the **Version** column of the document’s version page.
   You can get to a document’s version page using the ``*`` shortlink (for example `https://ls.st/LDM-151* <https://ls.st/LDM-151*>`__).

   The version URL used in the body of the tag message is the URL that the version number links to on the document’s version page.

.. seealso::

   :ref:`ccd-docushare-tag` (API reference).

.. _ccd-git-api:

Summary of the Git tag and branch API
=====================================

In the change-controlled documentation Git workflow, branches and tags form an API that is used by DM's infrastructure to automate documentation management.
This section summarizes the intents of each type of branch and tag.

.. _ccd-docushare-tag:

DocuShare tags
--------------

DocuShare tags are formatted as ``docushare-v<N>`` where ``<N>`` corresponds to a document version number in DocuShare.
DocuShare version numbers increment by one each time a new version of a document for a given handle is uploaded to DocuShare.
Note that DocuShare version numbers are distinct from :ref:`semantic version numbers <ccd-semantic-tag>`.

See :ref:`ccd-docushare-upload` for details on how the tag is made.

.. _ccd-semantic-tag:

Semantic version tags
---------------------

Semantic version tags are formatted as ``v<major>.<minor>``.
The meanings of semantic document versions are described in `LPM-51`_.

Semantic versions are determined when the CCB baselines a document.
For project documents, the LSST project librarian determines the version number.
For DM documents, the DM release manager determines the version.

By definition, for each semantic version tag there is always a corresponding :ref:`DocuShare tag <ccd-docushare-tag>` at the same commit.

On LSST the Docs, the default version of a document shown at the root URL (for example, https://ldm-151.lsst.io) is always the most recent semantic version.

See :ref:`ccd-release` for details on how the tag is made.

.. _ccd-release-branch:

Release branches
----------------

Submissions to the DM CCB have an associated RFC and submission to the project CCB have an associated LCR.
Work related to a release is done on a release branch named after the RFC or LCR number: ``tickets/RFC-N`` or ``tickets/LCR-N``.
These release branches are never merged back to the ``master`` branch.
Instead, amendments are backported to ``master`` using :command:`git cherry-pick`.

Note that because creating an RFC or LCR requires a document in DocuShare, release branches are only created after the initial :ref:`DocuShare tag <ccd-docushare-tag>` is created.

.. _ccd-master-branch:

master branch
-------------

The ``master`` branch is the main development branch where individual ticket branches are integrated.
The document on the ``master`` branch is understood to be peer-reviewed but not baselined by the CCB.
