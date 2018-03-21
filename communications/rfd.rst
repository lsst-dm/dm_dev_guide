.. See RFC-53: https://jira.lsstcorp.org/browse/RFC-53

############################
Request for discussion (RFD)
############################

By creating a **Request for Discussion (RFD)**, you can schedule an in-depth technical discussion across DM.
The types of discussions you might schedule include:

- Detailed design discussions for a component of the system or its interfaces.
- Design reviews for new code or refactorings of old code.
- Brainstorming methods to solve difficult problems.
- "Brain dump" explanations of a design to share knowledge across DM.

.. seealso::

   :doc:`rfc` is an additional process you should use to seek adoption of a specific proposal.

.. _rfd-creating:

Creating an RFD
===============

Create an RFD by `making a post`_ on Community in the  `DM RFD category`_.
A `template is provided in the post <https://community.lsst.org/new-topic?category=data%20management/dm%20rfd>`_ to allow you to suggest the date and time of the discussion (:ref:`see below for time slot <rfd-time>`), the medium for the discussion, and to specify the suggested audience.
In the RFD's description:

- Summarize the issue, and indicate a desired outcome from the discussions.
- Include background material (using attachments, if necessary).
- Provide a link to the BlueJeans room.

Creating an RFD post will trigger postings to the `dm-devel mailing list`_ and the `'#dm' Slack channel`_.

As the discussion organizer, you are responsible for ensuring all required attendees are available for the time slot.
DM members can comment on the RFD to indicate their availability, or whether the subject being discussed has already been resolved or covered elsewhere.

.. _`making a post`: https://community.lsst.org/new-topic?category=data%20management/dm%20rfd
.. _`DM RFD category`: https://community.lsst.org/c/dm/dm-rfd
.. _`dm-devel mailing list`: https://lists.lsst.org/mailman/listinfo/dm-devel
.. _`'#dm' Slack channel`: https://lsstc.slack.com/messages/dm/

.. _rfd-time:

The RFD time slot
=================

RFDs can be scheduled for any convenient time, but we do have a weekly reserved time slot on Tuesdays from 12:30 to 2 PM Pacific.

If there are no requests 24 hours before a given time slot, the meeting will be canceled and the time freed up for other activities.

If there are conflicting claims to the RFD time slot, the System Architect will arbitrate.

.. _rfd-followup:

RFD followup
============

Tickets or RFCs that arise from an RFD should link back to the RFD post on community.lsst.org and the Community post can be used to continue the discussion following the meeting.
