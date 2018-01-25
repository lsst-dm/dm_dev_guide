######################################
Using the Bulk Transfer Server at NCSA
######################################

NCSA has setup a dedicated bulk transfer server, ``lsst-xfer.ncsa.illinois.edu``, for handling large data moves in and out of LSST's storage at NCSA.
The following bulk data transfer clients are configured on ``lsst-xfer.ncsa.illinois.edu``:

- :ref:`Globus Online <ncsa-bulk-globus>`
- :ref:`iRODS <ncsa-bulk-irods>`
- :ref:`BBCP <ncsa-bulk-bbcp>`

.. _ncsa-bulk-globus:

Globus Online
=============

If you don't already have a Globus Online account, you'll need to create one at https://www.globusonline.org/SignIn#step=SignUp.

Authentication is handled by a certificate created locally on the ``lsst-xfer`` system using your NCSA account.

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

``lsst-xfer.ncsa.illinois.edu`` is setup to use TCP ports 65001-65535 for BBCP transfers with the following external networks:

- IN2P3 134.158.0.0/16
- SLAC 134.79.0.0/16
- UC Davis 169.237.0.0/16
- UW 140.142.0.0/16
- UW 205.175.96.0/19

Additional subnets can be requested by `filing a JIRA ticket <https://jira.lsstcorp.org/secure/CreateIssueDetails!init.jspa?pid=12200&issuetype=10902&priority=10000>`_ in the IHS project.

See:

- http://www.slac.stanford.edu/~abh/bbcp/
- http://www.nics.tennessee.edu/computing-resources/data-transfer/bbcp
