####################
Onboarding Checklist
####################

*Welcome to Data Management*.
This page gives you an overview of the accounts you'll have as a member of DM.

.. note::

   Some things you can set up yourself, but many accounts require action by your manager.
   We've given them a handy :ref:`onboarding-tcam-checklist` at the bottom.

.. _getting-started-lsst-account:

LSST account
============

Your manager — or T/CAM, in LSST jargon — will request a single sign-on account for you.
This gives you access to:

- The internal project website, including travel requests: http://project.lsst.org
- An e-mail address of the form ``username@lsst.org``:

  - AURA employees will be able to access the AURA e-mail system at https://mail.lsst.org/owa
  - For non-AURA employees, this will forward to your institutional address (as registered with the `Contacts Database <https://project.lsst.org/LSSTContacts/MemberListPage1.php>`_)

- The Jira project management tool: http://jira.lsstcorp.org/
- The Confluence wiki: https://confluence.lsstcorp.org
- The DocuShare document archive: https://docushare.lsst.org

  - The IT Team have some `further information about Docushare <https://confluence.lsstcorp.org/display/IT/Docushare>`_.
    Note in particular the comments on licensing.

You can always update or reset your LSST password at https://pwdreset.lsst.org/

Finally, read over the LSST Project's `New Employee Onboarding <https://project.lsst.org/onboarding>`_ page.
That will get you up to speed with the LSST Project; the rest of this page is specific to DM.

.. _getting-started-ncsa:

Data Facility resources
=======================

You'll also need an account for the LSST Data Facility services, hosted at NCSA, which include:

- Development Servers (`lsst-dev </services/lsst-login.html>`_)

This account will be automatically issued along with your LSST account.

.. _getting-started-github:

GitHub and LSST organizations
=============================

If you don't have one already, create an account on https://github.com.

Next, ask your T/CAM to add you to the `lsst <https://github.com/lsst>`__ and `lsst-dm <https://github.com/lsst>`__ GitHub organizations, along with any relevant team organizations (send your GitHub username to your T/CAM).

.. seealso::

   - :doc:`/git/setup` page for recommendations on setting up two-factor authentication and credential helpers for GitHub.
   - :doc:`/git/git-lfs` page for configuring Git LFS for DM.

Community.lsst.org
==================

https://community.lsst.org is LSST's public-facing discussion and support forum.
Browse the `forum-howto <https://community.lsst.org/tags/forum-howto>`_ tag to learn how to use the platform.

Create an account, and let your T/CAM know your username to get access to internal discussion categories.

Slack
=====

`Slack <https://slack.com/>`_ is LSST's real-time chat platform.
It is used across the project and by external science collaborations.
Please be aware of our guidance on :doc:`/communications/community-support` when interacting with the latter.

Ask your T/CAM for access to the ‘lsstc’ Slack team.
You can access it online at https://lsstc.slack.com, and through `Slack's mobile and desktop apps <https://get.slack.help/hc/en-us/articles/201746897-Slack-apps-for-computers-phones-tablets>`__.
Slack's `online help <https://get.slack.help/hc/en-us>`__ is a great way to learn Slack's features.

Be sure to :doc:`link your github profile to your slack account <../communications/slack-github-username>` so that our slack integrations will work correctly.

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
- `dm-tea-time <https://lsstc.slack.com/archives/dm-tea-time>`__ for more serious but still non-LSST conversation.
- `dm-admin-support <https://lsstc.slack.com/archives/dm-admin-support>`__ to contact DM's administrator.

Your team may also have specific channels, and you can send private messages to individuals.

Mailing lists
=============

We don't use mailing lists for conversations, but they're still used for notifications about :doc:`RFCs </communications/rfc>` and conversations happening on https://community.lsst.org.
You will automatically be be subscribed to these lists as soon as you get an :ref:`LSST acccount <getting-started-lsst-account>`:

- `dm-devel <https://lists.lsst.org/mailman/listinfo/dm-devel>`_
- `dm-announce <https://lists.lsst.org/mailman/listinfo/dm-announce>`_
- `dm-staff <https://lists.lsst.org/mailman/listinfo/dm-staff>`_ (internal list)

Calendars
=========

Important DM meetings are listed on `this Google Calendar <https://calendar.google.com/calendar/embed?src=pft8isslcqcll4jao0rqdmphvg%40group.calendar.google.com>`_, to which you may wish to subscribe.
More information is available about the various :ref:`calendars` which are available.

Checklist for hires
===================

In summary, here are the things you can do to get started:

#. Send a profile photo to your T/CAM for our `team page <https://confluence.lsstcorp.org/display/DM/The+Team>`__.

#. Send your GitHub username to your T/CAM.

#. Send your https://community.lsst.org username to your T/CAM.

#. Follow emailed directions to set up your LSST account (including email), NCSA account, and Slack account.

Further steps
-------------

While you're waiting on your accounts, here are some additional steps to help smooth your entry into the Rubin Observatory software team:

