############################
JIRA Work Management Recipes
############################

JIRA is a powerful web app that you can customize to suit your needs.
This page mentions a few ways to improve your workflow, though the `JIRA User Guide <https://confluence.atlassian.com/jira064/jira-user-s-guide-720416011.html>`_ is the definitive resource for power users.

LSST's JIRA is available at https://jira.lsstcorp.org.

*See also:* :ref:`workflow-jira` in the :doc:`/processes/workflow`.

.. _jira-create-filters:

Creating filters
================

Filters are a great way to maintain dynamic lists of issues for different workflows.
You can make an issue filter by saving a JIRA search:

1. Open the `Issues page in JIRA <https://jira.lsstcorp.org/issues>`_.
2. Enter a search term.
   `You can learn about JIRA's syntax from the docs <https://confluence.atlassian.com/jira064/advanced-searching-720416661.html>`_.
3. Run the search.
4. Press the **Save as** button on the search results page.

Your saved filters are accessible from the **Issues** dropdown menu in JIRA, among other places.

You can manage your filters from https://jira.lsstcorp.org/secure/ManageFilters.jspa.

.. _jira-search-examples:

Example search terms
====================

All of your open issues::

   assignee = currentUser() AND resolution = Unresolved ORDER BY updatedDate DESC

All of your issues that are in progress::

   status in ("In Progress", "In Review", Acknowledged, Reviewed, "Code Review", Blocked, "Awaiting Signoff") AND resolution = Unresolved AND assignee = currentUser() ORDER BY updatedDate DESC

All open issues you have been assigned to review::

   Reviewers in (currentUser()) AND status = "In Review"

All issues closed in a given month::

   status changed to Done DURING ("2015/12/01", "2015/12/31")

Issues where you have been mentioned in the last two weeks::

   text ~ currentUser() AND updatedDate >= -14d ORDER BY updated DESC

Issues that match a label::

   labels = label-name

Issues that are blocked by other issue::

   issueFunction in hasLinks("is blocked by")
