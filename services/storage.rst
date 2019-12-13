#################
Storage Resources
#################

This document describes the file systems available at the LSST Data Facility and their quotas.

There are a few other documents that might have the info you are looking for:

- The :doc:`data_protection` policy page describes what the retention policy is, what are immutable files, what is to be placed in each file system area.
- The :doc:`ldf-resources` LDF resources pages for explanation of each of the file systems, and the type of data and where it's to be located and the policies of each of the file systems.

Filesystems in GPFS (6.3PB of storage)
======================================

:file:`/lsstdata/offline/teststand`
    Long term storage of LSST project data, including production, engineering, and test stand datasets. Contains immutable data. This is under a disaster recovery policy.
    Currently includes :file:`/lsstdata/offline/teststand/auxTel` for datasets from the LATISS/AuxTel test stand in Tucson and :file:`/lsstdata/offline/teststand/BOT` for datasets from the Bench for Optical Testing at SLAC. The former includes read-only Gen2 Butler repositories under :file:`/lsstdata/offline/teststand/auxTel/DAQ/gen2repo` and :file:`/lsstdata/offline/teststand/auxTel/L1Archiver/gen2repo`. These are updated periodically (several times an hour) as data is taken in Tucson.
    A *writable* Gen2 Butler repository for LATISS/AuxTel data with associated calibrations and shared reruns is currently available at :file:`/project/shared/auxTel`.  This repository is what should be used for typical staff analysis.

:file:`/lsstdata/dac/services`
    Storage area for data that is owned primarily by a service running at the DAC (eg. ELK stack, Jenkins, etc.) A fileset for a new service can be requested via an IHS ticket, and will be provisioned by NCSA staff.  If desired a quota can be set on the area to limit the application's file system usage, if desired please note this in the ticket.

:file:`/datasets`
    Long term storage of project-approved shared data. Contains immutable data. This is under a disaster recovery policy that every 30 days it is stored and written to nearline tape.

:file:`/home`
    Storage of individual-user data. This data is backed up on a daily basis and NCSA retains 30 days of those backups in a snapshot.  It does have quotas on this file system for 1TB for each "directory," and a 1 million INODE quota.

:file:`/software`
    Central location for maintenance of project-shared software installations that require access from multiple resources. (i.e., batch, Nebula).

:file:`/sui`
    Shared storage for ephemeral data for the purpose of supporting SUI/T in the PDAC enclave. This file system has no backups or purging.

:file:`/scratch`
    Ephemeral big-data storage for use in computation and other project-related activities. This is not backed up.  This file system is purged.   Every 30 days a purge policy deletes files older than 180 days.

:file:`/project`
    Long term big-data storage for use in computation and other project-related activities. This is backed up with 7 days of snapshots.  This file system is not subject to purge.

Quotas 
======

Your home directory is the default directory you are placed in when you log on. You should use this space for storing files you want to keep long term such as source code, scripts, etc. Every user has a 1TB home directory quota (total space) and 1 million INODE quota (total number of files).

On 6/17/2018, quotas were enforced. The soft limit is 1TB and the hard limit is 1.2 TB. The INODE soft quota is 1 million files and the hard limit is 1.2 million files.   If the amount of data in your home directory is over the soft limit  but under the hard limit, there is a grace period of 7 days to get under the soft limit. When the grace period expires, you will not be able to write new files or update any current files until you reduce the amount of data to below the soft limit.

The command to see your disk usage and limits is :command:`quota`. Example:

.. code-block:: text

   $ quota
   Directories quota usage for user jdoe:

---------------------------------------------------------------
| GPFS Fileset         | Used (GB)  | Quota (GB) | # Of Files |
---------------------------------------------------------------
| home                 | 1          | 1000       | 22,533     |
| jhome                | 0          | 100        | 9          |
| scratch              | 0          | 0          | 2          |
| project              | 0          | 0          | 2          |
---------------------------------------------------------------

Home directories are backed up using snapshots and a separate DR process.

Data compression
================

To reduce space usage in your home directory, an option for files that are not in active use is to compress them. The :command:`gzip` utility can be used for file compression and decompression. Another alternative is :command:`bzip2`, which usually yields a better compression ratio than gzip but takes longer to complete. Additionally, files that are typically used together can first be combined into a single file and then compressed using the tar utility.

Examples
--------

Compress a file :file:`largefile.dat` using :command:`gzip`:

.. code-block:: bash

   gzip largefile.dat

The original file is replaced by a compressed file named :file:`largefile.dat.gz`.

To decompress the file:

.. code-block:: bash

   gunzip largefile.dat.gz

Alternatively:

.. code-block:: bash

   gzip -d largefile.dat.gz

To combine the contents of a subdirectory named :file:`largedir` and compress it:

.. code-block:: bash

   tar -zcvf largedir.tgz largedir

The convention is to use extension ``.tgz`` in the file name.

.. note::

   If the files to be combined are in your :file:`home` directory and you are close to the quota, you can create the ``tar`` file in the :file:`scratch` directory (since the :command:`tar` command may fail prior to completion if you go over quota):

   .. code-block:: bash

      tar -zcvf ~/scratch/largedir.tgz largedir

To extract the contents of the compressed tar file:

.. code-block:: bash

   tar -zxvf largedir.tgz

.. note::

   ASCII text and binary files like executables can yield good compression ratios. Image file formats (gif, jpg, png, etc.) are already natively compressed so further compression will not yield much gains.
   Depending on the size of the files, the compression utilities can be compute intensive and take a while to complete. Use the compute nodes via a batch job for compressing large files.
   With :command:`gzip`, the file is replaced by one with the extension .gz. When using :command:`tar`` the individual files remain --- these can be deleted to conserve space once the compressed tar file is created successfully.
   Use of :command:`tar` and compression could also make data transfers between the Campus Cluster and other resources more efficient.
