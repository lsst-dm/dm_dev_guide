#########################################
Data Access: Storage Locations and Butler
#########################################

This document describes the file systems available at the LSST Data Facility.

Storage Locations
=================

Personal space:
 - Home directory space is available at /sdf/home/<first_letter_of_account>/<account> - standard S3DF personal allocation (25 GB)
 - Rubin-allocated space: /sdf/group/rubin/u/<account_name> with a 1 TB quota
 - A scratch directory is auto-created for every SDF account in /sdf/scratch/<account>

Science data under /sdf/group/rubin/:
 - datasets/
 - lsstdata/offline/ (still in prep)
 - repo/
 - ncsa_home - copy of NCSA home directories (in prep, setting permissions)
 - ncsa_jhome - copy of NCSA RSP home directories (in prep, setting permissions)
 
 Shared stack builds
  - /sdf/group/rubin/software/
  
Interim while NCSA data is being placed at SLAC
 - SDF Lustre is separate from s3df filesystems. Access the Lustre filesystem via ``/fs/ddn/sdf/`` to access your SDF home directories, sandbox and scratch files
 - datasets and repo/main are read-only, with the exception of repo/main_20220411, which is live and in use for HSC reprocessing

Butler access
=============

The USDF butler can be accessed at https://usdf-butler.slac.stanford.edu

As of this writing, authentication is via vault, but is being transitioned to access by existing per-user credentials. The actual url is hidden in the db-auth.yaml files.

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
