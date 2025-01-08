##################################################
S3DF: SLAC Shared Science Data Facility Hosts USDF
##################################################

The USDF is hosted on the S3DF cluster at SLAC. The resource is shared amongst projects, and is documented here:

https://s3df.slac.stanford.edu/public/doc/#/

The following login load-balancer is run by SLAC to jump to select Rubin Observatory development resources at SLAC.  Note that almost nothing useful can be done on the login nodes themselves:

- ``s3dflogin.slac.stanford.edu``

USDF usage questions can be posted to the `Rubin Observatory slack <https://rubin-obs.slack.com>`__ ``#usdf-support`` channel. Announcements will go to ``#usdf-announce``. SLAC also maintains an internal workspace with a channel dedicated to S3DF support, called comp-sdf. We have created an `LSSTC workspace <https://lsstc.slack.com>`__ wormhole into that channel, called ``#ops-help-s3df-slac``, intended for non Stanford/SLAC people.  This slack channel is used by the entire S3DF community.

Connecting and Authenticating to Rubin servers
==============================================

You'll need to be a member of the ``rubin_users`` unix group to access pretty much anything Rubin. If you're finding that you cannot, this is probably why. Ask to be added in the ``#usdf-support`` slack channel or contact your SLAC POC.

You can use `NoMachine <https://s3df.slac.stanford.edu/#/tutorials?id=graphics-and-remote-visualization>`__ for ssh access as well:

https://s3dfnx.slac.stanford.edu/

You should ssh into Rubin Observatory development servers at SLAC with your unix account and password. It is only visible from the s3df login nodes. Use the load balancer:

ssh ``rubin-devl`` (note: do not add the .slac.stanford.edu postfix!)

If you are connecting from the summit, outside the Long Haul Network (LHN), you'll currently need to access s3df via a bastion host outside s3df. ssh to ``centos7.slac.stanford.edu`` for this, authenticating with your usual unix credential, and then to s3dflogin.

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

and then add your e.g. ``~/.ssh/id_rsa.pub`` from from your device to ``~/.ssh/authorized_keys`` at SLAC, using:

ssh-copy-id <you>@s3dflogin.slac.stanford.edu

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

Note that the notebook tutorials that come with RSP are targeted at the IDF/DP02. The DP0.2 image data is not available at the USDF; the catalogue data is.
