############################
Using the lsst-dev-db Server
############################

.. ATTENTION::
  **The lsst-dev-db server will be turned off on Oct 1, 2020.**

  Services that make use of this server should move to using alternate, supported databases.

The material presented below is for historical reference and will be removed in the future.
------------

``lsst-dev-db`` is the development MySQL database server run by NCSA for LSST DM development work.
The CNAMEs ``lsst-db.ncsa.illinois.edu`` and ``lsst10.ncsa.illinois.edu`` direct to ``lsst-dev-db.ncsa.illinois.edu`` to support historical usage of those hostnames.

To get an account, see the :doc:`Onboarding Checklist </team/onboarding>`.

This page is designed to assist developers in their work with ``lsst-dev-db``:

#. :ref:`lsst-db-password`
#. :ref:`lsst-db-auth`

.. _lsst-db-password:

Account Password
================

The ``lsst-dev-db`` server does NOT use your NCSA account.

After you receive your initial temporary password, change it as soon as possible as follows.

Set the ``MYSQL_HISTFILE`` environment variable to :file:`/dev/null` (By doing it you will prevent the command with your new password from being saved in clear-text history file.).

.. code-block:: bash

   export MYSQL_HISTFILE=/dev/null

Then, log into MySQL:

.. code-block:: bash

   mysql -h lsst-dev-db.ncsa.illinois.edu -u<userName> -p
   Password: <type temporary mysql password>

And then, set a new password:

.. code-block:: bash

   set password = password('theNewPassword');

.. _lsst-db-auth:

Authentication Configuration File
=================================

Create a ``db-auth.py`` configuration file with your mysql host, user, password and mysql port information.  This file belongs in ``$HOME/.lsst/``, and must have permissions 600.

.. code-block:: python

   config.database.authInfo["auth1"].host = "lsst-dev-db.ncsa.illinois.edu"
   config.database.authInfo["auth1"].user = "<user>"
   config.database.authInfo["auth1"].password = "<password>"
   config.database.authInfo["auth1"].port = 3306

You will also need to create a ``db-auth.paf`` file, because the ``pex_persistence`` package hasn't been updated to use Config.  This file also belongs in ``$HOME/.lsst``, and requires permissions 600.

.. code-block:: yaml

   database: {
       authInfo: {
          host: lsst-dev-db.ncsa.illinois.edu
          port: 3306
          user: <user>
          password: <password>
       }
   }
