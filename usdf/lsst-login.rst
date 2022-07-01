############################
Using the lsst-login Servers
############################

The following login load-balancer is run by SLAC to jump to select Rubin Observatory development resources at SLAC:

- ``sdf-login.slac.stanford.edu``

Connecting and Authenticating
=============================

You'll need to be a member of the rubin_users unix group to access pretty much anything Rubin. If you're finding you're not, this is probably why. Ask to be added in the #ops-usdf slack channel.

You'll need to ssh into an SDF login server once to establish your home directory etc - **using your Windows account password**. From then on you can choose access via ssh or the browser portal, https://sdf.slac.stanford.edu (we don't recommend using the JupyterLab from the portal - we have our own RSP; just use the terminal).

You can use NoMachine for ssh access as well:

https://confluence.slac.stanford.edu/x/f8E7Eg

You can ssh into Rubin Observatory development servers at SLAC with your Windows account and password. It is only visible from the SDF login nodes (or within the SLAC network. Use the load balancer:

``rubin-devl.slac.stanford.edu``

Staff RSP
=========

An RSP has been deployed for testing - the kubernetes environment has not been declared production yet, so beware. Your SLAC credential will be used for authentication.

https://rubin-data-dev.slac.stanford.edu/
