##############################
Interim Data Facility Overview
##############################

Pre-operations activities may be carried out on the Interim Data Facility (IDF) hosted on the `Google Cloud Platform <https://cloud.google.com/>`_.
The `Google Cloud documentation site <https://cloud.google.com/docs/overview>`_ provides an overview of its products and services.

The IDF is considered a production environment to support Data Preview releases.
Development and Commissioning work continue on the Construction-funded `LSST Data Facility (LDF) <../services/lsst-devl.rst>`_.


Login credentials
=================

Rubin staff working on deploying and operating Data Production services receive a ``username@lsst.cloud`` identity.
This IDF cloud identity is not an email and is independent from other Rubin accounts.
Not everybody in the Data Production department needs this login; contact your pre-operations team lead(s) if in doubt.

Two-factor authentication (2FA) is required for the IDF identity.
See :ref:`idf-internal-support` for lost password or login issues.


Environments
============

On GCP, resources are organized into a base-level entity called a "project".
A project is linked to billing, permissions, and other settings.
Projects are grouped in folders.
We have six top-level folders:

- ``Science Platform``
- ``QServ``
- ``Processing``
- ``SQuaRE``
- ``Shared Services``
- ``Scratch``

For each top-level folder except ``Shared Services`` and ``Scratch``, we have three sub-folders: ``Dev``, ``Integration``, and ``Production``.
``Production`` is intended to host services used by end users.
``Dev`` and ``Integration`` provide testing and staging environments where one can deploy near-production services.

All environments on IDF are managed with `Terraform <https://www.terraform.io/>`_, an infrastructure-as-code tool, via configuration files in the `idf_deploy <https://github.com/lsst/idf_deploy>`_ repo.
See the documentation in idf_deploy's `run book <https://github.com/lsst/idf_deploy/tree/main/runbook>`_.
GitHub Actions are used to automatically deploy GCP resources on IDF in response to pull requests on the configuration files.
All resources should be deployed this way so that operations can be repeated consistently.


The only exception to using `idf_deploy <https://github.com/lsst/idf_deploy>`_ is the ``Scratch`` folder.
Projects inside the ``Scratch`` folder are for short-lived testing or cloud training; they may be removed on short notice.
No user-facing services should live in the ``Scratch`` folder.
Contact your pre-operations team lead(s) if your work requires a scratch project.

All IDF resources should live in the ``us-central1`` region.

Permissions
===========

Permissions are managed via Google Groups configured in the `idf_deploy <https://github.com/lsst/idf_deploy>`_ repo.
Group memberships are managed manually by the administrators.
See :ref:`idf-internal-support` to request to be added to an existing group.

Monitoring
==========

A number of dashboards have been configured in Cloud Monitoring; for more information, see `Monitoring and Logging in the run book <https://github.com/lsst/idf_deploy/blob/main/runbook/monitoring-logging.md>`_.

.. _idf-internal-support:

Support (interim)
=================

Questions can be sent to the `#ops-google-idf <https://lsstc.slack.com/archives/CC82DT23Y>`_ Slack channel.
For requests or infrastructure service issues, file a `JIRA <https://jira.lsstcorp.org/>`_ DM ticket, add the ``idf`` label, and mention the ticket in the #ops-google-idf Slack channel.
Infrastructure issues will be redirected to Google Support.
See `Google's Best practices on ticketing issues <https://cloud.google.com/support/docs/best-practice>`_.
