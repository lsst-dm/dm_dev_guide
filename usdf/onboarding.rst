############################
SLAC Onboarding Procedure
############################

Overview
========

The SLAC onboarding procedure involves the following steps:

#. Join the SLAC Users Organization, SLUO
#. Fill out the SLAC Site Access Portal form
#. Request a username and access to S3DF batch repos
#. Do the SLAC cyber training
#. Register your SLAC UNIX account in S3DF
#. Fill out the `Rubin Observatory Staff Access Form <https://ls.st/staff-access-form>`__ (if you have not already done so as part of Rubin onboarding)  
#. Complete Access Control Training.

SLAC IT will create Active Directory (AD) and unix accounts (for the same username).  The AD account is only used for annual cyber training and web access to Service Now, the SLAC IT ticketing system. The AD account needs to be accessed every 60 days; notifications are sent out.  Once IT creates the accounts, a link will be emailed to reset the passwords.

Notes:

* If you are an in-kind contributor, you'll need to be listed in `SITCOMTN-050 <https://sitcomtn-050.lsst.io/>`__.
* If you already have a SLAC unix account, you do not need to be re-onboarded. However, you may need to follow step 3 below.
* If you only have a SLAC Confluence account (e.g., for DESC or LSSTCam), you will still need to be onboarded as a user, **and** there will be complications with your accounts. SLAC and Rubin Confluence sites are independent installations.

  - If your existing Confluence account name is longer than 8 characters (or if for some reason your unix account name did not match your Confluence one), you will need a different name. In that case, a new Confluence identity is created using your unix account name, added to DESC permissions, and your old account is deleted.
  - Otherwise, you will need to login to Confluence once with the unix password, then the Confluence admins will merge the unix and Confluence identities.
  - Once all this happens, Confluence will use your unix account password for authentication; if it expires, it's the unix account password that will need to be changed. There are no longer Confluence-specific accounts/passwords.

Onboarding Steps
================

Please follow the steps below to complete the onboarding process.

1. SLUO Registration
""""""""""""""""""""
New users are required to register as a SLAC User via the **Enrollment** button at the bottom of the `SLAC Scientific Collaborative Research Registration <https://it.slac.stanford.edu/identity/scientific-collaborative-researcher-registration>`__ page.  Also linked at that page are `step-by-step instructions for that process <https://it.slac.stanford.edu/support/KB0012289>`__.

Notes for the SLAC User Registration form:

- For SLAC Project, select "Vera C. Rubin Observatory".

2. Site Access Portal form
""""""""""""""""""""""""""
Once the your SLAC Point-of-Contact (POC), Sierra Villarreal, has approved your request, you will receive an email to fill out the SLAC Site Access form.

Notes for the Site Access form:

- If your institution is missing, let Sierra know, and she will have it added to the list.
- Emergency Contact: Your own personal contact, e.g., relative, friend.
- Group: Select "FPD Technology & Operations".
- Details of visit and project name:  "Using SLAC computing resources to collaborate on Rubin Operations."  (It seems to be optional to include your home institution.)
- Funding Source: Choose your majority support source.
- Time at SLAC: This is for being physically on site. For most people, this is <10%. Occasional visits for meetings don't count.
- Start date: Choose today.
- Will you be performing work at SLAC: "Yes".
- SLAC Spokesperson/Sponsor/Supervisor: Select Antonia Villarreal.

All foreign nationals will additionally be requested to submit an CV with the following guidelines:

- The CV must be written in English
- All education and work history back to the start of college (within the last 10 years)
- Beginning and end dates of education and experience must include month and year (mm/yyyy format)
- Include all science and technology specialties
- Names of all academic institutions attended must be current/accurate
- There should be no time gap. If any gaps in education and/or employment, it must be noted and explained
- Do not include social security numbers, government ID numbers, passport numbers, or any other similar data

