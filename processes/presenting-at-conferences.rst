#######################################
Attending and Presenting at Conferences
#######################################

This is our playbook for going to Project and public meetings, and presenting on behalf of DM.

.. seealso::

   Conference proceedings papers are coordinated by the LSST Project Publication Board.
   See :doc:`publication-policy` for more information.

.. _presenting-confluence-meeting-page:

Sign up for a meeting on Confluence (required)
==============================================

DM tracks meetings, along with who will attend them, at https://confluence.lsstcorp.org/display/DM/DM+Meetings.

If you're interesting in attending a meeting, add your name to the column "Expressed Interest in Attending."

Once your travel is approved (see :ref:`Travel requests <presenting-travel-requests>`), move your name to the "Attending" column.

.. _presenting-travel-requests:

Travel requests (required)
==========================

You'll need to fill out a *travel request* (TR) to travel to a meeting.
The TR both lets the project approve the expense and puts the Project travel coordinator to work on booking your itinerary.
Instructions for submitting TRs are at https://project.lsst.org/travel/travel-requests.

After your trip, you'll need to also fill out a *travel expense report* (TER).
Instructions for filing TERs are at https://project.lsst.org/travel/reimbursement.

.. _presenting-templates:

Slide templates (required)
==========================

If the meeting doesn't have a specific slide template, use the `Project's templates and stock slides <https://project.lsst.org/documents/stock-slides-templates>`__.

.. _presenting-key-numbers:

Key numbers and stock graphics (as needed)
==========================================

You must ensure that any LSST performance characteristics you state are consistent with the Project's `Key Numbers`_.
These numbers are rigorously vetted and maintained.

If you need visualizations or photos of the telescope, the Project `image and video gallery <https://www.lsst.org/gallery/image-gallery>`__ is also an excellent resource.

.. _Key Numbers: https://confluence.lsstcorp.org/display/LKB/LSST+Key+Numbers

.. _presenting-slack:

Slack during the meeting (optional)
===================================

You might want to create a dedicated Slack channel for the meeting you're attending.
Use this channel to coordinate with other on-site LSST folks and to live-blog for the rest of the team.
Here's how to make the channel:

1. `Create a channel <https://get.slack.help/hc/en-us/articles/201402297-Create-a-channel>`__ on https://lsstc.slack.com. Use a ``meetings-`` prefix for the channel name.
   For example: ``meetings-adass-2016``.
2. Announce the channel in `#lsst-newchannels <https://lsstc.slack.com/archives/lsst-newchannels>`__.
   You might want to also mention the channel in `#dm <https://lsstc.slack.com/archives/dm>`__ since `#lsst-newchannels <https://lsstc.slack.com/archives/lsst-newchannels>`__ is lightly followed.

.. _presenting-report:

Summarize the meeting on the Community forum (by request)
=========================================================

Once the meeting is over, it's a great idea to write down what happened.
This record helps the rest of the team benefit from your experience.

Policy on requesting a summary
------------------------------

Conference summaries are a great idea, but you're not required to write one.
DM team members can ask each other to write summaries of their meeting experience by writing a JIRA ticket and assigning it to the attendee.

How to write the summary
------------------------

Write your summary as a new topic in the `LSST Project <https://community.lsst.org/c/lsst-project>`__ category on the Community forum.
If multiple team members attended the same meeting, you can either collate your post beforehand, or post multiple replies within the same topic thread.

Tag your topic with ‘`conference-report <http://community.lsst.org/tags/conference-report>`_\ ’ so it's easy to find later.

Also add a link to your meeting report to https://confluence.lsstcorp.org/display/DM/DM+Meetings.

.. note::

   The `LSST Project <https://community.lsst.org/c/lsst-project>`__ forum category is only visible to LSST staff (including DM, but other Project subsystems too).
   This venue gives you license to frankly assess reaction from the community to LSST and other projects.

.. _presenting-proceedings:

Submit proceedings papers (required)
====================================

If you are writing a proceedings paper in conjunction with your presentation, you'll need to submit it to the LSST Publication Board before submitting it to the publisher.
See :doc:`publication-policy` for details.

After Publication Board approval, proceedings papers should be submitted to https://arXiv.org if the agreement with the publisher allows.
*We don't use Zenodo for proceedings.*

.. _presenting-zenodo:

Upload slides and posters to the LSST DM Zenodo Community (required)
====================================================================

DM collects conference presentation material (slide decks and posters, but **not** proceedings) in the `Large Synoptic Survey Telescope Data Management community on Zenodo <https://zenodo.org/communities/lsst-dm/>`__.
Zenodo archives and provides Digital Object Identifiers (DOIs) for scientific artifacts.
DOIs let you to robustly cite artifacts in scientific literature.

Uploading your material to Zenodo is a self-service process.
The instructions below will get you started.

.. _presenting-zenodo-upload:

Zenodo submission procedure
---------------------------

If you haven't already, create an account at https://zenodo.org.
You might want to log in with your existing `GitHub <https://github.com>`__ or `ORCiD <http://orcid.org>`__ accounts.

To start your upload, go to this dedicated page for LSST DM: https://zenodo.org/deposit/new?c=lsst-dm.

Next, fill out each relevant section of the submission page:

- **Files.** For presentations, include both the original source files (such as PowerPoint or Keynote documents) **and** an exported PDF version.

- **Upload type.** Typically choose **Presentation** or **Poster** for conference presentation material. If you have multiple types of artifacts from the same event it's best to submit each separately. Reach out to `#dm-docs <https://lsstc.slack.com/archives/dm-docs>`__ for advice.

- **Basic information.**

  - **Digital Object Identifier.** Usually you'll leave this blank. But if you want to include the DOI in your archived slide deck: click the 'Pre-Reserve DOI' button, add the reserved DOI to your artifacts, and then upload those artifacts.

  - **Publication date.** This is the day you presented or otherwise 'published' the material, not necessarily today's date.

  - **Title.** This should match your presentation's title in the meeting's agenda.

  - **Authors.**

  - **Description.** Use the abstract for your presentation. Don't include metadata about the conference here.

  - **Keywords.** Include ``lsst`` and any other keywords you see fit.

- **License.** Choose **Open Access** and the **Creative Commons Attribution 4.0** license unless you have extenuating circumstances. Reach out to `#dm-docs <https://lsstc.slack.com/archives/dm-docs>`__ for advice.

- **Communities.** Ensure that **Large Synoptic Survey Telescope Data Management** is included here (it's added by default by using the `DM upload page <https://zenodo.org/deposit/new?c=lsst-dm>`__). Your meeting might have also have a Zenodo community that you should add.

- **Related/alternate identifiers.** This is an optional section where you can connect your upload to other artifacts. For example, if presentation you're uploading to Zenodo is associated with a proceedings paper on `arXiv.org <https://arxiv.org>`__, you could provide the arXiv ID and say it "is a supplement to this upload." Use as many related identifiers as necessary. Again, reach out to `#dm-docs <https://lsstc.slack.com/archives/dm-docs>`__ for advice.

- **References.** You might choose to provide your reference list here, but it's not necessary.

- **Conference.** Include as much metadata about the conference or meeting as possible.

  - **Conference title.** Example: ``Astronomical Data Analysis Software and Systems XXVI``.

  - **Acronym.** Example: ``ADASS XXVI``.

  - **Dates.**

  - **Place.**

  - **Website.** Use the website of the meeting, not necessarily the organization. For example, use http://www.adass2016.inaf.it/index.php rather than http://www.adass.org.

  - **Session.**

  - **Part.**

Once all the metadata is filled in, click **Save** *and then* click **Publish.** In a moment, the DM community moderator will approve your submission and it'll appear at https://zenodo.org/communities/lsst-dm/.

.. note::

   You can always update metadata for your uploads by visiting https://zenodo.org/deposit.
   Also, keep in mind that *only you* can maintain the metadata for your uploads.
   If there's an issue, someone from DM may ask you to change a metadata field.
   However, you *can't* change the uploaded artifact itself.

.. _presenting-zenodo-sharing:

Link from the DM Meetings page (required)
-----------------------------------------

Once your slides are archived, link to them from the DM Meetings page, https://confluence.lsstcorp.org/display/DM/DM+Meetings.

Sharing your work (optional)
----------------------------

Some ideas:

- Add the URL of your presentation's Zenodo page to your :ref:`Community conference report <presenting-report>`.
  Discourse will helpfully embed a preview of your slides.
- Tweet the URL of your presentation's Zenodo page.
- Export a BibTeX citation for your slides from the presentation's Zenodo page.