* Familiarize yourself with :doc:`our code of conduct <../team/code-of-conduct>`.
* Read :ref:`these tips <slack-summary>` on using our large slack.
* Configure :doc:`your editor <../editors/index>` to better integrate with the Science Pipelines workflow.
* Check out our :doc:`coding style guides <../coding/intro>`; our python style is mostly enforced by flake8 as a Github Action.
* Ensure your :doc:`git and GitHub configuration <../git/setup>` uses your :ref:`institutional email address <git-setup-institutional-email>`, and is tuned to :ref:`help your development process <git-shell-setup>`.
* Begin becoming familiar with our :doc:`development workflow <../work/flow>`: this will be an ongoing process as you work with other DM developers.
* Browse this guide's sidebar and use the search box: we've tried to provide guidance to help ensure consistent code quality and help you work within this large collaboration.

.. _onboarding-tcam-checklist:

Checklist for T/CAMs
====================

Onboarding
----------

Here's what T/CAMs need to do to get their new hire started:

#. Fill out the `Project onboarding form <https://project.lsst.org/onboarding/form>`__.

   - There's no need to upload a photo to DocuShare, see the next step instead.
   - Under "User should belong to which Mailing Lists," add ``dm-devel`` and ``dm-announce``. IT automatically adds DM hires to ``dm-staff``.

#. Ask your new hire for a profile photo and add it to https://confluence.lsstcorp.org/display/DM/The+Team.

#. Add the new hire to the DM Team Google spreadsheet with time allocation information.

#. Add the hire as a member of the 'Data Management' team in each these GitHub organizations:

   - `github.com/lsst <https://github.com/orgs/lsst/teams/data-management>`__.
   - `github.com/lsst-dm <https://github.com/orgs/lsst-dm/teams/data-management>`__.

#. Add the hire as a member of these Community forum groups:

   - `LSST <https://community.lsst.org/groups/LSST>`__.
   - `LSSTDM <https://community.lsst.org/groups/LSSTDM>`__.

#. Give the hire's email address to a Slack administrator: `@brianv0 <https://lsstc.slack.com/team/brianv0>`__, `@jonathansick <https://lsstc.slack.com/team/jonathansick>`__, and `@frossie <https://lsstc.slack.com/team/frossie>`__, can make Slack accounts.

Your new hire should automatically be issued a Data Facility (NCSA) account along with their LSST account.
However, if for some reason this doesn't happen, send the following information to ``lsst-account _at_ ncsa.illinois.edu`` (and CC ``lsst-sysadmins _at_ lsst.org``):

- First and last name of new hire
- Email
- Sponsoring LSST manager (ie, your name)
- Team within DM (one of DM Science, Architecture, Alert Production, Data Release Production, SUIT, Data Access and Database, Data Factility, Long Haul Networks, SQuaRE)

Departing
---------

When a member of your staff leaves the project, they can end up in one of two
states:

Offboarded

   An offboarded member of staff loses access to all LSST services.
   They retain builder status if they have accrued enough time with the project.
   To transition a member of staff to this status, fill out the `offboarding form <https://project.lsst.org/onboarding/offboarding_form>`_ and ensure they are set to 0% contribution in the `team spreadsheet <https://docs.google.com/spreadsheets/d/1f_dijhaSBjOvNyGPlPgIFWjjZpo_jwii_a0j7imq2CM/edit>`_.

Friendly

   “Friendly” individuals are no longer on the LSST payroll, but continue to collaborate with the project.
   As such, they retain access to services such as Jira, Confluence, etc.
   However, they will be removed from the ``dm-staff`` mailing list.
   Do *not* fill out an offboarding form for friendlies.
   Instead, simply set their contribution to 0% in the `spreadsheet <https://docs.google.com/spreadsheets/d/1f_dijhaSBjOvNyGPlPgIFWjjZpo_jwii_a0j7imq2CM/edit>`_ and send an e-mail to the DM Admin to let her know.
   Refer to `Document-27073 <http://ls.st/Document-27073>`_ for more information on friendly status.

In addition, the LSST Communications Team request that you notify the `dm-staff <https://lists.lsst.org/mailman/listinfo/dm-staff>`_ mailing list of any departures from your team following the template in `Document-26947 <http://ls.st/Document-26947>`_.

.. _onboarding-admin-checklist:

Checklist for the DM Admin
==========================

Here's what the awesome DM admin does:

#. After the onboarding form is received, send a welcome email to the hire with bullet points about the travel profile, Google calendar access, ContactDB info, and other miscellaneous project into. CC this to the supervisor.

#. Add a photo to the DM staff gallery, if not already done by the T/CAM.

#. Notify the LSST Digest editor and travel administrator.

#. Provide Google calendar access to DM Meetings and DM Travel/Vacation (for DMLT members only).

For details on LSST IT's account onboarding procedures, see `Account Management in the IT Support Confluence <https://confluence.lsstcorp.org/display/IT/Account+Management>`_.