3. Username Request and S3DF Batch Repo Access
""""""""""""""""""""""""""""""""""""""""""""""

Once the Site Access form has been approved, another email will be sent out with your SLAC System ID (SID).  Once the SID has been assigned, computing accounts can be made.  At this point, email your POC, Sierra (sierrav@slac.stanford.edu), with your first and second choice usernames (these are limited to no more than 8 alphanumeric characters), and she will submit a ticket to IT with the account request.  Once your account is activated, Sierra will email you a link to request S3DF batch repo access.

4. Cyber Training
"""""""""""""""""

Cyber training comes up annually. You will need to use your Active Directory (aka Windows) account to log into the training website.  Note that you will need to use your SLAC SID wherever a "username" is requested.

The SLAC training website is https://slactraining.csod.com/ and the interim training password is "SLACtraining2005!". If it does not work, email slac-training via the link on that entry page and ask them to reset it. Then go back to the original link, enter your SID and this password, and do course CS100.  DO NOT click on "Forgot Password?".

Note that if you have received an email saying that your training is coming due, the SLAC System ID (SID) is embedded in the url in the email as "sid=xxxxxx".

If you still have problems, ask your SLAC POC for help.

**SLAC cyber training must be done within 2 weeks to keep the account enabled.**

5. Register your SLAC UNIX account in S3DF
""""""""""""""""""""""""""""""""""""""""""

This is the same as step 2 of the `S3DF Accounts and Access page <https://s3df.slac.stanford.edu/#/accounts-and-access>`__.   This step should be performed *before* accessing any resources, including S3DF accounts and the USDF Rubin Science Platform.

6. Fill out the Rubin Observatory Staff Access Form
"""""""""""""""""""""""""""""""""""""""""""""""""""

Some of the resources and data accessible from the USDF are meant to be only available to Rubin staff.  Please fill out the `Rubin Observatory Staff Access Form <https://ls.st/staff-access-form>`__ to help us determine whether you can be regarded as a Rubin team-member for the purposes of accessing these staff-only resources.

**Final Notes:**

When the user submits the onboarding request form, the form is
sent to several approvers before a SLAC SID is granted.
If the user is a US citizen, the completed onboarding form is
routed to the SLAC POC, then to the SLAC HR team for a
duplicate SID check.
If the user is a non-US citizen, the completed onboarding form is routed to the SLAC POC, then to the VUE Center Coordinator, and then to the SLAC HR team for a duplicate SID check.

7. Complete Access Control Training
"""""""""""""""""""""""""""""""""""

All users will need to complete Access Control Training previous to being granted access to the USDF resources. This training is currently run every Wednesday at 8am PDT and located on Zoom (`Zoom meeting link <https://stanford.zoom.us/j/93763004905?pwd=GxkphvOcZ64ebx41C04bLDMOVqISdo.1>`__). If that time is not feasible, please reach out to Sierra Villarreal on Rubin, Discovery Alliance, or SLAC Slack workspaces.


Troubleshooting Accounts
========================

From an S3DF node, check that you are a member of the ``rubin_users`` group::

  $ id <your username>

Contact your SLAC POC to request access to that group.

Accounts can get disabled a number of ways:

- Out-of-date password (`unix password reset <https://unix-password.slac.stanford.edu/>`__).
- Out-of-date cyber training (`training link <https://slactraining.skillport.com/skillportfe/login.action>`__)
- Accounts can also be locked out if too many attempts with the wrong password are made.  File a `Service Now ticket <https://slacprod.servicenowservices.com/gethelp.do>`__ to request a reset.  Alternatively, it's often quicker to call the `SLAC IT Service Desk <https://it.slac.stanford.edu/support>`__ directly for help with passwords.

Users are warned via several emails about these events, but in case those emails have been ignored/forgotten, the following resources can be used to find any issues:

- The `accounts site <https://www-internal.slac.stanford.edu/comp/admin/bin/account-search.asp>`__  can tell us if the account is disabled.  If it's not disabled, then the password has expired.
- The `training site <https://www-internal.slac.stanford.edu/esh-db/training/slaconly/bin/ETA_ReportAll.asp?opt=6>`__ can tell us if cyber training has expired.

Currently, both of these sites are only available within the SLAC internal network.
