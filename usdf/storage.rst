#########################################
Data Access: Storage Locations and Butler
#########################################

This document describes the file systems available at the LSST Data Facility.

Storage Locations
=================

Personal space:
 - Home directory space is available at /sdf/home/<first_letter_of_account>/<account> - standard S3DF personal allocation (25 GB)
 - Rubin-allocated space: /sdf/group/rubin/u/<account_name> with a 1 TB quota
 
Web space:
 - "public_html" web access is available upon request: it will be visible at https://s3df.slac.stanford.edu/people/<user>
 - send email to usdf-help at slac.stanford.edu requesting a personal web directory
 - a public_html directory will be created in your home directory after acknowledging a usage policy
 - note that this is for static pages - no server-side content.
 - no symlinks outside public_html will be followed.

Science data under /sdf/group/rubin/:
 - datasets/
 - lsstdata/offline/ (still in prep)
 - repo/
 - g/shared/data/{test,validation}_data - daily updated checkouts of git lfs repos for use in testing code
 - ncsa_home - copy of NCSA home directories (in prep, setting permissions)
 - ncsa_jhome - copy of NCSA RSP home directories (in prep, setting permissions)
 
 Shared stack builds
  - /sdf/group/rubin/sw/
  
Interim while NCSA data is being placed at SLAC
 - SDF Lustre is separate from s3df filesystems. Access the Lustre filesystem via ``/fs/ddn/sdf/`` to access your SDF home directories, sandbox and scratch files
 - datasets and repo/main are read-only, with the exception of repo/main_20220411, which is live and in use for HSC reprocessing

Butler access
=============

The primary Butler repos are located at ``/sdf/group/rubin/repo/main_20210215`` and ``/sdf/group/rubin/repo/dc2_20210215``.
They can also be accessed via aliases ``/repo/main`` and ``/repo/dc2``.

The USDF butler Registry can be accessed at ``usdf-butler.slac.stanford.edu``.

As of this writing, authentication is by a single account and password. It will be set up for you automatically once you log in to RSP once, creating a .lsst/postgres-credentials.txt file. You wil need to fire up a notebook server while on RSP.

Data Transfer Tools
===================

SLAC supports bbcp and Globus. For now, see the s3df documentation:

https://s3df.slac.stanford.edu/public/doc/#/data-transfer

(it is expected that the s3df endpoint will be established close to Aug 15)

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
