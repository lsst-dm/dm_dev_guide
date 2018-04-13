#########################
Creating LDF Jira Tickets 
#########################

My content goes here.  


This page describes the procedures for reporting problems with the LSST Data Facility (LDF).  

1. :ref:`Creating a Jira ticket <jira-create>`.
2. :ref:`Checking ticket status <jira-status>`.
3. :ref:`The workflow of a ticket <jira-workflow>`.


.. _jira-create:


Tickets
-------

All problems encountered throughout the LDF resources need to be reported as a  **JIRA issue**.   The reporting process requires that a "trouble ticket" is created and are generically referred to as a **ticket**:

To get an account, see the :doc:`Onboarding Checklist </team/onboarding>`.



Creating a Jira Ticket
----------------------

You can create a ticket from the `JIRA web app <https://jira.lsstcorp.org>`_ toolbar using the **Create** button.
For more general information, you can consult `Atlassian's docs for JIRA <https://confluence.atlassian.com/jirasoftwarecloud/jira-software-documentation-764477791.html>`_ and `JIRA Agile <https://confluence.atlassian.com/agile067>`_.

JIRA allows a myriad of metadata to be specified when creating a ticket.
At a minimum, you should specify:

Project
   This should be set to **IT Helpdesk Support (IHS)**. 
Issue Type
   This should be set to **Incident**.   This is letting the admin staff know that there is something wrong with a resource.  It's not functioing correctly as it's suppose to.  
   A task and request are also part of this field.  These are used for when work is requested (task), or a discussion of what would be nice to have added to the NCSA LDF environment.     
Summary
   This is the ticket's title and should be written to help colleagues browsing JIRA dashboards.
Components
   You should choose from the pre-populated list of components to specify what part of the DM system the ticket relates to.
   If in doubt, ask your T/CAM.
Description
   The description should provide a clear description of the issue and can serve as a definition of 'Done.'
Attachment 
    This is for any additional information that is needed to explain the problem.   
Watchers 
   Who should also watch the progress of this ticket.  
Responsible Organization 
   This is at what site are you having a problem with.   The Base, Summit, NCSA, or not sure.   

.. _jira-status:

Checking Ticket Status
----------------------

Checking on the status of a ticket is at:  `JIRA web app <https://jira.lsstcorp.org>`_  You can search for your ticket number or many other search type criteria.   

Tickets are watched by many admins, the service manager and the product owner at NCSA.  After a ticket is created,  if a serious incident is ongoing the  `status page <https://confluence.lsstcorp.org/display/DM/LSST+Service+Status+page>`_ can be checked for known incidents, and a quick note into the dm-infrastucture slack channel can also get information  about a problem you are having.   

Currently all resources at NCSA are considered development and fixed with a "best effort" type of work.   NCSA currently works on a 8*5 (CST) schedule for non-critical tickets.   A critical issue will be worked on throughout a 7*24 schedule to resolution.   


.. _jira-workflow:

The Workflow of a ticket
----------------------------------
Tickets are created with a status of **todo.** 
Tickets that are beig worked on have a status of **in progress**.  
All communication about this task/incident/request will be kept on comments with this ticket.  The Jira system will send email to the watchers and creator of the ticket with each entry in the comment field.   Please keep all the reporting and exchange of information regarding this ticket through this jira interface.   That will keep all the information in one place.     
The admin once they finish with a ticket will mark the ticket **awaiting signoff**.    This is when the ticket owner (you) would go out and verify that the request/task/incident is truely resolved.    The owner would then use the **workflow** pull down menu to set the ticket to being **done**.   This ensures that the originator checks to make sure that the ticket has been resolved to their satisfaction before the ticket is put into a **done** status.   

