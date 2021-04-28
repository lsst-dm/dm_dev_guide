.. _slack-culture:

#############
Slack Culture
#############

Slack is Rubin Observatory's real-time chat platform.
It is used by project staff and science collaboration members, who can view and join all public channels.
Partnering users and projects may also be allowed to join specific channels as guests.
(Ask a Slack admin or ask in ``#help-slack`` if you need a guest added to a channel or want to share a channel with another project/organization.)

Teams may evolve different cultures around the use of Slack.
In addition, different types of channels may work in different ways.
This page documents the common, accepted Data Management culture, with specific adjustments for four types of channels: announcement, support, discussion, and informal.
But note that when it comes to communication, there are always exceptions, and culture can also change with time, deliberately or organically.

.. _slack-summary:

Summary
=======

- Use common emoji as reactions in place of messages. (:ref:`Details<slack-emoji-responses>`)

- Use text snippets or posts instead of long code or text blocks. (:ref:`Details<slack-snippets>`)

- Use threads for side conversations; suggest replies go to a thread with ``→``, ``-->``, or ``:thread:`` (🧵). (:ref:`Details<slack-general-threading>`)

- Use ``@channel``, ``@here``, and @-mentions of people sparingly, and be aware of timezones when mentioning people. (:ref:`Details<slack-general-mentions>`)

- In announcement channels, any non-announcements should be in threads. (:ref:`Details<slack-announcement-threading>`)

- In announcement channels, use @-mentions even more rarely. (:ref:`Details<slack-announcement-mentions>`)

- Follow documented procedures for providing community support to non-staff members. (:ref:`Details<slack-support-non-staff>`)

- In support channels, use threads to analyze and follow up on questions and problems. Consider moving detailed conversations to a team channel. (:ref:`Details<slack-support-threading>`)

- In support channels, use ``@here`` to announce urgent items and forestall questions for widespread issues. Use @-mentions to report solutions to the person who had a problem. (:ref:`Details<slack-support-mentions>`)

- Decisions in discussion channels must be formally recorded elsewhere. (:ref:`Details<slack-discussion-decisions>`)

- In discussion channels, be aware of the limitations of Slack's threads. (:ref:`Details<slack-discussion-threading>`)

- Follow Data Management's Focus Friday rules. (:ref:`Details<slack-focus-friday>`)

- Be professional and courteous in informal channels. (:ref:`Details<slack-informal-channels>`)

.. _slack-channel-types:

Channel Types
=============

Announcement channels are ones in which notices are posted, sometimes by automated "bots", and little or no response is anticipated.
These are often but not always indicated in the channel name with "announce" or "-status".

Support channels are ones in which users of a service, software package, or dataset interact with developers, primarily by asking questions and reporting problems.
These are often but not always indicated in the channel name with "-support", "-users", "-problems", "-ask", or "help-".

Informal channels are ones for interactions that are not at all or not directly work-related.
They are often location-specific or oriented towards particular interests or hobbies.

Discussion channels are all the rest: work-related discussions about particular topics.

We are looking into renaming channels to make their type more obvious.

.. _slack-general-practices:
 
General Practices
=================

.. _slack-emoji-responses:

Emoji responses
---------------

You can save space, time, and distractions to others by using commonly understood emoji instead of messages when semantically equivalent to your response.

- ``:heavy_plus_sign:`` (➕) = me too

-  ``:white_check_mark:`` (✅) or ``:heavy_check_mark:`` (✔︎) = this is correct

-  ``:+1:`` or ``:thumbsup:`` (👍) = OK

-  ``:thank_you:`` (🙏) or ``:thankyou:``

.. _slack-snippets:

Text snippets and posts
-----------------------

Slack has several ways to include blocks of text or code in a message.

- Inline code can be written using the backtick ````` character before and after or using the "code" button in the formatting bar.  This should typically be used for short (one or a few words) code elements embedded within normal text statements.

- Code blocks can be written using the triple-backtick ``````` before and after or using the "code block" button in the formatting bar.  This should typically be used for short (one to 10 lines) code blocks.

- Block quotes can be written using a ``>`` before each line or using the "blockquote" button in the formatting bar.  This should typically be used for short (one to 10 lines) text quotations from other messages or documents.

.. figure:: /_static/communications/slack-culture/format-bar.png
   :name: fig-slack-format-bar
   :alt: Slack formatting bar with inline code, code block, block quote buttons indicated

   Slack formatting bar.

- Entire messages can be shared from one place to another using the "Share message" button that appears when you hover over or select a message.

There are two less-known but very powerful features for code and text blocks.
Within the "lightning bolt" Shortcuts menu to the left of the :ref:`formatting bar <fig-slack-bolt-normal>` or the :ref:`message input area <fig-slack-bolt-advanced>`, there are entries for "Create a text snippet" and "Create a post".

.. figure:: /_static/communications/slack-culture/bolt-normal.png
   :name: fig-slack-bolt-normal
   :alt: Shortcut "lightning bolt" icon with the normal formatting bar

   Shortcut "lightning bolt" icon with the normal formatting bar.

.. figure:: /_static/communications/slack-culture/bolt-advanced.png
   :name: fig-slack-bolt-advanced
   :alt: Shortcut "lightning bolt" icon with the markup-only preference set

   Shortcut "lightning bolt" icon with the markup-only preference set.

.. figure:: /_static/communications/slack-culture/snippet-post.png
   :name: fig-slack-snippet-post
   :alt: Text snippet and post shortcuts

   Text snippet and post shortcuts.

A `text snippet`_ is a file, but it appears as a message attachment.
It can have a title (like a filename with extension).
Content will be monospaced, like code blocks, but lines are numbered, and syntax highlighting for a wide variety of languages can be applied, either automatically based on the filename's extension or manually chosen.
Whether the code should wrap when displayed or scroll horizontally can also be chosen.
Finally, and perhaps most importantly, long snippets are automatically displayed in "collapsed" form.
Readers can expand the snippet inline, view it in detail in a sidebar, or download it.
Instead of a large code block in a message that has to be scrolled around vertically, an expanded snippet can be collapsed again, taking up only a small amount of visible message space.
Like messages themselves, text snippets can be edited even after being sent.

.. _text snippet: https://slack.com/help/articles/204145658-Create-a-snippet

A `post`_ is also a file that appears as a (somewhat larger) message attachment.
Its title is more of a heading than a filename.
It can include normal text, which can be formatted in the same ways as messages, including triple-backtick code blocks.
Two levels of header formatting are also available.
There are two special things about posts: they can be made editable by other users (snippets are only editable by the original author), and they can be given public URLs to be shared outside of Slack (but only if the post is posted in a public channel).
When a post gets longer than about 48 lines, it will automatically display in "collapsed" form.

.. _post: https://slack.com/help/articles/203950418-Use-posts-in-Slack

Please use text snippets or posts for long segments of code, text, or error messages (e.g. more than 10 lines or so).

.. _slack-general-threading:

Threading
---------

Threads allow conversations to take place among a subset of the members of a channel.
They can branch off from any message at any time, and messages in a thread can also be shared with the main channel.
At times you may want to post several messages in sequence that don't all belong in the main channel, or you may anticipate follow-up conversation that only involves a few of the channel members.
In these cases, you can signal that replies (yours or others) to a message should be in a thread with either a rightward arrow (``→`` or ``-->``) or the ``:thread:`` (🧵) emoji.

There are more specifics on thread usage in certain types of channels below.

.. _slack-general-mentions:

@-mentions
----------

``@channel`` sends a notification to every member of a channel, even if they are in a meeting, away, or on vacation (unless they pause notifications).

The uncontroversial use of ``@channel`` is "This group of people has opted into this channel for a fairly narrow purpose, and they all really need a notification interrupt related to that purpose".
For example, it is appropriate to use ``@channel`` on a meeting-specific channel for a DM All-Hands meeting to say “Conference Photo has been moved to 4pm to try and beat the rain” because:

- It is time-sensitive, and the consequences of missing the message are severe.

- It is something everybody on the channel is reasonably expected to care about.

- It is reasonable to assume this is the kind of content people joined the channel for.

At the other end, for a large channel whose membership is organizational rather than voluntary, such as "all members of DM", it is rarely appropriate to use ``@channel``.
Consider whether the information is time-critical or a normal message could be used instead.
Consider whether the information is relevant to all (or the vast majority of) channel members or could be redirected to a narrower channel.
In particular, we have a specific opt-in ``#talk-starting-soon`` channel for timely reminders of talks or seminars that may be of wide interest but that do not deserve to interrupt everyone in a large channel.
Consider whether everyone who might be interested already keeps up on the channel as part of their daily/hourly routine, so no notification is required at all.

``@here`` is slightly narrower than ``@channel`` as it only notifies active channel members, not those who are away.
The same general considerations apply, however.

Slack has a concept of user groups that can be notified instead of an entire channel that has members outside that group.
If you can use such a group rather than ``@channel`` or ``@here``, that is preferred.
If you need to have a group created because you have a routine need to @-mention them, contact a Slack admin (e.g. via ``#help-slack``)

@-mentioning a particular user notifies that user and adds the message to their "Mentions & reactions" list.
Be aware of the person's timezone before @-mentioning them.
If you need to @-mention them outside normal hours, you may want to schedule the message to be posted later (using the ``/send`` or more sophisticated ``/schedule`` shortcuts from `Timy`_).
Sometimes @-mentioning a user can be helpful to disambiguate replies in a multi-person conversation, but if you find yourself prefixing every message you send with an @-mention, consider whether it is implied by context or whether the whole conversation might be better in a thread or in direct messages to that user.

.. _Timy: https://timy.website/#commands

There are more specifics on @-mention usage in certain types of channels below.


.. _slack-announcement-channels:

Announcement Channels
=====================

These channels include ``#general`` (for general discussions and postings to most of the people on Slack) and ``#announce-everyone`` (for essential announcements to everyone on Slack).

.. _slack-announcement-threading:

Threading
---------

To reserve the main channel for announcements, almost any question or reply should be in a thread.
If there is a clarification developed in a thread, that message can be shared back to the main channel.

.. _slack-announcement-mentions:

@-mentions
----------

Since these channels typically have wide membership, pay special attention to timeliness and relevance before using ``@channel`` or ``@here`` in them.


.. _slack-support-channels:

Support Channels
================

Often the relevant manager will review all messages in a support channel to ensure that no incidents or questions have been left unhandled.

.. _slack-support-non-staff:

Non-Staff Support
-----------------

The :doc:`Providing Support to the Community </communications/community-support>` page discusses how we are handling this type of support.
It refers to the `Interim Model for Community Support <https://dmtn-155.lsst.io/>`__ document.

.. _slack-support-threading:

Threading
---------

Support channels have special characteristics:

- Hard-to-follow information and distractions can impede developers trying to help users in an effective and timely manner.

- High-volume and especially interleaved main-channel traffic on concurrent issues makes it hard for the ad-hoc incident response coordinator to assess status.

- These channels are often monitored outside normal hours (sometimes as part of the job, sometimes on a best-effort volunteer basis).  Ongoing conversations on issues that are no longer urgent can have a disruptive effect.

As a result, these channels frequently use threads to separate conversations, even having one per incident.

Of course it is totally reasonable for conversation to start in the main channel, typically during the “is it broken or is it me” phase.
In this stage of a problem it is useful to have many eyes so people can go “me too” or offer peer-to-peer support for common problems, like “is your VPN on?”.

At some point, it becomes obvious that there is an actual problem and one or more developers and/or an incident coordinator need to work it.
This is an excellent time to move the conversation to a thread for a number of reasons:

- It clears the main channel for other problems or important updates

- It creates a huddle among people actively involved in the problem (devs and users) and so it reduces the “peanut gallery” effect.

- It keeps log dumps, sceenshots and other artifacts with a poor column-inches-to-general-interest ratio off the main channel.

- It reduces the impact of developers who favour “stream of consciousness” troubleshooting on everyone else.

- It vastly reduces potential misinformation during the troubleshooting phase (“ALL THE DATA IS GONE” followed by “never mind, I was logged onto the test server”).

In fact there can be a second level of “threading” where, once it because apparent what the issue is, developers can retreat to their team channel (which may still be public but with a narrower membership) to further discuss the issue and to avoid pummeling the user with speculation and technical details rather than specific questions and a solution.

Bottom line: please try and thread screendumps etc.; always follow the lead of the incident coordinator if they ask you to thread; and keep the main channel clear for important information and new problem threads.

Some channels are specifically for observing operations support.
While these channels are public, if you have not been assigned or requested to participate, you should remain a quiet "lurker".

.. _slack-support-mentions:

@-mentions
----------

Support channels are also special with regard to @-mentions.
As they generally include all users of a particular service, time-sensitive announcements to all of those users can deserve an ``@channel``.
In particular, when a widely used service is down, the team is often pummeled with notifications on every medium from users reporting a problem.
In such a situation an aggressive notification serves a wider purpose: stemming the flow.
The inconvenience to the people who are notified and didn’t know or care is offset by the benefit to the responding team of reduced noise.
But ``@here`` may be sufficient since people who are away are not likely to be affected by the service outage.
The incident response coordinator (often the team leader) should judge the situation.

If a problem affects only one person, however, an @-mention of that person is sufficient to report a solution.


.. _slack-discussion-channels:

Discussion Channels
===================

.. _slack-discussion-decisions:

Decisions
---------

In Data Management, discussions in Slack do not produce an authoritative record of decisions.
All decisions emerging from such discussions need to be formalized elsewhere, often an :doc:`RFC </communications/rfc>`, a :doc:`technical note </project-docs/technotes>`, or, at minimum, a `Confluence page <https://confluence.lsstcorp.org/>`__ or `Jira issue <https://jira.lsstcorp.org/>`__.

.. _slack-discussion-threading:

Threading
---------

Outside support channels, some of the disadvantages of Slack's threading model are more prominent.
For example, you can’t easily thread off a thread to generate a tertiary conversation.
"Taking it to another channel" instead can lose linkage to the original discussion; reporting conversation results back to the originating channel or at least pasting message links becomes more important.
If you’re reading a thread but not actively contributing to it, you need to explicitly “Follow thread” to get notifications.
This can be especially difficult if someone starts a thread off an older message as there’s no easy way of knowing that it even exists.

.. _slack-focus-friday:

Focus Friday
------------

Data Management observes :doc:`Focus Friday </team/focus-friday>`.
See that page for information on use of Slack versus asynchronous communications mechanisms on Fridays.
Do not use any @-mentions in a discussion channel on Focus Friday.


.. _slack-informal-channels:

Informal Channels
=================

While informal channels are not about work topics, you should still behave professionally and courteously within them, including exhibiting a welcoming attitude towards newcomers.
