#########################################
Data Access: Storage Locations and Butler
#########################################

This document describes the file systems available at the LSST Data Facility.

Storage Locations
=================

Personal space:
 - Home directory space is available at ``/sdf/home/<first_letter_of_account>/<account>`` - standard S3DF personal allocation (25 GB)
 - Rubin-allocated space: ``/sdf/data/rubin/user/<account_name>`` with a 1 TB quota (a symlink to this directory, called ``rubin-user``, is auto-created in your home directory). If you need more space, request it in ``#ops-usdf``, and a ticket will get opened to request the quota increase.
 
Web space:
 - "public_html" web access is available upon request: it will be visible at ``https://s3df.slac.stanford.edu/people/<user>``
 - send email to ``usdf-help`` at ``slac.stanford.edu`` requesting a personal web directory
 - a ``public_html`` directory will be created in your home directory after acknowledging a usage policy
 - note that this is for static pages - no server-side scripting.
 - no symlinks outside ``public_html`` will be followed.

Science data under ``/sdf/group/rubin/``:
 - Much of this is still disorganized and contains vestiges of the structure from NCSA that was moved to USDF.  Bear with us until we get it all straightened out.
 - ``shared/`` contains various datasets for common usage.
   - ``shared/data-repos.yaml`` contains the list of aliases for Butler repos.
   - ``shared/data/test_data`` contains daily-updated test datasets.
   - ``shared/data/validation_data`` contains daily-updated validation datasets.
   - Other requested storage for particular groups or external datasets is also located under ``/sdf/group/rubin/shared/``.
   - Request new shared storage via ``#ops-usdf``, providing the name, purpose, storage quota needed, and owner.  Storage will generally be given group ``rubin_users``, giving all staff access; this can be read-only or read-write as desired.
 - ``repo/`` contains Butler repo configurations.  See the next section.
 - ``sw/`` contains the "shared stack" of LSST Science Pipelines software.
 
Butler access
=============

Butler repo configurations for most repos are located under ``/sdf/group/rubin/repo/``, but we define aliases for them as a convenience.
A few Butler repos that use S3 object stores have their configuration files defined there, also with convenience aliases.

Available Butler repos:
   - ``main`` - All images taken of the real sky by HSC, DECam, LATISS, LSSTComCam, and LSSTCam and data products derived from them.  (This repo only contains post-embargo images for the Rubin cameras.)
   - ``embargo`` - Embargoed data from Summit cameras (located in the Embargo Rack).  After the embargo period, images and other data products in this repo will be copied to ``main`` and/or ``prompt``.  After a further delay, they will be removed from this repo.
   - ``prompt`` - Summit camera raw images and data products published as nightly post-embargo data products for LSST data rights holders.
   - ``dp1_prep`` - Preparatory repo for the Data Release Production for the Data Preview 1 release.
   - ``dp1`` - Official repo with the final DP1 contents.
   - ``dc2`` - DESC DC2 simulated LSSTCam.
   - ``ir2`` - LSSTCam and TS8 data taken at SLAC during testing.
   - ``bts`` - Equivalent of ``embargo`` for the Base Test Stand (located in the Embargo Rack).
   - ``tts`` - Equivalent of ``embargo`` for the Tucson Test Stand (not located in the Embargo Rack).
   - ``ops-rehearsal-3-prep`` - Images and data products used to prepare for Ops Rehearsals 3 and 4.  Data products generated as a result of the Ops Rehearsals are elsewhere, starting in ``/repo/embargo``..
   - ``hsc_pdr2_multisite`` - Special campaign for testing multi-site Data Release Production (DRP).  (Does not have an alias defined.)
   - Future DRPs such as DP2, DR1, etc. will go into distinct Butler repos, one for preparation and one with the final published release.

The USDF butler Registry can be accessed at ``usdf-butler.slac.stanford.edu``.

As of this writing, authentication to the Butler repos is by a single shared account and password. It will be set up for you automatically once you log in to the USDF RSP and start a notebook server. This will create ``~/.lsst/postgres-credentials.txt`` and ``~/.lsst/aws-credentials.ini`` files.
Certain services use distinct service accounts for Butler repo access.

Requests for outages of the Butler repos should be handled by the `USDF outage process <https://confluence.lsstcorp.org/display/LSSTOps/USDF+Outage+Planning>`__.


Data Transfer Tools
===================

SLAC supports bbcp and Globus. For now, see the s3df documentation:

https://s3df.slac.stanford.edu/public/doc/#/data-transfer

Data transfer nodes are available at s3dfdtn.slac.stanford.edu.

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
