#################################################
Discussion and Decision Making Process (RFC, RFD)
#################################################

This page describes some of the formal processes we use in Data Management to make decisions.
Generally, DM teams and staff can implement non-controversial work (see § :ref:`decision-making-empowerment`).

For instances where you have a well-formed proposal that does not meet :ref:`our three-point criteria <decision-making-empowerment>` for independent implementation we use a :ref:`Request for Comments (RFC) <decision-making-rfc>` process.

You may also want to convene members across DM for an in-depth technical discussion.
The :ref:`Request for Discussion (RFD) <decision-making-rfd>` process facilitates DM-wide discussions in a weekly discussion time slot.

.. _decision-making-empowerment:

Empowerment
===========

You are empowered by the DM Project Manager (Jeff Kantor), Project Scientist (Mario Juric) and Project Engineer (Kian-Tat Lim) to make decisions on any DM-internal matter---such as technical/algorithm issues, process improvements, and tool choices---when:

1. you are willing and able to do the work to implement the decision yourself or with people who agree with you,
2. you (collectively) are willing and able to fix any problems if it goes wrong, and
3. you believe that all affected parties (including your immediate manager) would not seriously object to your decision and implementation.

.. _decision-making-rfc:

Request for Comments (RFC) Process
==================================

If the :ref:`above criteria <decision-making-empowerment>` are not met, perhaps because you don't know all the affected parties or because you don't know their positions, you should publish your proposed decision and implementation as an RFC-type issue in `JIRA RFC project <https://jira.lsstcorp.org/projects/RFC>`_.

RFCs are used to seek consensus on concrete plans that affect other parties.
It is usually difficult to determine all the affected parties for published package interfaces. Changes to interfaces should thus typically go through this process.

It's a good idea to contact any affected parties you *do* know about before starting this process to check that your resolution is sensible.
Your institutional technical manager is always affected, as she or he is responsible for tracking your work schedule.
If you are proposing work for others, they are obviously affected.
Your institutional scientist, the DM System Architect (K-T Lim), the Interface Scientist (Gregory Dubois-Felsmann), the Project Engineer (K-T Lim) and the Project Scientist (Mario Juric) are also valuable resources for determining affected parties.

The purpose of an RFC is to inform others about the existence and content of the proposed decision and implementation in order to allow them to evaluate its impact, comment on it, refine it if necessary, and agree (implicitly or explicitly) or object (explicitly) to its execution.

.. _decision-making-rfc-creating:

Creating an RFC
---------------

Create an RFC by making a JIRA issue in the `Request For Comments (RFC) <https://jira.lsstcorp.org/projects/RFC>`_ project with a component of "DM."
This will trigger postings to the `dm-devel mailing list <https://lists.lsst.org/mailman/listinfo/dm-devel>`_ and the `'Bot: RFC' HipChat room <hipchat://hipchat.com/room/1028779>`_.

.. _decision-making-rfc-medium:

RFC discussion medium
---------------------

The discussion of the RFC takes place in the medium of your choosing (typically this is the RFC issue itself, but other venues such as `community.lsst.org <http://community.lsst.org/c/dm>`_, a convened videocon, or an in-person meeting can be used instead).
You should be open to private communications as well.
Discussions should be summarized and persisted to the RFC issue or a `community.lsst.org topic <http://community.lsst.org/c/dm>`_.

.. _decision-making-rfc-consensus:

Role of the Assignee in reaching consensus
------------------------------------------

The Assignee of an RFC is the person in charge of seeing the proposal to implementation.
Typically the initial Assignee will be the issue Reporter.

In our RFC process, the opinions of those who will be doing the work (and fixing any problems if something goes wrong) are given more weight.
In some cases, this may mean that the RFC issue's Assignee passes to someone else.
The opinions of more senior people or people more experienced in the area should also be given more weight and may also result in the Assignee changing.

The Assignee is responsible for determining when no serious objections remain.
In particular, there is no need to call for a formal vote on the (refined) resolution.
If no explicit objections have been raised within, typically, 72 hours for "ordinary" issues and 1 week for "major" issues, the Assignee should assume that there are none.
This is known as "lazy consensus."

Be especially careful about not making irreversible changes in the "lazy consensus" time period unless you're absolutely certain there's a general agreement on the stated course of action.
If you break something, be ready to fix it.
Apply sound reasoning and good judgment about what may be acceptable and what might be not.
Mistakes will happen; accept that occasionally you will be requested to revert an action for which you thought agreement existed, and learn from the experience.

Part of the consensus-building process is a clear statement of what the implementation plan will be.
This implementation plan is translated into tickets in the :ref:`adoption phase <decision-making-rfc-adoption>`.

.. _decision-making-rfc-appeals:

Appeals process
---------------

