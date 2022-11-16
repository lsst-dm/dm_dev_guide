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

You can use NoMachine for ssh access as well:

https://confluence.slac.stanford.edu/x/f8E7Eg

You should ssh into Rubin Observatory development servers at SLAC with your unix account and password. It is only visible from the s3df login nodes. Use the load balancer:

ssh ``rubin-devl`` (note: do not add the .slac.stanford.edu postfix!)

Passwordless ssh access to rubin-devl
=====================================

You can modify your .ssh config to allow direct passwordless access from your device to rubin-devl, by adding this to your .ssh/config file on your end:

.. code-block:: text

   Host slac*
           User <you>

   Host slacl
           Hostname s3dflogin.slac.stanford.edu

   Host slacd
           Hostname rubin-devl
           ProxyJump slacl

and then add your e.g. ``~/.ssh/id_rsa.pub`` from from your device to ``~/.ssh/authorized_keys`` at SLAC.

Outbound Access
===============

Currently the s3df is in private IP space, so a squid proxy is used to access the outside world. Your .bashrc was configured when your account got created to set environment variables to make use of the proxy. You should not overwrite the section of your .bashc that sets HTTPS_PROXY (and similar).

Should you have overwritten your .bashrc, this snippet is what set up the environment variables:

.. code-block:: text

   # SLAC S3DF - source all files under ~/.profile.d
   if [[ -e ~/.profile.d && -n "$(ls -A ~/.profile.d/)" ]]; then
      source <(cat $(find -L  ~/.profile.d -name '*.conf'))
   fi

Staff RSP
=========

An RSP has been deployed. Your SLAC unix credential will be used for authentication.

https://usdf-rsp.slac.stanford.edu/
