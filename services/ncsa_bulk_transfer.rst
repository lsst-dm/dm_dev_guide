######################################
Using the Bulk Transfer Server at NCSA
######################################

NCSA has setup a dedicated bulk transfer server, ``lsst-xfer.ncsa.illinois.edu``, for handling large data moves in and out of LSST's storage at NCSA.
The following bulk data transfer clients are configured on ``lsst-xfer.ncsa.illinois.edu``:

- :ref:`Globus Online <ncsa-bulk-globus>`
- :ref:`iRODS <ncsa-bulk-irods>`
- :ref:`bbcp <ncsa-bulk-bbcp>`

.. _ncsa-bulk-globus:

Globus Online
=============

If you don't already have a Globus Online account, you'll need to create one at https://www.globusonline.org/SignIn#step=SignUp.

Authentication is handled by a certificate created locally on the ``lsst-xfer`` system using the local unix account.
You will need to email ``lsst-admin at ncsa.illinois.edu`` and request them to manually set a password for your unix account on ``lsst-xfer.ncsa.illinois.edu``.
Once the password is temporarily set, you can change the password by logging into ``lsst-xfer.ncsa.illinois.edu`` with your SSH public key and using the :command:`passwd` command.

The globus connect endpoint has been created as a public endpoint named: ``lsst#lsst-xfer``.

If you need to use Globus Online from a local computer that is not already configured with the Globus Online service, you can quickly and easily add your computer as a local Globus Connect Endpoint.
Go to https://www.globusonline.org/xfer/ManageEndpoints and select add **Globus Connect** for instructions and software downloads.

.. _ncsa-bulk-irods:

iRODS Client
============

The iRODS client can be used to transfer data from iRODS servers such as those at IN2P3.
Documentation for using the iRODS client can be found at https://www.irods.org/index.php/icommands.

To connect to the IN2P3 storage, set the following in :file:`~/.irodsEnv`:

.. code-block:: text

   irodsHost 'ccirods.in2p3.fr' 
   irodsPort 5579 
   irodsUserName 'lsstread' 
   irodsHome '/lsst-fr/data' 
   irodsZone 'lsst-fr'

.. _ncsa-bulk-bbcp:

bbcp Client
===========

BBCP is an alternative to Gridftp when transferring large amounts of data, capable of breaking up your transfer into multiple simultaneous transferring streams, thereby transferring data much faster than single-streaming utilities such as SCP and SFTP.
See:

- http://www.slac.stanford.edu/~abh/bbcp/
- http://www.nics.tennessee.edu/computing-resources/data-transfer/bbcp
