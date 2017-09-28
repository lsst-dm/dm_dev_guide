.. _writing-ccd:

#######################################
Writing change-controlled documentation
#######################################

Change-controlled documents are documents that require approval from a Change Control Board (CCB) before they can be released.
The project-wide change control process is described in `LPM-19`_, with the process for managing documents being described in `LPM-51`_, and covers those documents using DocuShare handles ``LSE`` or ``LPM`` that must be approved by the Project `CCB`_.
For Data Management, these documents have the DocuShare handle ``LDM`` and must be approved by the DM CCB using the :ref:`RFC <decision-making-rfc>` process.
The DM document management process is formally described in `LDM-294`_.

Change-controlled documents can be written using the Word templates defined in `Document-9224`_, but the preference within Data Management is to write change-controlled documents in LaTeX using the `lsstdoc document class`_ provided by the `lsst-texmf`_ package and to develop these documents using Git repositories within the LSST organization on GitHub (https://github.com/lsst).

This page describes the development and release processes of change-controlled documents produced by DM.

.. _CCB: https://project.lsst.org/groups/ccb/
.. _Document-9224: https://ls.st/Document-9224
.. _lsst-texmf: https://lsst-texmf.lsst.io
.. _lsstdoc document class: https://lsst-texmf.lsst.io/lsstdoc.html
.. _LPM-19: https://ls.st/LPM-19
.. _LPM-51: https://ls.st/LPM-51
.. _GitHub: https://github.com/lsst
.. _LDM-294: https://ls.st/LDM-294

.. _ccd-regular:

Regular development
===================

Develop change-controlled documents using :doc:`DM's standard workflow <../processes/workflow>`.
That is:

1. Create a ticket branch from ``master``.
2. Work on the ticket branch.
3. Have the ticket peer-reviewed.
4. Rebase and merge the ticket branch to ``master``.

Merging to ``master`` does not denote acceptance by a CCB.
Instead, it adds to the changeset that will be included in the next CCB review.

.. figure:: ccd-develop.svg
   :name: fig-ccd-develop
   :align: center
   :target: ccd-develop.svg
   :alt: Git commit tree showing two ticket branches merged to master.

   Example of Git branches during document development.
   Authors write and edit the document on individual ticket branches (``tickets/DM-1`` and ``tickets/DM-2``) that they merge to ``master``, following DM's regular :doc:`code workflow <../processes/workflow>`.

.. _ccd-submit:

Submitting a document to the CCB
================================

Establishing a new baselined version of the document begins with submitting it to the CCB.
The release manager is responsible for orchestrating this process.

1. Choose a commit on ``master`` where the document's content is ready for CCB review.
2. Create a :ref:`DocuShare tag <ccd-docushare-tag>` at the commit.
   DocuShare tags are formatted as ``docushare-vN``, where ``N`` is the next-available document version number in DocuShare.
3. Upload the PDF built by CI for the ``docushare-vN`` tag to DocuShare.
   By definition, this uploaded document should become version ``N`` in DocuShare.
4. For LDM documents, create a DM RFC.
   For project documents (LSE), create an LCR.
5. Once the RFC or LCR number is known, create a branch from the ``docushare-vN`` tag named ``tickets/RFC-N`` or ``tickets/LCR-N``.
   This :ref:`release branch <ccd-release-branch>` initially has no new commits on it.

.. figure:: ccd-submit.svg
   :name: fig-ccd-submit
   :align: center
   :target: ccd-submit.svg
   :alt: Git commit tree showing a docushare-v1 tag added to the head of the master branch.

   Example Git tree showing document submission to the CCB.
   The release manager creates a ``docushare-v1`` tag from the head of the ``master`` branch, since ``1`` is the next-available version number for the document in DocuShare.
   The release manager submits the PDF built from the ``docushare-v1`` tag to the CCB (as an RFC or an LCR).
   Finally, since the submission is ``RFC-1`` the release manager creates the ``tickets/RFC-1`` :ref:`release branch <ccd-release-branch>` from ``docushare-v1`` tag.

.. _ccd-edit:

Addressing CCB feedback
=======================

The CCB may request amendments before the document can be baselined.

1. Create a ticket branch from the ``tickets/RFC-N`` or ``tickets/LCR-N`` :ref:`release branch <ccd-release-branch>`.
2. Commit amendments to that ticket branch and peer review.
3. Rebase and merge the ticket branch onto the ``tickets/RFC-N`` or ``tickets/LCR-N`` :ref:`release branch <ccd-release-branch>`.
4. Multiple ticket branches can be created and merged to the :ref:`release branch <ccd-release-branch>` if the CCB's requests are being addressed by multiple authors working on separate parts of the document.
5. The release manager creates a new :ref:`DocuShare tag <ccd-docushare-tag>` (``docushare-vN``) from the head of the :ref:`release branch <ccd-release-branch>`, uploads the revised document to DocuShare, and notifies the CCB.

.. figure:: ccd-amend.svg
   :name: fig-amend
   :align: center
   :target: ccd-amend.svg
   :alt: Git commit tree showing amendments and resubmission to a CCB.

   Example Git tree showing how CCB feedback is addressed on a :ref:`release branch <ccd-release-branch>`.
   Two authors address CCB feedback by creating separate ticket branches (``tickets/DM-3`` and ``tickets/DM-4``) from the :ref:`release branch <ccd-release-branch>` (``tickets/RFC-1``) that are merged back to the ``tickets/RFC-1`` :ref:`release branch <ccd-release-branch>`.
   The release manager resubmits the amended document to the CCB by creating a :ref:`docushare tag <ccd-release-branch>` (``docushare-v2``) and uploading version 2 of the document to DocuShare.

.. _ccd-release:

Releasing a new baselined version of the document
=================================================

When the CCB baselines (accepts) the new document, the project librarian designates the baselined document with a semantic version.
The DM release manager is responsible for releasing a document.

1. From the head of the :ref:`release branch <ccd-release-branch>` (``tickets/RFC-N`` or ``tickets/LCR-N``), add a commit that:

	- Updates the semantic version of the document to the one designated by the project librarian.
	- Updates the change history table to reflect the new version.
	- Fixes the document's date to the date of baselining.
	- Removes the "draft" watermark (for example, by removing ``draft`` from the `document class's arguments <https://lsst-texmf.lsst.io/lsstdoc.html#document-preamble>`_).

2. Create a new :ref:`DocuShare tag <ccd-docushare-tag>` (``docushare-vN``) and upload the document to DocuShare.

3. Once the project librarian has set that DocuShare version as the preferred version, create a :ref:`semantic version tag <ccd-semantic-tag>` (formatted ``v<major>.<minor>``) at the same commit as the corresponding DocuShare tag.

4. Create a new ticket branch from the **head** of the ``master`` branch.
   Cherry pick amendment commits from the :ref:`release branch <ccd-release-branch>` onto that ticket branch.
   Also include a commit that updates the document change history table.
   Merge that ticket branch to ``master``.

**Notes:**

- The :ref:`release branch <ccd-release-branch>` is never merged back to ``master``.
  Amendments get back to ``master`` through cherry picking commits from the :ref:`release branch <ccd-release-branch>`.
- Development is allowed to happen on the ``master`` branch while CCB review is simultaneously happening on a :ref:`release branch <ccd-release-branch>`.
  This means that the DM release manager is responsible for properly addressing conflicts while cherry picking amendments back to ``master``.

.. figure:: ccd-release.svg
   :name: fig-release
   :align: center
   :target: ccd-release.svg
   :alt: Git commit tree showing a document release.

   Example Git tree showing how a document is released and baselined.
   The release manager creates a ticket branch (``tickets/DM-6``) from the current :ref:`release branch <ccd-release-branch>` (``tickets/RFC-1``).
   Commit ``D`` updates the document's history table.
   Commit ``E`` sets the document's version of removes the draft watermark.
   Once this ticket branch is merged to the :ref:`release branch <ccd-release-branch>`, the release manager uploads it to DocuShare (using a ``docushare-v3`` tag) and also tags the document's semantic version (``v1.0``).
   Finally, the release manager backports the amendment commits (``A``, ``B``, ``C``, and ``D`` --- but not ``E`` where the draft watermark was removed) to the ``master`` branch using a ticket branch (``tickets/DM-7``).

.. _ccd-hotfix:

Hotfixing a baselined document
==============================

It may be necessary to release a minor update to a baselined document (to fix typos, for example).
This is done by creating a branch based off the prior :ref:`release branch <ccd-release-branch>`.
Hotfixes cannot be made from ``master`` because significant edits may have been merged in the time since the document was baselined.

1. Create a ticket branch from the :ref:`semantic version tag <ccd-semantic-tag>` of the prior release.
2. Commit fixes to that ticket branch and have the changes peer reviewed.
3. Create a :ref:`DocuShare tag <ccd-docushare-tag>` (``docushare-vN``) and upload the document to DocuShare.
4. Create an RFC or LCR proposing the changes to the CCB.
5. Once the RFC or LCR number is known, create a new :ref:`release branch <ccd-release-branch>` (``tickets/RFC-N`` or ``tickets/LCR-N``) from the ``docushare-vN`` tag created in Step 3.
6. The remaining process of releasing this document, upon CCB approval, is the same as in :ref:`ccd-release`.

.. figure:: ccd-hotfix.svg
   :name: fig-hotfix
   :align: center
   :target: ccd-hotfix.svg
   :alt: Git commit tree showing a hotfix to a baselined document.

   Example Git tree showing how a baselined document is hotfixed.
   Since the fix is to the ``v1.0`` release, the author creates a ticket branch (``tickets/DM-8``) from the ``v1.0`` tag and commits the fix to it.
   Next, the release manager tags the fixed document as ``docushare-v4`` to upload a new DocuShare version and create a submission to the CCB.
   When the RFC number is known, the release manager creates a :ref:`release branch <ccd-release-branch>` from the ``v1.0`` tag (``tickets/RFC-2``) and merges the ``tickets/DM-8`` branch to the new :ref:`release branch <ccd-release-branch>`.
   When the CCB approves the fix, the release manager creates a ``tickets/DM-9`` branch to update the document's version history table and the document version and merges that ticket branch back to the ``tickets/RFC-2`` :ref:`release branch <ccd-release-branch>`.
   The release manager creates the ``docushare-v5`` tag to submit the finalized document to DocuShare and also tags the semantic version (``v1.1``).
   Finally, the release manager backports commits ``F`` and ``G`` with the fix and revised change history table back to the ``master`` branch.


.. _ccd-git-api:

Summary of the Git tag and branch API
=====================================

In the change-controlled documentation Git workflow, branches and tags form an API that is used by DM's infrastructure to automate documentation management.
This section summarizes the intents of each type of branch and tag.

.. _ccd-docushare-tag:

DocuShare tags
--------------

DocuShare tags are formatted as ``docushare-vN`` where ``N`` corresponds to a document version number in DocuShare.
DocuShare version numbers increment by one each time a new version of a document for a given handle is uploaded to DocuShare.
Note that DocuShare version numbers are distinct from :ref:`semantic version numbers <ccd-semantic-tag>`.

Since DocuShare version numbers are only created once a file is uploaded to DocuShare, we always create DocuShare tags for the next available available DocuShare version, and upload the corresponding PDF to DocuShare.
This procedure is illustrated in the following sequence:

1. The newest existing version of a document in DocuShare is version 5.
2. The release manager creates the tag ``docushare-v6`` and uploads the associated PDF built by a continuous integration system to DocuShare.
3. That upload becomes version 6.

.. _ccd-semantic-tag:

Semantic version tags
---------------------

Semantic version tags are formatted as ``v<major>.<minor>``.
The meanings of semantic document versions are described in `LPM-51`_.

Note that only the LSST project librarian can assign a semantic version to a released document.
This happens when the CCB baselines a document.
Thus the semantic version Git tag is applied when the librarian sets the preferred document version in DocuShare.

By definition, for each semantic version tag there is always a corresponding :ref:`DocuShare tag <ccd-docushare-tag>` at the same commit.

On LSST the Docs, the default version of a document shown at the root URL (for example, https://ldm-151.lsst.io) is always the most recent semantic version.

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
