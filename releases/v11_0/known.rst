#############
Known Issues
#############

Cross Platform
==============

-  Compiling some packages – in particular ``afw ``– requires a large
   amounts of RAM. This is compounded as the system will automatically
   attempt to parallelize the build, and can cause the build to run
   extremely slowly or fail altogether. On machines with less than 8 GB
   of RAM, disable parallelization by setting ``EUPSPKG_NJOBS=1`` in
   your environment before running ``eups distrib``.

Red Hat (and clones) specific:
==============================

Older platforms:
----------------

-  Not a bug as such, but if you have a problem building on RHEL 6 check
   the `Pre-requisites </display/LSWUG/OSes+and+Prerequisites>`__  notes
   to make sure sure you are using a more recent version of gcc (minimum
   required is 4.8)
-  curl looks for certificates in ``/etc/pki/tls/certs/ca-bundle.crt``
   rather than
   ``/etc/ssl/certs/ca-certificates.crt.``\ ``The solution is to copy``\ `` ca-certificates.crt``\ `` to``\ `` ca-bundle.crt``\ `` as explained at ``\ ``Building the LSST Stack from Source``

OSX specific:
=============

New versions:
-------------

-  El Capitan came out after our testing period, and there are known
   issues (eg. |image0|) that will be addressed in the next release.

Older platforms:
----------------

-  Some old installations of XCode on Macs create a \ ``/Developer``
   directory.  This can interfere with installation.
-  Macs must use the \ ``clang`` compiler, not \ ``gcc``. \ |image1|

   -  One version of this problem occurs when using Macports, which, by
      default, will create a symlink from ``/opt/local/bin/c++`` to its
      version of ``g++``. Try removing that, starting a new shell, and
      restarting ``eups distrib install``.

 

.. |image0| image:: /plugins/servlet/confluence/placeholder/macro?definition=e2ppcmE6a2V5PURNLTMyMDB9&locale=en_GB
.. |image1| image:: /plugins/servlet/confluence/placeholder/macro?definition=e2ppcmE6a2V5PURNLTM0MDV9&locale=en_GB
