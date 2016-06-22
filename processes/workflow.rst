##########################################################
DM Development Workflow with Git, GitHub, JIRA and Jenkins
##########################################################

This page describes our procedures for collaborating on LSST DM software and documentation with `Git <http://git-scm.org>`_, `GitHub <https://github.com>`_ and JIRA_:

1. :ref:`Configuring Git for DM development <git-setup>`.
2. :ref:`Using JIRA for agile development <workflow-jira>`.
3. :ref:`Policies for naming and using Git branches <git-branching>`.
4. :ref:`Preparing code for review <review-preparation>`.
5. :ref:`Reviewing and merging code <workflow-code-review>`.

In appendices, we suggest some *best practices* for maximizing the usefulness of our Git development history:

- :ref:`Commit organization best practices <git-commit-organization-best-practices>`.
- :ref:`Commit message best practices <git-commit-message-best-practices>`.

Other related pages:

- :doc:`/tools/git_setup`.
- :doc:`/tools/git_lfs`.
- :doc:`/tools/jira_tips`.

**For more hands-on overview of how the DM development workflow applies to LSST Stack development,** see the `Development Tutorial with lsstsw and lsst-build <http://pipelines.lsst.io/latest/developer/lsstsw_tutorial>`_ in the `Science Pipelines <http://pipelines.lsst.io>`_ documentation.

.. _git-setup:

Git & GitHub Setup
==================

You need to install Git version 1.8.2, or later, and the Git LFS client to work with our data repositories.
See the :doc:`DM Git LFS documentation </tools/git_lfs>` for more information on how to install and setup the Git LFS client for your machine.

We use Git commit authorship metadata to audit copyrights in DM code.
Ensure that Git is setup to use your *institution-hosted* email address (only AURA employees should use their ``lsst.org`` email addresses) in the :file:`~/.gitconfig` file.
You can do this from the command line:

.. code-block:: bash

   git config --global user.name "Your Name"
   git config --global user.email "your_email@institution.edu"

Likewise, in your `GitHub account email settings <https://github.com/settings/emails>`_, add your institution-hosted email.
We recommend that you set this institutional email as your **Primary GitHub** email address.
This step ensures that Git commits you make `directly on GitHub.com <https://help.github.com/articles/github-flow-in-the-browser/>`_ (such as quick documentation fixes) and merges made via the 'big green button' have proper authorship metadata.

*See also:* :doc:`/tools/git_setup`.

.. _workflow-jira:

Agile development with JIRA
===========================

We use JIRA_ to plan, coordinate and report our work.
Your Technical/Control Account Manager (T/CAM) is the best resource for JIRA usage within your local group.
T/CAMs can consult the `Technical/Control Account Manager Guide <https://confluence.lsstcorp.org/pages/viewpage.action?pageId=21397653>`_.
This section provides a high-level orientation for everyday DM development work.

*See also:* :doc:`/tools/jira_tips`.

.. _workflow-jira-concepts:

Agile concepts
--------------

Issue
   Issues are the fundamental units of work/planning information in JIRA.
Story Points
   Story points are how we estimate and account for time and effort.
   One story point is an idealized half day of uninterrupted work by a competent developer.
Velocity
   No developer works a two story point day.
   Communication overhead, review work, and other activities will invariably eat into your day.
   *Velocity* is the fraction of a story point that you can reasonably achieve in a half day.
   A common velocity in DM is 0.7, so that you nominally accomplish 1.4 story points in a day.
   We do not track velocities for individual developers; each DM group shares a common velocity.
   Ask your T/CAM.
Epic
   Epics are a special type of issue, created by T/CAMs, that guide your work over a six month **cycle** in pursuit of DM's development roadmap (`LDM-240 <http://ls.st/ldm-240>`_).
   At the start of each cycle, your T/CAM will create an epic (or several) and allocate *story points* to that epic.
   You don't work directly on an epic; rather you work on *stories* (below) that cumulatively accomplish the epic.

.. _workflow-jira-issues:

Tickets
-------

All development work is done on these three types of **JIRA issues** that are generically referred to as **tickets**:

Story
   Stories are issues associated with an epic.
   That is, stories are for work that accomplish your main goals for a cycle.
Bug
   A bug is an emergent (not planned with an epic) ticket that fixes a fault in the software that exists on ``master``.
   Bug tickets are not associated with an epic.
