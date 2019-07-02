#########################################
Project Planning for Software Development
#########################################

This page describes the project planning process used in DM for software
development. This process is a fusion of NSF and Federal mandates for Risk
and Earned Value Management and Project Planning with Agile Process. Our
nickname for this process is "Agile for Government".

Data Management Planning Process
================================

As LSST is now in Construction and funded under the NSF :abbr:`MREFC (Major
Research Equipment and Facilities Construction)` budget, the planning process
has become more formal than was the case in R&D. For the primary work plans
during Construction, the following process has been used.

.. figure:: /_static/development/planning_flowdown.jpg
   :name: fig-planning-flowdown

#. Using the flow-down of System Requirements (`LSE-30`_) to DM System
   Requirements (`LSE-61`_), LSST Program Schedules, LSST Operations plans, and a
   DM section of the `Risk & Opportunity Register`_ that assesses the perceived
   programmatic and technical risks, a set of time-phased software capabilities
   and key progress metrics for the DM System has been defined. The DM Roadmap
   (`LDM-240`_) "bins" these planned software capabilities and key progress
   metrics into "coarse-grained" 12-month periods. These activities encompass all
   major DM R&D work in all areas (DM System Management and Engineering,
   Applications, Middleware, Infrastructure).

   .. figure:: /_static/development/ldm_240_extract.jpg
      :name: fig-ldm-240-extract

#. In the LSST Project Management Control System (PMCS) the DM Project Manager
   creates and maintains software and data release and management/system
   engineering project plans that encompass the entire Roadmap and add the next
   level of detailed work planning. In addition, the plans cover activities
   specific to preparing and conducting formal reviews. The granularity of the
   release activities in this plan are 3 to 6 months each. Each activity includes
   the activity description, expected start and end dates, and resources
   assigned. Inter-activity dependencies are also captured to allow for critical
   path method scheduling and analysis. This plan is the "top-down" plan for the
   entire Construction phase. It is the basis for all LSST budgets and the
   Earned Value Management required by the MREFC process.

   .. figure:: /_static/development/pmcs_extract.jpg
      :name: fig-pmcs-extract

#. At the start of each 6-month period (aka each new Winter or Summer Release)
   each DM Cost Account Manager (T/CAM) interviews the institution team and
   creates a very detailed work plan, with individual activity granularity from 1
   to 3 months (see the `T/CAM Guide`_). Further, each activity is divided into
   steps of 2 - 20 days effort. This plan is known as a Release Plan. This
   process is done via the Agile Process, including backlog and sprint meetings,
   interactive communications, and design reviews. This process is accomplished
   in :doc:`JIRA Agile <jira-agile>`, outside the PMCS. Then plan is incorporated
   into the PMCS. Once work starts on the release, this level of plan is tracked
   on a weekly basis, and the status is rolled up to the PMCS (see DM Reporting
   Process below).

   The PMCS actually includes all activities to be performed during the current
   release period, even those that are not directly part of the data production
   and release (e.g. LSST and Agency Review activities, level of effort
   activities covering periodic meetings such as risk management meetings, etc.).
   While the plan includes both release and other activities, the plan is coded
   in PMCS so that those activities that are part of the data production and
   release can be easily identified in filtered views of the plan.

.. _LSE-30: http://ls.st/lse-30
.. _LSE-61: http://ls.st/lse-61
.. _Risk & Opportunity Register: https://www.lsstcorp.org/sweeneyroot/riskmanagement/risks_01.php
.. _LDM-240: http://ls.st/ldm-240
.. _T/CAM Guide: https://confluence.lsstcorp.org/pages/viewpage.action?pageId=21397653

Data Management Reporting Process
=================================

The DM project (including all DM contracted institutions) is legally required
to provide monthly status reports to LSST senior management, including the
:abbr:`AMCL (AURA Management Council for LSST)`. These monthly reports are
also provided to the funding agencies, and are audited annually by Federal
auditors. Non-compliance with reporting requirements is cause for contract
termination. As discussed above, the DM Project Manager maintains release and
management/system engineering plans in the LSST :abbr:`PMCS (Project
Management Control System)`. Each activity in the plan includes the name of
the activity, expected start and end dates, and assignees (with primary/lead
person listed first).

The LSST Project provides :doc:`JIRA Agile <jira-agile>`, a web-based tool for
Agile development. JIRA Agile is used as a means to capture the Epics and
stories that are imported into PMCS in the Release Planning process described
above. As the team performs Agile sprints, stories are marked as Done when
they are implemented. The story status is imported into PMCS for monthly
status reporting against the plan. The status collected marks the stories
(Steps) as 100 % complete which updates the Epic (Activities) % complete, and
sets the actual start and expected finish dates. The LSST Project Planner
exports the list of recently completed stories from JIRA Agile into tables,
sorted by WBS and Epic, and imports the status into PMCS.

Standard weekly status reporting cycle
--------------------------------------

Monday
    Each DM partner institution :abbr:`T/CAM (Technical/Cost Account Manager)`
    verifies that stories have been correctly mapped into Epics and Sprints.
    Large-scale issues that affect the overall release schedule or scope are
    discussed at the weekly DM Leadership Team meeting. The LSST PMCS planner
    publishes PDF files of the `current release plans`_.

Tuesday:
    DM team discusses status, issues, blockages, progress in Release
    Coordination Standup Meetings.

Friday:
    The assignees (or "primary resources") mark completed stories as Done in
    JIRA Agile. The LSST Project Controls Specialist imports the updated story
    status into PMCS.

.. _current release plans: https://www.lsstcorp.org/Primavera/MREFC/W15/

Standard monthly progress reporting cycle
-----------------------------------------

The first week of the month, the LSST Project Controls Specialist creates an
"extended" progress report, which indicates the progress of all the activities
and shows any Earned Value variances.

The second week of the month, the DM T/CAMs submit narrative to the DM Project
Manager, describing both the last months accomplishments and the next months
plans. The T/CAMs also submit narrative explaining any EV variances that are
above a defined threshold.

The third week of the month, DM Project Manager assembles both an Extended
Report containing all detailed narratives for each institution, and a Summary
Report which excerpts high-level accomplishments and plans across DM
institutions. The Extended Reports have been examined every year by Federal
auditors to check that the DM Project Manager is monitoring the work
performed/progress by each contracted DM institution. The Summary Report is
prepared for submission to senior management and for inclusion in the monthly
report to the AMCL. The DM Project Manager posts both report in `Docushare
Collection 221`_.

The fourth week of the month, the LSST Project Manager and Project Controls
Specialist prepare and submit the report to the funding agencies. These
reports are also included in the quarterly and annual reports to the funding
agencies.

.. _Docushare Collection 221: https://docushare.lsstcorp.org/docushare/dsweb/View/Collection-221
