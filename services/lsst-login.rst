############################
Using the lsst-login Servers
############################

The following login nodes are run by NCSA for access to select Rubin Observatory development resources at NCSA:

- ``lsst-login01.ncsa.illinois.edu``
- ``lsst-login02.ncsa.illinois.edu``
- ``lsst-login03.ncsa.illinois.edu``

To get an account, see the :doc:`Onboarding Checklist </team/onboarding>`.

This page is designed to assist developers in use of the ``lsst-login`` servers:

#. :ref:`lsst-login-overview`
#. :ref:`lsst-login-connect`
#. :ref:`lsst-login-software`

.. _lsst-login-overview:

Overview
========

The ``lsst-login`` servers are primarily intended as bastions used to access other resources at NCSA. Additional capabilities include:

- light development with short-running processes that require modest resources (e.g., build docs, short compilations against LSST software stack)
- view files (e.g., FITS files)

Users are encouraged to submit batch jobs to perform work that requires more significant resources. Please see :doc:`/services/batch` for more information.

The ``lsst-login`` nodes have access to the :doc:`LDF file systems <storage>`.

For system status and issues:

- `Service status <https://confluence.lsstcorp.org/display/DM/LSST+Service+Status+page>`_ including announcements of upcoming planned down-time.
- `Real-time system status <https://monitor-ncsa.lsst.org/>`_ (requires login).
- To report system issues, please submit an :doc:`IHS ticket <ldf-tickets>` tagging NCSA as the responsible organization.

.. _lsst-login-connect:

Connecting and Authenticating
=============================

You can log into Rubin Observatory development servers at NCSA with your NCSA account as follows:

   - NCSA username and password **OR** valid Kerberos ticket from workstation/laptop, **AND**
   - NCSA Duo authentication

You can reset your NCSA password at the following URL:

   - https://identity.lsst.org/reset

Information on setting up NCSA Duo is available at the following URL:

   - https://wiki.ncsa.illinois.edu/display/cybersec/Duo+at+NCSA

If you are using OpenSSH on your local machine and you wish to use Kerberos from your local machine (instead of entering your password on the login node), you could add something like this to your local ~/.ssh/config file:

.. prompt:: bash $ auto

  GSSAPIAuthentication yes
  PreferredAuthentications gssapi-with-mic,keyboard-interactive,password

The Kerberos domain for the ``lsst-login`` servers is ``NCSA.EDU``, so something like this may work to generate a Kerberos ticket on your local machine:

.. prompt:: bash $ auto

  kinit username@NCSA.EDU
  
  # you may get an error like this: 'kinit: Cannot find KDC for realm "NCSA.EDU" while getting initial credentials';
  # if that's the case, the Kerberos config on the local machine may need to be updated with 'dns_lookup_kdc = true'

You may wish to use an ``lsst-login`` node as a "jump host" (a gateway to an interior node). If using OpenSSH on your local machine you can do this as follows:

.. prompt:: bash $ auto

   Host lsst-someinternalhost.ncsa.illinois.edu
      User ncsausername
      ProxyJump lsst-login01.ncsa.illinois.edu

When using an ``lsst-login`` node as a "jump host" you may also wish to configure port forwarding through the lsst-login node to the internal cluster node. To do that you would include something like this in your OpenSSH config file:

.. prompt:: bash $ auto

   Host lsst-someinternalhost.ncsa.illinois.edu
      User ncsausername
      ProxyJump lsst-login01.ncsa.illinois.edu
      DynamicForward yourportnumber

You may also wish to reuse a single connection to/through an ``lsst-login`` node via an OpenSSH ControlMaster socket. This allows you to authenticate to the login node one time and reuse that initial connection to make additional connections without authenticating again. See for example
`OpenSSH Cookbook - Multiplexing <https://en.wikibooks.org/wiki/OpenSSH/Cookbook/Multiplexing>`_.

A relatively complete ``~/.ssh/config`` "recipe" for streamlining your SSH connections (assuming OpenSSH, e.g., on Linux or macOS) through the ``lsst-login`` nodes might look like this:

.. prompt:: bash $ auto

   # Set common config for the lsst-login nodes
   Host lsst-login*
      # if your account on your local workstation/laptop does not match your LSST username, indicate the latter should be used;
      # substitute your own NCSA username
      User ncsausername               
      # allow use of a Kerberos ticket on your local machine for auth to LSST machines
      GSSAPIAuthentication yes   
      # prefer Kerberos ticket auth, amongst other possibilities (order/include others as desired)
      PreferredAuthentications gssapi-with-mic,keyboard-interactive,password
      # forward your local Kerberos ticket to the login node if you need to continue to another LSST server after the login
      GSSAPIDelegateCredentials yes
      # configure OpenSSH Control Master "multiplexing" (to allow reuse of an initial connection)
      ControlMaster auto
      ControlPath ~/.ssh/cm_socket_%r@%h:%p
      ControlPersist 5m

   # Define aliases onto full hostnames for each login node
   Host lsst-login01
      HostName lsst-login01.ncsa.illinois.edu
   Host lsst-login02
      HostName lsst-login02.ncsa.illinois.edu
   Host lsst-login03
      HostName lsst-login03.ncsa.illinois.edu

   # Define an alias and config for an internal node, which can only be reached through a login node
   Host lsst-devl01
      HostName lsst-devl01.ncsa.illinois.edu
      # you may need to specify your NCSA username again
      User ncsausername
      # when connecting to this internal host, tunnel/jump through a login node (using an alias you defined above)
      ProxyJump lsst-login01
      # if you want to use your local Kerberos ticket to authenticate on the interior node, configure that:
      GSSAPIAuthentication yes
      PreferredAuthentications gssapi-with-mic
      # if the internal node is a batch submit node where you might want a Kerberos ticket (e.g., to
      # submit jobs to HTCondor), you can choose to forward your credentials:
      GSSAPIDelegateCredentials yes
      # if you need to configure port forwarding to the internal node, you can do that here;
      # substitute your actual port number
      DynamicForward yourportnumber

With such config in ``~/.ssh/config`` on your local machine, your SSH connections can be significantly streamlined. Your experience may look like this:

(1) Your first connection attempt involves typing your password once, on your local machine, along with a Duo push for the login node. There's no need to type your password on the login node or the internal node due to GSSAPI authentication. And your local Kerberos ticket is forwarded into your session on the internal node:

.. prompt:: bash $ auto

   localuser@localmachine ~ % kinit ncsauser@NCSA.EDU
   ncsauser@NCSA.EDU's password: 
   localuser@localmachine ~ % ssh lsst-devl01
   Duo two-factor login for ncsauser
   
   Enter a passcode or select one of the following options:
   
    1. Duo Push to XXX-XXX-####
   
   Passcode or option (1-1): 1
   Last login: Fri Aug 14 15:06:35 2020 from 141.142.181.18
   lsst-devl01.ncsa.illinois.edu (141.142.181.231)
     OS: CentOS 7.8.2003   HW: Dell   CPU: 24x 2.60GHz   RAM: 252 GB
     Site: ncsa  DC: npcf  Cluster: condor_dac  Role: condor_submit
   [ncsauser@lsst-devl01 ~]$ klist
   Ticket cache: FILE:/tmp/krb5cc_11111_OrKJ2p97xr
   Default principal: ncsauser@NCSA.EDU
   
   Valid starting       Expires              Service principal
   08/14/2020 15:06:12  08/15/2020 01:05:59  krbtgt/NCSA.EDU@NCSA.EDU
   [ncsauser@lsst-devl01 ~]$

(2) In a 2nd terminal window, you can connect again without any need to authenticate whatsoever (thanks to your ControlMaster config):

.. prompt:: bash $ auto

   localuser@localmachine ~ % ssh lsst-devl01
   Last login: Fri Aug 14 15:07:34 2020 from 141.142.181.18
   lsst-devl01.ncsa.illinois.edu (141.142.181.231)
     OS: CentOS 7.8.2003   HW: Dell   CPU: 24x 2.60GHz   RAM: 252 GB
     Site: ncsa  DC: npcf  Cluster: condor_dac  Role: condor_submit
   [ncsauser@lsst-devl01 ~]$

(3) Your control master master connection will persist in the background after your initial client connection terminates, according to the value of ``ControlPersist``. To terminate your control master connection immediately, do the following on your local machine:

.. prompt:: bash $ auto

   localuser@localmachine ~ % ssh -O exit lsst-login03
   Exit request sent.
   localuser@localmachine ~ %

NOTE: This will break all connections in any terminals that depend on this master connection, e.g.:

.. prompt:: bash $ auto

   [ncsauser@lsst-devl01 ~]$ client_loop: send disconnect: Broken pipe
   localuser@localmachine ~ %

.. tip::

   **More tips on working Kerberos tickets and OpenSSH ControlMaster**

   - Your Kerberos ticket on your local machine will need to be renewed occasionally, which you can do with ``kinit -R``.
   - Renewing the ticket on your local machine will not generally renew any tickets you have forwarded to remote machines. (NOTE: OpenSSH has a GSSAPIRenewalForcesRekey option that will cascade your ticket renewal out wherever you have forwarded them, however it is not implemented on all platforms, e.g. macOS.)
   - The example above shows you can request a ticket with a maximum lifetime (25 hours) and maximum renewable life time (7 days), again, ``kinit -l 25h -r 7d ...``.
   - If your local ticket expires before you renew it you will have to ``kinit`` (and authenticate with your password) to create a new ticket.

.. _lsst-login-software:

Common Software Available
=========================

Refer to :doc:`software` for more details about software available for use on ``lsst-login`` nodes.

