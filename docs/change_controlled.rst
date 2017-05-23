###################################
Writing Change-Controlled Documents
###################################

Change-controlled documents are documents that require approval from the Change Control Board (CCB) before they can be released.
The project-wide change control process is described in `LPM-19`_, with the process for managing documents being described in `LPM-51`_, and covers those documents using DocuShare handles "LSE" or "LPM", that must be approved by the Project `CCB`_.
For Data Management, these documents have the DocuShare handle "LDM" and they must be approved by the DM CCB using the :ref:`RFC <decision-making-rfc>` process.
These change-controlled documents can be written using the Word templates defined in `Document-9224`_, but the preference within Data Management is to write change-controlled documents in LaTeX using the ``lsstdoc`` document class provided by the `lsst-texmf`_ package, and to develop these documents using ``git`` repositories within the LSST organization on `GitHub`_.

.. _CCB: https://project.lsst.org/groups/ccb/
.. _Document-9224: https://ls.st/Document-9224
.. _lsst-texmf: https://lsst-texmf.lsst.io
.. _LPM-19: https://ls.st/LPM-19
.. _LPM-51: https://ls.st/LPM-51
.. _GitHub: https://github.com/lsst
.. _LDM-294: https://ls.st/LDM-294

.. note::
  The definition of which types of documents should be change-controlled is defined in `LDM-294`_.


Developer Workflow
==================

The development of change-controlled documents differs from :ref:`that of code <git-branching>`, in that some documents under development can take a long time to evolve and can be developed under multiple stories (ticket branches), and by multiple authors.
Repositories associated with change-controlled documents should therefore use two protected branches: ``master`` should correspond solely to an archived instance of the document on DocuShare, and ``draft`` is a development branch that should be used as the document evolves.
Ticket branches should branch from ``draft`` and should follow standard :ref:`DM branching policies <git-branching>`.

.. warning::
  Need to understand whether we need to handle two independent edits to an LDM that will be submitted as two distinct RFCs in parallel.

Once a document handle has been issued a repository can be created in the ``lsst`` GitHub organization using a repository name that matches the handle.
If the document exists in a pre-existing repository, it should be renamed to the handle and, if necessary, moved to the correct organization.

.. warning::
  It may be necessary to adjust the history of a pre-existing repository if it has been developed using different policies, in particular it is important that ``master`` be adjusted such that it only contains merge commits from approved versions (and the initial placeholder commit).

All documents use a Travis configuration file to build the document and deploy it to the corresponding https://ldm-nnn.lsst.io/ web site.
Built PDFs of documents should not be committed to the repository.
They are deployed automatically to the web during development and the final version will also be archived on DocuShare.

During development:

* Use the ``lsstdraft`` class option to make it clear that the document has not been approved.
* Specify a date using :code:`\today` so that the built document continues to have an updated date for each change (we do not automatically insert a date based on the state of the git repository).
* Update the change record but do not specify a version number.
  The version number will be added during the release process.
* New references should be added to a local :file:`ldm-nnn.bib` file and that file should be added to the bibliography search path.
* If the document is receiving minor edits consider using the :code:`\newtext` and :code:`\oldtext` macros to indicate text changes.
  For larger changes the :command:`latexdiff-vc` command may be helpful when preparing for an RFC or change request submission.

.. note::
  Should draft mode automatically override the release date?

When a document is ready to be reviewed by the CCB, it should be uploaded to DocuShare.
The review process is more efficient if the changes to be reviewed are marked clearly on the PDF.
If the CCB process triggers new modifications these should be made on a branch named ``tickets/RFC-nnn`` or ``tickets/LCR-nnn`` (relative to ``draft``) to make clear that the work was triggered by the review process.
Once the document change is approved the CCB shall nominate someone to prepare the document for release.
The release process for a document consists of (starting on the LCR/RFC ticket branch):

* Remove ``lsstdraft`` modifier and set the date to the approval date.
* Disable development notes (see below for alternate approach).
* Move references to the shared bibliography files in the ``lsst-texmf`` package.
  References should be added in the correct files and should be placed in the file based on alphabetical ordering of the keys.
  There should be no local bib file in a released document.
* Update the change record following the process described in `LPM-51`_.
  For LSE documents the change record should be approved by the LSST Librarian.
* Verify that the generated PDF (preferably one built and deployed by Travis) looks correct.
  LSE documents should be approved by the LSST Librarian at this point to ensure that the document is correct before the changes are merged to ``master``.
  The LSST Librarian will upload the document to DocuShare and close out the LCR.
* Merge the ticket branch to ``draft`` and the ``draft`` branch to master.
* For DM change-controlled documents upload the PDF to DocuShare and make it the preferred version.
  Update the RFC to indicate that it has been Implemented.
* Add a tag to the merge commit on ``master`` of the form ``docushare-vNN`` where ``NN`` corresponds to the DocuShare version of the document.

.. note::
  I think that we should use the LDM-151 scheme for hiding notes for released documents but trigger this on whether draft mode is enabled or not, rather than using a separate variable.
  We may want to distinguish document asides that should be included in the final released version of the document and asides that are used as development commentary.
