#################
Storage Resources
#################

This document describes the file systems available at the LSST Data Facility during the interim period where the Rubin filesystems at SLAC go into production mode on our own hardware, and while user and project data are being transferred from NCSA.

A sandbox area has been created at:

/sdf/group/rubin/sandbox/

with access control via the rubin_users unix group. Currently it is unregulated. Once the data transfers are done from NCSA, a more familiar filetree will be available.

Home directory space is available at /sdf/home/<first_letter_of_account>/<account>

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
