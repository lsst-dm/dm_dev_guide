######################################
Discussion and Decision Making Process
######################################

.. _decision-making-empowerment:

1. Empowerment
==============

You are empowered by the DM Project Manager (PM) and Project Scientist (PS) to make decisions on any DM-internal matter, including technical/algorithm issues, process improvements, tool choices, etc., when:

- you are willing and able to do the work to implement the decision yourself or with people who agree with you,
- you (collectively) are willing and able to fix any problems if it goes wrong, and
- you believe that all affected parties (including your immediate manager) would not seriously object to your decision and implementation.

.. _decision-making-rfc:

2. Request for Comments Process
===============================

If the above three criteria are not met, perhaps because you don't know all the affected parties or because you don't know their positions, you should publish your proposed decision and implementation as a JIRA issue in the `Request For Comments (RFC) <https://jira.lsstcorp.org/projects/RFC>`_ project with a component of "DM".
This will trigger postings to the `dm-devel mailing list <https://lists.lsst.org/mailman/listinfo/dm-devel>`_ and the `'Bot: RFC' HipChat room <hipchat://hipchat.com/room/1028779>`_.

It is usually difficult to determine all the affected parties for published package interfaces. Changes to interfaces should thus typically go through this process.

It's a good idea to contact any affected parties you *do* know about before starting this process to check that your resolution is sensible.
Your institutional technical manager is always affected, as she or he is responsible for tracking your work schedule.
If you are proposing work for others, they are obviously affected.
Your institutional scientist, the DM System Architect (SA, K-T Lim), the DM Interface Scientist (IS, Gregory Dubois-Felsmann), and the DM PS (Mario Juric) are also valuable resources for determining affected parties.

The purpose of an RFC is to inform others about the existence and content of the proposed decision and implementation in order to allow them to evaluate its impact, comment on it, refine it if necessary, and agree (implicitly or explicitly) or object (explicitly) to its execution.

The discussion of the RFC takes place in the medium of your choosing (e.g., a specific mailing list, the RFC JIRA issue itself, a HipChat room, a convened videocon, some combination of those, etc.), but you should be open to private communications as well.

In our RFC process, the opinions of those who will be doing the work (and fixing any problems if something goes wrong) are given more weight.
In some cases, this may mean that the RFC issue's Assignee passes to someone else.
The opinions of more senior people or people more experienced in the area should also be given more weight and may also result in the Assignee changing.

The Assignee is responsible for determining when no serious objections remain.
In particular, there is no need to call for a formal vote on the (refined) resolution.
If no explicit objections have been raised within, typically, 72 hours for "ordinary" issues and 1 week for "major" issues, the Assignee should assume that there are none.
This is known as "lazy consensus".
When this state has been reached, the Assignee is responsible for ensuring that the final consensus has been recorded in the RFC issue before closing it and proceeding with implementation of the decision.

Be especially careful about not making irreversible changes in the "lazy consensus" time period unless you're absolutely certain there's a general agreement on the stated course of action.
If you break something, be ready to fix it.
Apply sound reasoning and good judgement about what may be acceptable and what might be not. Mistakes will happen; accept that occasionally you will be requested to revert an action for which you thought agreement existed, and learn from the experience.

.. _decision-making-exceptions-appeals:

3. Exceptions and Appeals
=========================

Some proposed resolutions may require changes to one or more of the baselined, change-controlled documents describing the Data Management system (those in DocuShare with an LDM- handle or marked as change-controlled in Confluence).
Note that major changes to budget or scope will almost certainly affect one or more LDM- documents.
In this case only, the DM Technical Control Team (TCT), consisting of the DM PM, PS, SA, and IS, may empanel an ad hoc committee including the lead author of the document and other relevant experts.
This committee or the TCT itself must *explicitly* approve the change.
In the case of DM Coding Standards, which are change-controlled Confluence pages, the TCT has, via `RFC-24 <https://jira.lsstcorp.org/browse/RFC-24>`_, delegated all decision-making to the SA, who must explicitly approve any changes.

Change-controlled documents with other handles, such as LSE- or LPM-, including inter-subsystem interfaces, have project-wide change control processes.
Please consult the DM PM, SA, or IS for more information.

At least one member of the DM TCT will read each RFC to determine if it might affect a change-controlled document.

If you can't converge on a resolution to an RFC that has no serious objections but you still feel that something must be done, you may request that the DM PM and PS rule on it.
In most non-trivial cases, they will, with the advice of the SA, impanel a group of experts to which they will delegate the right to make the decision, by voting if need be.

.. _decision-making-formalities:

4. Formalities
==============

For project management purposes, RFCs are formally proposals made to the DM PM and PS who by default are responsible for everything in DM (they "own" all problems).
As owners, they have the final word in accepting or rejecting all proposals.
Functionally, they delegate that ownership---the right and responsibility to make decisions---to others within the team (e.g. the SA, IS, group leads, etc.) who are expected to delegate it even further.
Notifying your institutional technical manager about an RFC serves to inform the DM PM.
