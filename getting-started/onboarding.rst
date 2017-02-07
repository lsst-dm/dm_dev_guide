##############################
Developer Onboarding Checklist
##############################

*Welcome to Data Management*.
This page gives you an overview of the accounts you'll have as a member of DM.

.. note::

   Some things you can set up yourself, but many accounts require action by your manager.
   We've given them a handy :ref:`onboarding-tcam-checklist` at the bottom.

.. _getting-started-lsst-account:

LSST account
============

Your manager will request an LSST single sign-on account for you.
This gives you access to:

- The internal project website, including travel requests: http://project.lsst.org
- Email (for AURA employees): https://mail.lsst.org/owa
- The JIRA project management app: http://jira.lsstcorp.org/
- The Confluence wiki: https://confluence.lsstcorp.org
- The DocuShare document archive: http://docushare.lsstcorp.org

You can always update your LSST password at https://lsstsspc.lsst.org/.

Finally, read over the LSST Project's `New Employee Onboarding <https://project.lsst.org/onboarding>`_ page.
That will get you up to speed with the LSST Project; the rest of this page is specific to DM.

.. _getting-started-ncsa:

NCSA Resources
==================

You'll also need account(s) for the LSST infrastructures hosted at NCSA:

- Development Servers (`lsst-dev </services/lsst-dev.html>`_)
- MySQL Database (`lsst-db </services/lsst-db.html>`_)
- `Nebula OpenStack </services/nebula/index.html>`_

If you are missing any of these accounts, you can request one by sending the following to ``lsst-account _at_ ncsa.illinois.edu``:
- First and last name		
- Email		
- Sponsoring LSST manager		
- LSST-DM subteam or project

.. _getting-started-github:

GitHub and LSST organizations
=============================

If you don't have one already, create an account on https://github.com.

Next, ask your T/CAM to add you to the `lsst <https://github.com/lsst>`__ and `lsst-dm <https://github.com/lsst>`__ GitHub organizations, along with any relevant team organizations (send your GitHub username to your T/CAM).
   
.. seealso::

   - :doc:`/tools/git_setup` page for recommendations on setting up two-factor authentication and credential helpers for GitHub.
   - :doc:`/tools/git_lfs` page for configuring Git LFS for DM.

Community.lsst.org
==================

https://community.lsst.org is LSST's public-facing discussion and support forum.
Browse the `forum-howto <https://community.lsst.org/tags/forum-howto>`_ tag to learn how to use the platform.
   
Create an account, and let your T/CAM know your username to get access to internal discussion categories.

Slack
=====

`Slack <https://slack.com/>`_ is LSST's real-time chat platform.
It is used across the project and by external science collaborations.

Ask your T/CAM for access to the ‘lsstc’ Slack team.
You can access it online at https://lsstc.slack.com, and through `Slack's mobile and desktop apps <https://get.slack.help/hc/en-us/articles/201746897-Slack-apps-for-computers-phones-tablets>`__.
Slack's `online help <https://get.slack.help/hc/en-us>`__ is a great way to learn Slack's features.

Channels set up specifically for Data Management related discussion have a ‘dm-’ prefix.
Some important channels are:

- `announce-everyone <https://lsstc.slack.com/archives/announce-everyone>`__ for project-wide announcements.
- `lsst-travel <https://lsstc.slack.com/archives/lsst-travel>`__ for help with travel on project business.
- `lsst-newchannels <https://lsstc.slack.com/archives/lsst-newchannels>`__ for notifications of new channels.
- `software-dev <https://lsstc.slack.com/archives/software-dev>`__ for anything about writing software.
- `dm <https://lsstc.slack.com/archives/dm>`__ for general DM discussion.
- `dm-square <https://lsstc.slack.com/archives/dm-square>`__ for developer support services.
- `dm-jenkins <https://lsstc.slack.com/archives/dm-jenkins>`__ for automatic notifications from our Continuous Integration system.
- `dm-tavern <https://lsstc.slack.com/archives/dm-tavern>`__ for “water cooler” type talk.
- `dm-tea-time <https://lsstc.slack.com/archives/dm-tea-team>`__ for more serious but still non-LSST conversation.
- `dm-admin-support <https://lsstc.slack.com/archives/dm-admin-support>`__ to contact DM's administrator.