Enhancement
   An enhancement is essentially a feature request.
   Like a *bug*, an enhancement is emergent.
   Unlike a bug, an enhancement adds new functionality.
   Enhancements differ from stories in that they have no epic link.
   
.. note::
   Everywhere that it says "enhancement" it should say "improvement" - that is the actual ticket type.

Issue semantics were discussed in `RFC-43 <https://jira.lsstcorp.org/browse/RFC-43>`_.

As a developer, you can create tickets to work on.
You can also create bug or enhancement tickets and assign them to others (ideally with some consultation).

.. _workflow-jira-ticket-creation:

Creating a ticket
-----------------

You can create a ticket from the `JIRA web app <https://jira.lsstcorp.org>`_ toolbar using the **Create** button.
For more general information, you can consult the `LSST JIRA wiki <https://confluence.lsstcorp.org/display/JIRAatLSSTUserGuide/JIRA+at+LSST+User%27s+Guide+Home>`_ and `Atlassian's docs for JIRA <https://confluence.atlassian.com/jirasoftwarecloud/jira-software-documentation-764477791.html>`_ and `JIRA Agile <https://confluence.atlassian.com/agile067>`_.

JIRA allows a myriad of metadata to be specified when creating a ticket; these are the most relevant fields:

Project
   This should be set to **Data Management**, unless you are creating a ticket for a different LSST subsystem.
Issue Type
   If the work is associated with an epic, the issue type is a 'Story.'
   For emergent work, 'Bug' or 'Enhancement' can be used (see above for semantics).
Summary
   This is the ticket's title and should be written to help colleagues browsing JIRA dashboards.
Components
   You should choose from the pre-populated list of components to specify what part of the DM system the ticket relates to.
   If in doubt, ask your T/CAM.
