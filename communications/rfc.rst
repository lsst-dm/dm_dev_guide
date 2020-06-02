.. note::

   This page is based on :ldm:`294` Appendix C.

##########################
Request for comments (RFC)
##########################

By creating a **Request for comments (RFC)**, you can make a make a proposal to the Data Management subsystem, collect feedback, build consensus, adopt a course of action, and track a decision's implementation.

In general, DM team members are empowered by the DM Project Manager (PM) and DM Subsystem Scientist (SS) to make decisions on any DM-internal matter provided they meet the criteria listed in :doc:`/team/empowerment`.
For instances where those criteria aren't initially met, you should follow the steps here to create an RFC and generate a decision around your proposed action.

On this page:

- :ref:`rfc-jira`.
- :ref:`rfc-cases`.
- :ref:`rfc-discussion`.
- :ref:`rfc-exceptions`.
- :ref:`rfc-formalities`.

.. seealso::

   :doc:`rfd` has a similar name, but has to do with convening discussions across DM teams.

.. _rfc-jira:

Summary of the RFC workflow in JIRA
===================================

This section describes how DM RFCs are created and resolved.
See :ref:`rfc-discussion` for additional information about the process.

Create a new issue in JIRA
--------------------------

Create a new RFC by creating a new JIRA issue:

- Set the **Project** to **Request for Comments**.
- Set the **Issue Type** to **RFC**.
- Set the **Component** to **DM**.
- Give the RFC a descriptive **Summary**.
- Write the proposal in the issue's **Description** field.
  Usually it's a good idea to provide some brief background on why this proposal is being made.
  Ensure that you clearly state your actual, actionable, proposal.
- Set the **Assignee** to yourself (in typical cases).
- Set the **Planned End** to at least 72 hours in the future for ordinary issues or 1 week ahead for major issues.
- Add any relevant team members as **Watchers** (optional).

Once you click **Create**, the RFC will be posted to both the ``dm-devel mailing list`` and the `#dm`_ Slack channel.

RFC discussion and consensus
----------------------------

Members of DM should comment on the RFC by posting comments to the JIRA issue.

Refer to :ref:`rfc-discussion` for guidelines on discussion and consensus building within an RFC.

.. _rfc-escalating:

Escalating an RFC
-----------------

If the discussion is not converging, but you still feel that a decision must be taken, you (or the DMCCB) may escalate the RFC to be considered by the DM Change Control Board (DMCCB).
Click the **Escalate RFC** button on the RFC's JIRA issue page to do this; the RFC will be marked as **Flagged**.

Some types of RFCs are immediately flagged as a matter of routine: see :ref:`rfc-exceptions` for details.

Adopting an RFC
---------------

.. _rfc-triggering:

Triggering tickets
^^^^^^^^^^^^^^^^^^

Before an RFC may be adopted, one or more JIRA stories must be created in the regular DM project to capture the work required to implement the RFC's decision.

Those stories must have an **Is triggered by** relationship with the parent RFC issue.

.. _rfc-adopt-it:

Adoption in JIRA
^^^^^^^^^^^^^^^^

When

- the **Planned End** data has passed;
- the RFC is either in state **Proposed** (that is, it has not been :ref:`escalated <rfc-escalating>`) or **Board Recommended** (it has been escalated and subsequently approved);
- the assignee judges that positive consensus has been reached; and
- a set of :ref:`triggered tickets <rfc-triggering>` have been defined

the Assignee is responsible for adopting the RFC.

Do this by clicking the **Adopt RFC** button on the RFC's JIRA issue page.
JIRA will pop up a text box where you can confirm the adoption and add an optional text message.
This message will automatically appear in the `#dm`_ channel.

When you adopt an RFC, ensure that the resolution of the discussion is clearly stated, especially if the resolution is different from the proposal.

Next, see :ref:`rfc-implementing`.

.. _rfc-withdrawing:

Withdrawing an RFC
------------------

If the RFC *cannot* be adopted (by consensus, decision of the DM Change Control Board, or decision of the Assignee), then you can withdraw the RFC.
Click the **Withdraw** button on the RFC's JIRA issue page to do this.

.. _rfc-implementing:

Implementing an RFC
-------------------

After an RFC has been successfully adopted, it needs to be implemented.
An RFC is considered implemented once all JIRA issues linked as **Is triggering** from the RFC issue are marked as **Done**.

To then formally marked the RFC as implemented, click the **We shipped it!** button on the RFC's JIRA issue page.

.. _rfc-cases:

Standard procedures that require an RFC
=======================================

Some procedures **always require** an RFC, including:

- :doc:`/stack/adding-a-new-package`.
- :doc:`/stack/packaging-third-party-eups-dependencies`.
- :ref:`Releasing a change-controlled document <ccd-release>`.

.. _rfc-discussion:

Extended discussion of the RFC process
======================================

