#############################
Using the lsst-db Server
#############################

``lsst-db`` is the development MySQL database server run by NCSA for LSST DM development work.
The cname ``lsst-db.ncsa.illinois.edu`` directs to ``lsst10.ncsa.illinois.edu``.

To get an account, see the :doc:`Onboarding Checklist </getting-started/onboarding>`.

This page is designed to assist developers in their work with ``lsst-db``:

#. :ref:`lsst-db-password`
#. :ref:`lsst-db-auth`

.. _lsst-db-password:

Account Password
================

The lsst-db server does NOT use your NCSA account.

After you receive your initial temporary password, change it as soon as possible as follows.

Set the MYSQL_HISTFILE environment variable to /dev/null (By doing it you will prevent the command with your new password from being saved in clear-text history file.).

.. prompt:: bash

   export MYSQL_HISTFILE=/dev/null

Then, log into MySQL:

.. prompt:: bash

   mysql -h lsst-db.ncsa.illinois.edu -u<userName> -p
   Password: <type temporary mysql password>

And then, set a new password:

.. prompt:: bash

   mysql> set password = password('theNewPassword');


.. _lsst-db-auth:

Authentication Configuration File
=================================

Create a ``db-auth.py`` configuration file with your mysql host, user, password and mysql port information.  This file belongs in ``$HOME/.lsst/``, and must have permissions 600.

.. prompt:: python

   config.database.authInfo["auth1"].host = "lsst-db.ncsa.illinois.edu"
   config.database.authInfo["auth1"].user = "<user>"
   config.database.authInfo["auth1"].password = "<password>"
   config.database.authInfo["auth1"].port = 3306

You will also need to create a ``db-auth.paf`` file, because the ``pex_persistence`` package hasn't been updated to use Config.  This file also belongs in ``$HOME/.lsst``, and requires permissions 600.

.. prompt:: python

   database: {
       authInfo: {
          host: lsst-db.ncsa.illinois.edu
          port: 3306
          user: <user>
          password: <password> 
       }
   }


