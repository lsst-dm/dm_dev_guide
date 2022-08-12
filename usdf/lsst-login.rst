##################################################
S3DF: SLAC Shared Science Data Facility Hosts USDF
##################################################

The USDF is hosted on the S3DF cluster at SLAC. The resource is shared amongst projects, and is documented here:

https://s3df.slac.stanford.edu/public/doc/#/

The following login load-balancer is run by SLAC to jump to select Rubin Observatory development resources at SLAC (almost nothing useful can be done here. Use the 
jump nodes):

- ``s3dflogin.slac.stanford.edu``

USDF usage questions can be posted to slack ``#ops-usdf``. Announcements will go to ``#ops-usdf-announce``.

Connecting and Authenticating to Rubin servers
==============================================

You'll need to be a member of the rubin_users unix group to access pretty much anything Rubin. If you're finding you're not, this is probably why. Ask to be added in the #ops-usdf slack channel.

You'll need to ssh into an SDF login server once to establish your home directory etc - **using your unix account password**. From then on you can choose access via ssh or the browser portal, https://s3df.slac.stanford.edu/ondemand (we don't recommend using the JupyterLab from the portal - we have our own RSP; just use the terminal).

You can use NoMachine for ssh access as well:

https://confluence.slac.stanford.edu/x/f8E7Eg

You can ssh into Rubin Observatory development servers at SLAC with your Windows account and password. It is only visible from the SDF login nodes (or within the SLAC network. Use the load balancer:

ssh ``rubin-devl`` (note: do not add the .slac.stanford.edu postfix!)

Staff RSP
=========

An RSP has been deployed. Your SLAC unix credential will be used for authentication.

https://usdf-rsp.slac.stanford.edu/