If you can't converge on a resolution to an RFC that has no serious objections but you still feel that something must be done, you may request that the Project Manager, Project Scientist, and Project Engineer rule on it.
In most non-trivial cases, they will, with the advice of the Software Architect, empanel a group of experts to which they will delegate the right to make the decision, by voting if need be.

.. _decision-making-rfc-adoption:

Adopting an RFC
---------------

When consensus is established the Assignee should create a set of tickets that specify the implementation work, and then mark the RFC as **Adopted** in JIRA.

Use an **Is triggered by** JIRA linkage for these tickets that refers to the RFC.

.. _decision-making-rfc-implementation:

RFC implementation
------------------

An RFC considered 'implemented' once all tickets that have an **Is triggering** relationship from the RFC are marked as **Done**.

Once the RFC is implemented, return to the RFC's JIRA issue page and click the "We Shipped It!" button.
This changes the RFC's status from **Adopted** to **Implemented.**

.. _decision-making-rfc-tct:

RFCs that affect change-controlled documents
--------------------------------------------

Some proposed resolutions may require changes to one or more of the baselined, change-controlled documents describing the Data Management system (those in DocuShare_ with an LDM- handle or marked as change-controlled in Confluence).
Note that major changes to budget or scope will almost certainly affect one or more LDM- documents.
In this case only, the `DM Technical Control Team (TCT) <https://confluence.lsstcorp.org/display/DM/Technical+Control+Team>`_, consisting of the Project Manager, Project Scientist, Project Engineer, System Architect, and Interface Scientist, may empanel an ad hoc committee including the lead author of the document and other relevant experts.
This committee, or the TCT_ itself, must *explicitly* approve the change.
In the case of DM Coding Standards, which are change-controlled Confluence pages, the TCT_ has, via `RFC-24 <https://jira.lsstcorp.org/browse/RFC-24>`_, delegated all decision-making to the System Architect, who must explicitly approve any changes.

Change-controlled documents with other handles, such as LSE- or LPM-, including inter-subsystem interfaces, have project-wide change control processes.
Please consult the TCT_ for more information.

At least one member of the DM TCT_ will read each RFC to determine if it might affect a change-controlled document.

.. _decision-making-rfc-responsibility:

Responsibility and delegation
-----------------------------

For project management purposes, RFCs are formally proposals made to the Project Manager, Project Scientist and Project Engineer who by default are responsible for everything in DM (they "own" all problems).
As owners, they have the final word in accepting or rejecting all proposals.
Functionally, they delegate that ownership---the right and responsibility to make decisions---to others within the team (e.g. the System Architect, Interface Scientist, group leads, etc.) who are expected to delegate it even further.
Notifying your institutional technical manager about an RFC serves to inform the Project Manager.

.. _decision-making-rfd:

Request for Discussion (RFD) Process
====================================

.. See RFC-53: https://jira.lsstcorp.org/browse/RFC-53

Requests for Discussion (RFD) are intended to facilitate in-depth technical discussions across DM.
These might be:

- Detailed design discussions for a component of the system or its interfaces.
- Design reviews for new code or refactorings of old code.
- Brainstorming methods to solve difficult problems.
- "Brain dump" explanations of a design to share knowledge across DM.

.. _decision-making-rfd-creating:

Creating an RFD
---------------

Create an RFD by making a JIRA issue in the `Request For Comments (RFC) <https://jira.lsstcorp.org/projects/RFC>`_ project with a **component of DM** and a **issue type of RFD**.
Use the **Location** field to specify the date and time of the discussion (:ref:`see below for time slot <decision-making-rfd-time>`).
In the RFD's description:

- Summarize the issue, and indicate a desired outcome from the discussions.
- Include background material (using JIRA attachments, if necessary).
- Provide a link to the BlueJeans or Google Hangouts room.

Creating an RFD issue will trigger postings to the `dm-devel mailing list <https://lists.lsst.org/mailman/listinfo/dm-devel>`_ and the `'Bot: RFC' HipChat room <hipchat://hipchat.com/room/1028779>`_.

As the discussion organizer, you are responsible for ensuring all required attendees are available for the time slot.
DM members can comment on the RFD issue to indicate their availability, or whether the subject being discussed has already been resolved or covered elsewhere.

.. _decision-making-rfd-time:

The RFD time slot
-----------------

RFDs can scheduled for any convenient time, but we do have a weekly reserved time slot on Tuesdays from 12:30 to 2 PM Pacific.

If there are no requests 24 hours before a given time slot, the meeting will be canceled and the time freed up for other activities.

If there are conflicting claims to the RFD time slot, the Project Engineer (K-T Lim) will arbitrate.

.. _decision-making-rfd-followup:

RFD followup
------------

Tickets or RFCs that arise from an RFD should link back to the RFD issue on JIRA.

.. _TCT: https://confluence.lsstcorp.org/display/DM/Technical+Control+Team
.. _DocuShare: https://docushare.lsstcorp.org
