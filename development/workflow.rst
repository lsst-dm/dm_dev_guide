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

.. _workflow-jira:

Agile development with JIRA
===========================

We use `JIRA <https://jira.lsstcorp.org>`_ to plan, coordinate and report our work.
Your Technical/Control Account Manager (T/CAM) is the best resource for JIRA usage within your local group.
T/CAMs can consult the `Technical/Control Account Manager Guide <https://confluence.lsstcorp.org/pages/viewpage.action?pageId=21397653>`_.
This section provides a high-level orientation for everyday DM development work.

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

Issue semantics were discussed in `RFC-43 <https://jira.lsstcorp.org/browse/RFC-43>`_.

As a developer, you can create tickets to work on.
You can also create bug or enhancement tickets and assign them to others (ideally with some consultation).

.. _workflow-jira-ticket-creation:

Creating a ticket
-----------------

You can create a ticket from the `JIRA web app <https://jira.lsstcorp.org>`_ toolbar using the **Create** button.
For more general information, you can consult the `LSST JIRA wiki <https://confluence.lsstcorp.org/display/JIRAatLSSTUserGuide/JIRA+at+LSST+User%27s+Guide+Home>`_ and Atlassian's docs for `JIRA <https://confluence.atlassian.com/jirasoftwarecloud/jira-software-documentation-764477791.html>`_ and `JIRA Agile <https://confluence.atlassian.com/agile067>`_.

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