Your team may also have specific channels, and you can send private messages to individuals.

Google account for Hangouts
===========================

Many small meetings are conducted on `Google Hangouts <https://hangouts.google.com/>`_, which requires you to have an account with https://google.com.
The meeting convener will pass around a Hangouts room URL to attendees.

Mailing lists
=============

We don't use mailing lists for conversations, but they're still used for notifications about :ref:`RFCs <decision-making-rfc>` and conversations happening on https://community.lsst.org.
You should be subscribed to these lists as soon as you get an :ref:`LSST acccount <getting-started-lsst-account>`:

- `dm-devel <https://lists.lsst.org/mailman/listinfo/dm-devel>`_
- `dm-announce <https://lists.lsst.org/mailman/listinfo/dm-announce>`_
- `dm-staff <https://lists.lsst.org/mailman/listinfo/dm-staff>`_ (internal list)

DM calendars
============

DM maintains calendars of meetings and staff travel on Google.
To get access, send your Google username to our admin in `#dm-admin-support <https://lsstc.slack.com/archives/dm-admin-support>`__ on Slack.

Checklist for hires
===================

In summary, here are the things you can do to get started:

#. Send a profile photo to your T/CAM for our `team page <https://confluence.lsstcorp.org/display/DM/The+Team>`__.

#. Send your GitHub username to your T/CAM.

#. Send your https://community.lsst.org username to your T/CAM.

#. Follow emailed directions to set up your LSST account (including email), NCSA account, and Slack account.

#. Once you're on Slack, send your Google username to `#dm-admin-support <https://lsstc.slack.com/archives/dm-admin-support>`__ to access DM calendars.

.. _onboarding-tcam-checklist:

Checklist for T/CAMs
====================

Here's what T/CAMs need to do to get their new hire started:

#. Fill out the `Project onboarding form <https://project.lsst.org/onboarding/form>`__.

   - There's no need to upload a photo to DocuShare, see the next step instead.
   - Under "User should belong to which Mailing Lists," add ``dm-devel`` and ``dm-announce``. IT automatically adds DM hires to ``dm-staff``.

#. Add the new hire to the DM Team Google spreadsheet with time allocation information.

#. Ask your new hire for a profile photo and add it to https://confluence.lsstcorp.org/display/DM/The+Team.

#. Add the hire as a member of the 'Data Management' team in each these GitHub organizations:

   - `github.com/lsst <https://github.com/orgs/lsst/teams/data-management>`__.
   - `github.com/lsst-dm <https://github.com/orgs/lsst-dm/teams/data-management>`__.

#. Add the hire as a member of these Community forum groups:

   - `LSST <https://community.lsst.org/groups/LSST>`__.
   - `LSSTDM <https://community.lsst.org/groups/LSSTDM>`__.

#. Give the hire's email address to a Slack administrator: `@brianv0 <https://lsstc.slack.com/team/brianv0>`__, `@jonathansick <https://lsstc.slack.com/team/jonathansick>`__, and `@frossie <https://lsstc.slack.com/team/frossie>`__ can make Slack accounts.

.. _onboarding-admin-checklist:

Checklist for the DM Admin
==========================

Here's what the awesome DM admin does:

#. After the onboarding form is received, send a welcome email to the hire with bullet points about the travel profile, Google calendar access, ContactDB info, and other miscellaneous project into. CC this to the supervisor.

#. Add a photo to the DM staff gallery, if not already done by the T/CAM.

#. Notify the Weekly Digest editor and travel coordinator.

#. Provide Google calendar access to DM Meetings and DM Travel.

For details on LSST IT's account onboarding procedures, see `Account Management in the IT Support Confluence <https://confluence.lsstcorp.org/display/IT/Account+Management>`_.