If the three criteria set in :doc:`/team/empowerment` are not met, perhaps because the team member doesn’t know all the affected parties or because they don’t know their positions, the team member should publish the proposed decision and implementation as a JIRA issue in the Request For Comments (RFC) project with a component of “DM.”
See :ref:`rfc-jira`.

It is usually difficult to determine all the affected parties for published package interfaces.
Changes to interfaces should thus typically go through this process.

It’s a good idea to contact any known affected parties before starting this process to check that the resolution is sensible.
The institutional technical manager is always affected, as she or he is responsible for tracking the work schedule. If work for others is being proposed, they are obviously affected.
The institutional scientist, the DM Software Architect (SA), the DM Interface Scientist (IS), and the DM Subsystem Scientist (SS) are also valuable resources for determining affected parties.

The purpose of an RFC is to inform others about the existence and content of the proposed decision and implementation in order to allow them to evaluate its impact, comment on it, refine it if necessary, and agree (implicitly or explicitly) or object (explicitly) to its execution.

The discussion of the RFC takes place in the medium of the requestor’s choosing (e.g., a specific mailing list, the RFC JIRA issue itself, a Slack Channel, a convened videocon, some combination of those, etc.), but the requestor should be open to private communications as well.

In the RFC process, the opinions of those who will be doing the work (and fixing any problems if something goes wrong) are given more weight.
In some cases, this may mean that the RFC issue’s Assignee passes to someone else.
The opinions of more senior people or people more experienced in the area should also be given more weight and may also result in the Assignee changing.

The Assignee is responsible for determining when no serious objections remain.
In particular, there is no need to call for a formal vote on the (refined) resolution.
If no explicit objections have been raised within, typically, 72 hours for “ordinary” issues and 1 week for “major” issues, the Assignee should assume that there are none.
This is known as “lazy consensus.”
When this state has been reached, the Assignee is responsible for ensuring that the final consensus has been recorded in the RFC issue before closing it and proceeding with implementation of the decision.

The requestor must be especially careful about not making irreversible changes in the “lazy consensus” time period unless they are absolutely certain there’s a general agreement on the stated course of action.
If something is broken, the requestor must be be ready to fix it.
It is critical to apply sound reasoning and good judgment about what may be acceptable and what might be not.
Mistakes will happen; accept that occasionally there will be a requirement to revert an action for which it was thought agreement existed.

.. _rfc-exceptions:

Exceptions and appeals
======================

Some proposed resolutions may require changes to one or more of the baselined, change-controlled documents describing the Data Management system (those in DocuShare with an LDM- handle or marked as change-controlled in Confluence). 
Note that major changes to budget or scope will almost certainly affect one or more LDM- documents.
In this case only, the DM Change Control Board (DMCCB) may empanel an ad hoc committee including the lead author of the document and other relevant experts.
This committee or the CCB itself must explicitly approve the change.

Change-controlled documents with other handles, such as LSE- or LPM-, including inter-subsystem interfaces, have project-wide change control processes.
Please consult the DM PM, SA, or IS for more information.
At least one member of the DM CCB will read each RFC to determine if it might affect a change-controlled document.

If the DM team can’t converge on a resolution to an RFC that has no serious objections but the requestor still feel that something must be done, the request will be escalated.
In most non-trivial cases, they will, with the advice of the SA, empanel a group of experts to which they will delegate the right to make the decision, by voting if need be.

If an RFC includes API changes, including deprecations, or updates to a data model such as the catalog schema generated by DRP, it must be approved by the DMCCB.

In all of these cases, the RFC is marked as **Flagged** to indicate that it is being considered by the DMCCB.

As a result of the discussion on a **Flagged** RFC, the DMCCB may decide to approve it and move forward with the proposal.
In this case, the RFC status is set to **Board Recommended**.
The assignee can then attach the triggering issues and adopt the RFC following the standard process.
During the discussion of a flagged RFC the DMCCB may ask for triggering issues to be created prior to its approval if there is some ambiguity as to the ramifications of said approval.

If the DMCCB does not approve the RFC, its status will be set to **Withdrawn**.
If the DMCCB declines to consider the RFC, the DMCCB will change the status back to **Proposed**.

All RFCs on DM controlled documents will be set directly to **Adopted** by the DMCCB, since they do not require implementation issues.

.. _rfc-formalities:

Formalities
===========

For project management purposes, RFCs are formally proposals made to the DM PM and PS who by default are responsible for everything in DM (they “own” all problems).
As owners, they have the final word in accepting or rejecting all proposals.
Functionally, they delegate that ownership, the right and responsibility to make decisions – to others within the team (e.g. the SA, IS, group leads, etc.) who are expected to delegate it even further.
Notifying the institutional technical manager about an RFC serves to inform the DM PM.

.. _`#dm`: https://lsstc.slack.com/messages/dm/
