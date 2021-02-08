##############################
Interim Data Facility Overview
##############################

Pre-operations activities may be carried out on Interim Data Facility (IDF) hosted on `Google Cloud Platform <https://cloud.google.com/>`_.
The `Google Cloud documentation site <https://cloud.google.com/docs/overview>`_ provides an overview of its products and services.

IDF is considered a production environment to support Data Preview releases.
Development and Commissioning work continue on `LDF <../services/lsst-devl.rst>`_.


Login credentials
=================

Rubin staff working on deploying and operating Data Production services receives a ``username@lsst.cloud`` identity.
This IDF cloud identity is not an email and is independent from other Rubin accounts.
Not everybody in the Data Production department needs this login; contact your pre-operations team leads if in doubt.

2FA is required for the IDF identity.
See :ref:`idf-internal-support` for lost password or login issues.


Environments
============

On GCP, resources are organized into a base-level entity called "project".
A project is linked to billing, permissions, and other settings.
Projects are grouped in folders.
We have six top-level folders:

- ``Science Platform``
- ``QServ``
- ``Processing``
- ``SQuaRE``
- ``Shared Services``
- ``Scratch``

For each top-level folders except ``Shared Services`` and ``Scratch``, we have three sub-folders: ``Dev``, ``Integration``, and ``Production``.
``Production`` is intended to host services used by end users.
``Dev`` and ``Integration`` provide testing and staging environments where one can deploy near-production services.

All environments on IDF are managed with `Terraform <https://www.terraform.io/>`_ infrastructure-as-code tool in the `idf_deploy <https://github.com/lsst/idf_deploy>`_ repo.
See the documentations in `idf_deploy <https://github.com/lsst/idf_deploy>`_'s `run book <https://github.com/lsst/idf_deploy/tree/master/runbook>`_.
GitHub Actions are used to automatically deploy GCP resources on IDF.
All resources should be deployed via `idf_deploy <https://github.com/lsst/idf_deploy>`_ or layers on top of it, so operations can be repeated consistently.


The only exception to using `idf_deploy <https://github.com/lsst/idf_deploy>`_ is the ``Scratch`` folder.
Projects inside the ``Scratch`` folder are for short lived testing or cloud training; they may be removed with a short notice.
Contact your pre-operations team leads if your work requires a scratch project.

By default, the ``us-central1`` region should be used.

Permissions
===========

Permissions are managed via Google Groups configured in the `idf_deploy <https://github.com/lsst/idf_deploy>`_ repo.
Group memberships are managed manually by the administrators.
See :ref:`idf-internal-support` for requesting to be added to an existing group.

Monitoring
==========

A number of dashboards have been configured and they are viewable in Cloud Monitoring; see `Monitoring and Logging in the run book <https://github.com/lsst/idf_deploy/blob/master/runbook/monitoring-logging.md>`_.

.. _idf-internal-support:

Support (interim)
=================

Questions can be sent to the #ops-google-idf Slack channel.
For requests or infrastructure service issues, file a `JIRA <https://jira.lsstcorp.org/>`_ ticket, add the ``idf`` label, and mention the ticket in the #ops-google-idf Slack channel.
Infrastructure issues will be redirected to Google Support.
See `Google's Best practices on ticketing issues <https://cloud.google.com/support/docs/best-practice>`_.
