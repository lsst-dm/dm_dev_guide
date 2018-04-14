###################
LDF Storage Resources 
################### 

There are a few other documents that might have the info you are looking for.  

- 1.  Look to the - :doc:`data_protection` policy page what the retention policy is, what are immutable files, what is to be placed in each file system area.  
- 2.  Look to the - :doc:`ldf-resources` LDF resources pages for explaination of each of the file systems, and the type of data and where it's to be located and the policies of each of the file systems.   

- This document covers the file systems, and then quotas for currently only the /home file system that is in place.  

Filesystems - in GPFS (4.9PB of storage) 
========================================

- ``/datasets`` - Long term storage of project-approved shared data. Contains immuteable data. This is under a disaster recovery policy that every 30 days it is stored and written to nearline tape.   
- ``/home`` - Storage of individual-user data. This data is backed up on a daily basis and ncsa retains 30 days of those backups in a snapshot.  It does have quotas on this file system for 1TB for each "directory", and a 1 million INODE quota.  
- ``/software`` - Central location for maintenance of project-shared software installations that require access from multiple resources. (ie batch, Nebula).
- ``/sui`` - Shared storage for ephemeral data for the purpose of supporting SUI/T in the PDAC enclave. This file system has no backups or purging.  
- ``/scratch`` - Ephemeral big-data storage for use in computation and other project-related activities. This is not backed up.  This file system is purged.   Every 30 days a purge policy deleteing files over 180 days.    
- ``/project`` - Long term big-data storage for use in computation and other project-related activities. This is backed up with 7 days of snapshots.  This file system is not subject to purge.  



- Quotas 
- ======
- Your home directory is the default directory you are placed in when you log on. You should use this space for storing files you want to keep long term such as source code, scripts, etc. Every user has a 1TB home directory quota (total space) and 1 million INODE quota (total number of files).

- On **TIME**, quotas were enforced. The soft limit is 1TB and the hard limit is 1.2 TB. The INODE soft quota is 1 million files and the hard limit is 1.2 million files.   If the amount of data in your home directory is over the soft limit  but under the hard limit, there is a grace period of 7 days to get under the soft limit. When the grace period expires, you will not be able to write new files or update any current files until you reduce the amount of data to below the soft limit.

- The command to see your disk usage and limits is quota. Example:

    [jdoe@golubh4 ~]$ quota
    Directories quota usage for user jdoe:

    - -------------------------------------------------------------------------------------
    - |      Fileset       |  Used   |  Soft   |  Hard   |   Used   |   Soft   |   Hard   |
    - |                    |  Block  |  Quota  |  Limit  |   File   |   Quota  |   Limit  |
     --------------------------------------------------------------------------------------
    - | home               | 501.1M  | 2G      | 4G      | 14       | 0        | 0        |
    - | cse-shared         | 0       | 1.465T  | 1.953T  | 1        | 0        | 0        |
    - -------------------------------------------------------------------------------------

Home directories are backed up using snapshots and a separate DR process.

Possible help for space utiziation:  Data Compression
To reduce space usage in your home directory, an option for files that are not in active use is to compress them. The gzip utility can be used for file compression and decompression. Another alternative is bzip2, which usually yields a better compression ratio than gzip but takes longer to complete. Additionally, files that are typically used together can first be combined into a single file and then compressed using the tar utility.

Examples:

Compress a file largefile.dat using gzip:
gzip largefile.dat
The original file is replaced by a compressed file named largefile.dat.gz
To uncompress the file:
gunzip largefile.dat.gz (or:   gzip -d largefile.dat.gz)
To combine the contents of a subdirectory named largedir and compress it:
tar -zcvf largedir.tgz largedir
[convention is to use extension .tgz in the file name]
Note: If the files to be combined are in your home directory and you are close to the quota, you can create the tar file in the scratch directory (since the tar command may fail prior to completion if you go over quota):

tar -zcvf ~/scratch/largedir.tgz largedir
To extract the contents of the compressed tar file:
tar -xvf largedir.tgz
See the manual pages (man gzip, man bzip2, man tar) for more details on these utilities.

Notes:

ASCII text and binary files like executables can yield good compression ratios. Image file formats (gif, jpg, png, etc.) are already natively compressed so further compression will not yield much gains.
Depending on the size of the files, the compression utilities can be compute intensive and take a while to complete. Use the compute nodes via a batch job for compressing large files.
With gzip, the file is replaced by one with the extension .gz. When using tar the individual files remain - these can be deleted to conserve space once the compressed tar file is created successfully.
Use of tar and compression could also make data transfers between the Campus Cluster and other resources more efficient.