Assignee
   Typically you will assign yourself (or your T/CAM will assign you) to a ticket.
   You can also assign tickets to others.
   If you are uncertain about who the assignee should be you can allow the ticket to be automatically assigned (which defaults to the component's T/CAM; `RFC-51 <https://jira.lsstcorp.org/browse/RFC-51>`_).
Description
   The description should provide a clear description of the deliverable that can serve as a definition of 'Done.'
   This will prevent scope creep in your implementation and the code review.
   For stories, you can outline your implementation design in this field.
   For bug reports, include any information needed to diagnose and reproduce the issue.
   Feel free to use `Atlassian markup syntax <https://jira.lsstcorp.org/secure/WikiRendererHelpAction.jspa?section=texteffects>`_. 
Story Points
   Use this field, at ticket creation time, to **estimate** the amount of effort involved to accomplish the work.
   Keep in mind how *velocity* (see above) converts story points into real-world days.
Labels
   Think of labels as tags that you can use to sort your personal work.
   Unlike the Component and Epic fields, you are free to create and use labels in any way you see fit.
Linked Issues
   You can express relationships between JIRA issues with this field.
   For example, work that implements an RFC should link to that RFC.
   You can also express dependencies to other work using a 'is Blocked by' relationship.
Epic Link
   If the ticket is a story, you must specify what epic it belongs to with this field.
   By definition, bug or enhancement-type tickets are not associated with an epic.
Team
   You must specify which DM team is doing the work with this field, for accounting purposes.
   The owner of the epic should be consistent with the team working on a ticket.

.. _workflow-jira-ticket-status:

Ticket status
-------------

Tickets are created with a status of **Todo.**

Once a ticket is being actively worked on you can upgrade the ticket's status to **In Progress.**

It's also possible that you may decide not to implement a ticket after all.
In that case, change the ticket's status to **Won't Fix.**

If you discover that a ticket duplicates another one, you can retire the duplicate ticket by marking it as **Invalid.**
Name the duplicate ticket in the status change comment field.

.. _git-branching:

DM Git Branching Policy
=======================

Rather than forking LSST's GitHub repositories, DM developers use a *shared repository model* by cloning repositories in the `lsst <https://github.com/lsst>`_, `lsst-dm <https://github.com/lsst>`_, and `lsst-sqre <https://github.com/lsst>`_ GitHub organizations.
Since the GitHub ``origin`` remotes are shared, it is essential that DM developers adhere to the following naming conventions for branches.

See `RFC-21 <https://jira.lsstcorp.org/browse/RFC-21>`_ for discussion.

.. _git-branch-integration:

The master branch
-----------------

``master`` is the main integration branch for our repositories.
The master branch should always be stable and deployable.
In some circumstances, a ``release`` integration branch may be used by the release manager.
Development is not done directly on the ``master`` branch, but instead on *ticket branches*.

Documentation edits and additions are the only scenarios where working directly on ``master`` and by-passing the code review process is permitted.
In most cases, documentation writing benefits from peer editing (code review) and *can* be done on a ticket branch.

The Git history of ``master`` **must never be re-written** with force pushes.

.. _git-branch-user:

User branches
-------------

You can do experimental, proof-of-concept work in 'user branches.'

These branches are named

.. code-block:: text

   u/{{username}}/{{topic}}

User branches can be pushed to GitHub to enable collaboration and communication.
Before offering unsolicited code review on your colleagues' user branches, remember that the work is intended to be an early prototype.

Developers can feel free to rebase and force push work to their personal user branches.

A user branch *cannot* be merged into master; it must be converted into a *ticket branch* first.

.. _git-branch-ticket:

Ticket branches
---------------

Ticket branches are associated with a JIRA ticket.
Only ticket branches can be merged into ``master``.
(In other words, developing on a ticket branch is the only way to record earned value for code development.)

If the JIRA ticket is named ``DM-NNNN``, then the ticket branch will be named

.. code-block:: text

   tickets/DM-NNNN

A ticket branch can be made by branching off an existing user branch.
This is a great way to formalize and shape experimental work into an LSST software contribution.

When code on a ticket branch is ready for review and merging, follow the :ref:`code review process documentation <workflow-code-review>`.

.. _git-branch-sims:

Simulations branches
--------------------

The LSST Simulations team uses a different branch naming scheme:

.. code-block:: text

   feature/SIM-NNN-{{feature-summary}}

.. _review-preparation:

Review Preparation
==================

When development on your ticket branch is complete, we use a standard process for reviewing and merging your work.
This section describes how to prepare your work for review.

.. _workflow-pushing:

Pushing code
------------

We recommend that you organize commits, improve commit messages, and ensure that your work is made against the latest commits on ``master`` with an `interactive rebase <https://help.github.com/articles/about-git-rebase/>`_.
A common pattern is:

.. code-block:: bash

   git checkout master
   git pull
   git checkout tickets/DM-NNNN
   git rebase -i master
   # interactive rebase
   git push --force

.. _workflow-testing:

Testing with Jenkins
--------------------

Use `Jenkins at ci.lsst.codes <https://ci.lsst.codes/job/stack-os-matrix/build?delay=0sec>`_ to run the Stack's tests with your ticket branch work.
To log into Jenkins, you'll use your GitHub credentials (your GitHub account needs to be a member of the `lsst <https://github.com/lsst>`_ organization).

Jenkins finds, builds, and tests your work according to the name of your ticket branch; Stack repositories lacking your ticket branch will fall back to ``master``.

.. figure:: /_static/development/jenkins_ci.png

   Jenkins test submission screen.
   In this example, the ``tickets/DM-9999`` branches of Stack repositories will be tested.
   If that branch doesn't exist, the ``tickets/DM-9998`` branch is be used.
   If neither of those branches exist for a given repository, the ``master`` branch is used.

You can monitor builds in the `Bot: Jenkins <https://lsst.hipchat.com/rooms/show/1648522>`_ HipChat room.
**If your build failed,** click on the **Console** link in the HipChat message to see a build log.

.. _workflow-pr:

Make a pull request
-------------------

On GitHub, `create a pull request <https://help.github.com/articles/creating-a-pull-request/>`_ for your ticket branch.

The pull request's name should be formatted as

.. code-block:: text

   DM-NNNN: {{JIRA Ticket Title}}

This helps you and other developers find the right pull request when browsing repositories on GitHub.

The pull request's description shouldn't be exhaustive; only include information that will help frame the review.
Background information should already be in the JIRA ticket description, commit messages, and code documentation.

.. _workflow-code-review:

DM Code Review and Merging Process
==================================

.. _workflow-review-purpose:

The scope and purpose of code review
------------------------------------

We review work before it is merged to ensure that code is maintainable and usable by someone other than the author.

- Is the code well commented, structured for clarity, and consistent with DM's code style?
- Is there adequate unit test coverage for the code?
- Is the documentation augmented or updated to be consistent with the code changes?
- Are the Git commits well organized and well annotated to help future developers understand the code development?

.. well- hyphenation? no http://english.stackexchange.com/a/65632

Code reviews should also address whether the code fulfills design and performance requirements.

Ideally the code review *should not be a design review.*
Before serious coding effort is committed to a ticket, the developer should either undertake an informal design review while creating the JIRA story, or more formally use the :abbr:`RFC (Request for Comment)` and :abbr:`RFD (Request for Discussion)` processes (see :doc:`/processes/decision_process`) for key design decisions.

.. TODO: link to RFC/RFC process doc

.. _workflow-review-assign:

Assign a reviewer
-----------------

On your ticket's JIRA page, use the **Workflow** button to switch the ticket's state to **In Review**.
JIRA will ask you to assign reviewers.

In your JIRA message requesting review, indicate how involved the review work will be ("quick" or "not quick").
The reviewer should promptly acknowledge the request, indicate whether they can do the review, and give a timeline for when they will be able to accomplish the request.
This allows the developer to seek an alternate reviewer if necessary.

Any team member in Data Management can review code; it is perfectly fine to draw reviewers from any segment of DM.
For major changes, it is good to choose someone more experienced than yourself.
For minor changes, it may be good to choose someone less experienced than yourself.
For large changes, more than one reviewer may be assigned, possibly split by area of the code.
In this case, establish in the review request what each reviewer is responsible for.

**Do not assign multiple reviewers as a way of finding someone to review your work more quickly.**
It is better to communicate directly with potential reviewers directly to ascertain their availability.

Code reviews performed by peers are useful for a number of reasons:

- Peers are a good proxy for maintainability.
- It's useful for everyone to be familiar with other parts of the system.
- Good practices can be spread; bad practices can be deprecated.

All developers are expected to make time to perform reviews.
The System Architect can intervene, however, if a developer is overburdened with review responsibility.

.. _workflow-code-review-process:

Code review discussion
----------------------

Code review discussion should happen on the GitHub pull request, with the reviewer giving a discussion summary and conclusive thumbs-up on the JIRA ticket.

GitHub pull requests are ideal venues for discussion since individual commit diffs can be annotated and referenced.
Be sure to make comments only from the **Conversation** and **Files changed** tabs---*not the Commits tab*.
Any comments on code patches from the Commits tab will be lost if the developer amends and force pushes commits to the pull request.

.. figure:: /_static/development/github_pr_comment_areas.png

   Pull request conversations should only happen in 'Conversation' and 'Files changed' tabs; your comments might get lost otherwise.

Code reviews are a collaborative check-and-improve process.
Reviewers do not hold absolute authority, nor can developers ignore the reviewer's suggestions.
The aim is to discuss, iterate, and improve the pull request until the work is ready to be deployed on ``master``.

If the review becomes stuck on a design decision, that aspect of the review can be elevated into an RFC to seek team-wide consensus.

If an issue is outside the ticket's scope, the reviewer should file a new ticket.

Once the iterative review process is complete, the reviewer should switch the JIRA ticket's state to **Reviewed**.
If there are multiple reviewers, our convention is that each review removes her/his name from the Reviewers list to indicate sign-off; the final reviewer switches the status to 'Reviewed.'
This indicates the ticket is ready to be merged.

Note that in many cases the reviewer will mark a ticket as **Reviewed** before seeing the requested changes implemented.
This convention is used when the review comments are non-controversial; the developer can simply implement the necessary changes and self-merge.
The reviewer does not need to be consulted for final approval in this case.

.. _workflow-code-review-merge:

Merging
-------

Putting a ticket in a **Reviewed** state gives the developer the go-ahead to merge the ticket branch.
If it has not been done already, the developer should rebase the ticket branch against the latest master.
During this rebase, we recommend squashing any fixup commits into the main commit implementing that feature.
Git commit history should not record the iterative improvements from code review.
If a rebase was required, a final check with Jenkins should be done.

We **always use non-fast forward merges** so that the merge point is marked in Git history, with the merge commit containing the ticket number:

.. code-block:: bash

   git checkout master
   git pull  # Sanity check; rebase ticket if master was updated.
   git merge --no-ff tickets/DM-NNNN
   git push

**GitHub pull request pages also offer a 'big green button' for merging a branch to master**.
We discourage you from using this button since there isn't a convenient way of knowing that the merged development history graph will be linear from GitHub's interface.
Rebasing the ticket branch against ``master`` and doing the non-fast forward merging on the command line is the safest workflow.

The ticket branch **should not** be deleted from the GitHub remote.

.. _workflow-announce:

Announce the change
-------------------

Once the merge has been completed, the developer should mark the JIRA ticket as **Done**.
If this ticket adds a significant feature or fixes a significant bug, it should be announced in the `DM Notifications category <https://community.lsst.org/c/dm/dm-notifications>`_ of community.lsst.org with tag `dm-dev <https://community.lsst.org/tags/dm-dev>`_.
In addition, if this update affects users, a short description of its effects from the user point of view should be prepared for the release notes that accompany each major release.
(Release notes are currently collected via team-specific procedures.)

.. _git-commit-organization-best-practices:

Appendix: Commit Organization Best Practices
============================================

Commits should represent discrete logical changes to the code
-------------------------------------------------------------

`OpenStack has an excellent discussion of commit best practices <https://wiki.openstack.org/wiki/GitCommitMessages#Structural_split_of_changes>`_; this is recommended reading for all DM developers.
This section summarizes those recommendations.

Commits on a ticket branch should be organized into discrete, self-contained units of change.
In general, we encourage you to err on the side of more granular commits; squashing a pull request into a single commit is an anti-pattern.
A good rule-of-thumb is that if your commit *summary* message needs to contain the word 'and,' there are too many things happening in that commit.

Associating commits to a single logical change makes debugging and code audits easier:

- Git bisect is more effective for zeroing in on the change that introduced a regression.
- Git blame is more helpful for explaining why a change was made.
- Better commit organization guides reviewers through your pull request, making for more effective code reviews.
- A bad commit can more easily be reverted later with fewer side-effects.

Some edits serve only to fix white space or code style issues in existing code.
Those whitespace and style fixes should be made in separate commits from new development.
Usually it makes sense to fix whitespace and style issues in code *before* embarking on new development (or rebase those fixes to the beginning of your ticket branch).

Rebase commits from code reviews rather than having 'review feedback' commits
-----------------------------------------------------------------------------

Code review will result in additional commits that address code style, documentation and implementation issues.
Authors should rebase (i.e., ``git rebase -i master``) their ticket branch to squash the post-review fixes to the pre-review commits.
The end-goal is that a pull request, when merged, should have a coherent development story and look as if the code was written correctly the first time.

There is *no need* to retain post-review commits in order to preserve code review discussions.
So long as comments are made in the 'Conversation' and 'Files changed' tabs of the pull request GitHub will preserve that content.  

.. _git-commit-message-best-practices:

Appendix: Commit Message Best Practices
=======================================

Generally you should write your commit messages in an editor, not at the prompt.
Reserve the ``git commit -m "messsage"`` pattern for 'work in progress' commits that will be rebased before code review.

We follow standard conventions for Git commit messages, which consist of a short summary line followed by body of discussion.
`Tim Pope wrote about commit message formatting <http://tbaggery.com/2008/04/19/a-note-about-git-commit-messages.html>`_.

.. _git-commit-message-summary:

Writing commit summary lines
----------------------------

**Messages start with a single-line summary of 50 characters or less**.
Consider 50 characters as a hard limit; your summary will be truncated in the  GitHub UI otherwise.
Write the message in the **imperative** tense, not the past tense.
For example, "Add feature ..." and "Fix issue ..." rather than "Added feature..." and "Fixed feature...."
Ensure the summary line contains the right keywords so that someone examining `a commit listing <https://github.com/lsst/afw/commits/master>`_ can understand what parts of the codebase are being changed.
For example, it is useful to prefix the commit summary with the area of code being addressed.

.. _git-commit-message-body:

Writing commit message body content
-----------------------------------

**The message body should be wrapped at 72 character line lengths**, and contain lists or paragraphs that explain the code changes. 
The commit message body describes:

- What the original issue was; the reader shouldn't have to look at JIRA to understand what prompted the code change.
- What the changes actually are and why they were made.
- What the limitations of the code are. This is especially useful for future debugging.

Git commit messages *are not* used to document the code and tell the reader how to use it.
Documentation belongs in code comments, docstrings and documentation files.

If the commit is trivial, a multi-line commit message may not be necessary.
Conversely, a long message might suggest that the :ref:`commit should be split <git-commit-organization-best-practices>`.
The code reviewer is responsible for giving feedback on the adequacy of commit messages.

The `OpenStack docs have excellent thoughts on writing great commit messages <https://wiki.openstack.org/wiki/GitCommitMessages#Information_in_commit_messages>`_.

.. _JIRA: https://jira.lsstcorp.org/
