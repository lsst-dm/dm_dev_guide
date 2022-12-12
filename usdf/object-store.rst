#########################
Data Access: Object Store
#########################

Some data at the USDF is stored in S3-compatible object stores.
In most cases, access to them is via the Data Butler and transparent to users.
This document describes techniques for advanced direct usage of the object stores.

Storage Locations
=================

All object stores currently use a single S3 endpoint: ``https://s3dfrgw.slac.stanford.edu``.
This is typically pointed to by the ``S3_ENDPOINT_URL`` environment variable.
Eventually the production embargo storage is expected to have its own endpoint.

Within that endpoint, there are many available buckets.
Some of them are listed below.

Embargo storage
---------------

These buckets hold the raw images from the Summit and the processed data products derived from them (``-users``) during the embargo period.
There is one set for each test stand in addition to the production set for the Summit.

- rubin-summit
- rubin-summit-users
- rubin-bts
- rubin-bts-users
- rubin-tts
- rubin-tts-users

Other object stores
-------------------

Prompt Processing development uses a pair of buckets to act as its "central store" and raw image storage (simulating the embargo production storage) as well as another bucket to hold test data.

- rubin-pp
- rubin-pp-users
- rubin-prompt-processing-test

Other development and production buckets, typically devoted to a single application and not guaranteed to maintain a consistent organization, may exist.


Credentials
===========

The default set of credentials for read-only access to the embargo raw data buckets and for read-write access to the embargo ``-users`` buckets is most easily retrieved by logging into the USDF RSP and starting a notebook server.
Starting the server will create or overwrite the ``~/.lsst/aws-credentials.ini`` file; the credentials will be set as the default profile in this file.
The RSP and the default scripts executed by .bashrc upon ssh login will set the ``AWS_SHARED_CREDENTIALS_FILE`` environment variable to point to this file.

To use additional non-default profiles, you should copy the ``aws-credentials.ini`` file elsewhere (to avoid overwriting by the USDF RSP) and add the profiles to it.
You will then need to manually set the ``AWS_SHARED_CREDENTIALS_FILE`` environment variable to point to the new location, in addition to the ``AWS_PROFILE`` variable to select a profile.

Read/write credentials for other buckets are stored in ``vault.slac.stanford.edu``; requests for access should go to Slack channel ``#ops-usdf``.


Access Methods
==============

Python
------

The simplest mechanism for access is to use the Data Butler where available.

Next simplest when using the LSST Science Pipelines is to use `lsst.resources.ResourcePath <https://pipelines.lsst.io/v/daily/py-api/lsst.resources.ResourcePath.html>`__.
This class allows easy switching between ``file://`` URLs for filesystem paths and ``s3://`` URLs for object store paths.

For even lower-level access, the ``boto3`` package included in ``rubin-env`` is suggested.

Command line
------------

The AWS command line client can be accessed via a Singularity/Apptainer container.

.. code-block:: bash

   alias s3api='singularity exec /sdf/sw/s3/aws-cli_latest.sif aws --endpoint-url https://s3dfrgw.slac.stanford.edu s3api'
 
This command defines an alias to run the container, executing the ``aws`` command line client with the proper endpoint URL and pre-selecting the S3 API.

Another alternative is to install the single-executable-file MinIO command line client ``mc``.
See the `installation and usage documentation <https://min.io/docs/minio/linux/reference/minio-mc.html>`__ for more details.
Note that ``mc`` generally requires credentials to be placed in ``~/.mc/config.json`` (although there is an environment variable option that should only be used for containerized services).
