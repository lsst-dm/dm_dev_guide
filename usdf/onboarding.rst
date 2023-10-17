############################
SLAC Onboarding Procedure
############################

Overview
=============================

The SLAC onboarding procedure involves the following steps:

- join the SLAC HEP users organization, SLUO
   - fill out the SLAC Users Organization (SLUO) form
   - fill out the SLAC Site Access Portal form
- a SLAC ServiceNow ticket is submitted to IT to request the account
- IT creates the unix account and sends a link to reset the password
- do the SLAC Cyber training

**If you already have a SLAC unix account, you do not need to be re-onboarded.**

Note that if you only have a SLAC Confluence account (eg for DESC or LSSTCam), you will still need to be onboarded as a user **and** there will be complications with your accounts. SLAC and Rubin confluence sites are independent installations.

- if your existing Confluence account name is longer than 8 characters (or if for some reason your unix account name did not match your confluence one), you will need a different name. In that case, a new Confluence identity is created using your unix account name, added to DESC permissions, and your old account deleted.
- else: you will need to login to Confluence once with the unix password, then the Confluence admins will merge the unix and Confluence identities.
- once all this happens, Confluence will use your unix account password for authentication; if it expires, it's the unix account password that needs changing; there is no longer a specific Confluence account/password. 

Procedure Details
=============================

To obtain a SLAC SID number and SLAC account, you first need to become a SLAC User. Please follow the below steps and complete the registration form.

New users are required to complete the SLUO registration form using this `form <https://www-group.slac.stanford.edu/IAM/>`__. The link also points to 
documentation on the process.

Notes:
 - Experiment: select Vera C. Rubin Observatory

Notes for Portal:
 - **If your institution is missing, let Richard Dubois know, to get it added to the list**
 - Emergency contact: your own personal contact - relative, friend.
 - Group: select "FPD LSST Computing"
 - details of visit and project name: Using SLAC computing resources to collaborate on Rubin Operations. Seems optional to include your home institution.
 - Funding source: choose your majority support source
 - Time at SLAC: this is physically on site. For most people, this is <10%. Occasional visits for meetings don't count.
 - Start date: choose today
 - Answer "yes" to will you be performing work at SLAC
 - SLAC Spokesperson/Sponsor/Supervisor: Select Richard Dubois.
	
1)	When the user submits the onboarding request form, the form is
	then sent to several approvers before a SLAC ID is granted.
	
	If the user is a US citizen, the completed onboarding form is
	first routed to the SLAC poc then to the SLAC HR team for SLAC
	ID duplicate check and issue the SLAC ID number.

	If the user is a non-US citizen, the completed onboarding form is first routed to the SLAC poc then to the VUE Center Coordinator and to the SLAC HR team for SLAC ID duplicate check and issue the SLAC ID number.

2)	After the SLAC SID number is issued, the VUE Center Coordinator completes the user’s SLUO registration form and sends an email to the user with instructions of the next steps. 

3)	The SLAC POC submits a ticket to IT requesting a SLAC account
	for the new user. Be sure to tell the POC your preferred account name (and second choice).

4) SLAC IT will send a url to the user to reset their initial
    password

5) SLAC Cyber training must be done within 2 weeks to keep the
    account enabled.

    
Troubleshooting Accounts
=============================

Check that you are a member of the rubin_users group:

id <your account>

Accounts can get disabled a number of ways:

- Every 6 months password changes (change pw - `unix <https://unix-password.slac.stanford.edu/>`__)
- Every year Cyber training `(link <https://slactraining.skillport.com/skillportfe/login.action>`__)
- They can also be locked out if they've forgotten their password(s)
  or put in too many attempts with the wrong password. (`ticket <https://slacprod.servicenowservices.com/gethelp.do>`__ to request a reset)

The user is warned about all these events, but in case they've been ignored/forgotten, how to figure out which it is and how to fix it?

- The accounts `site <https://www-internal.slac.stanford.edu/comp/admin/bin/account-search.asp>`__ can tell us if the account is disabled
   - if none disabled, then it's due to password expire
   
- The training `site <https://www-internal.slac.stanford.edu/esh-db/training/slaconly/bin/ETA_ReportAll.asp?opt=6>`__ can tell us if Cyber is expired.
