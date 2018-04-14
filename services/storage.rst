3. Storage
Home Directory
Your home directory is the default directory you are placed in when you log on. You should use this space for storing files you want to keep long term such as source code, scripts, etc. Every user has a 2 GB home directory quota.

On Monday December 9, 2013 at 7 a.m. CT, quotas were enforced. The soft limit is 2 GB and the hard limit is 4 GB. Once quotas are enforced, if the amount of data in your home directory is over the soft limit of 2 GB but under the hard limit of 4 GB, there is a grace period of 7 days to get under the soft limit. When the grace period expires, you will not be able to write new files or update any current files until you reduce the amount of data to below 2 GB.

The command to see your disk usage and limits is quota. Example:

    [jdoe@golubh4 ~]$ quota
    Directories quota usage for user jdoe:

    -------------------------------------------------------------------------------------
    |      Fileset       |  Used   |  Soft   |  Hard   |   Used   |   Soft   |   Hard   |
    |                    |  Block  |  Quota  |  Limit  |   File   |   Quota  |   Limit  |
    -------------------------------------------------------------------------------------
    | home               | 501.1M  | 2G      | 4G      | 14       | 0        | 0        |
    | cse-shared         | 0       | 1.465T  | 1.953T  | 1        | 0        | 0        |
    -------------------------------------------------------------------------------------

Home directories are backed up using snapshots.
Scratch Directory
The scratch filesystem is shared storage space available to all users. It is intended for short term use and should be considered volatile. No backups of any kind are performed for this storage. There is a soft link named scratch in your home directory that points to your scratch directory.

Scratch Purge Policy:

All files located in scratch (/scratch/users) that are older than 30 days will be purged (deleted).
Project Space
For investors that have project space (/projects/investor_group_name), usage and quota information is available with the command:


    [golubh1 ~]$ projectquota <project_directory_name>

Please consult with your investor technical representative regarding availability and access.

Snapshots
Nightly snapshots of the home and project filesystems are available for the last 30 days in the following locations:

Home Directory:

        /gpfs/iccp/home/.snapshots/home_YYYYMMDD*/$USER

Investor Project Directory:

        /gpfs/iccp/projects/<project_directory_name>/.snapshots/<project_directory_name>_YYYYMMDD*
Note: Since snapshots are created nightly, there is a window of time between snapshots when recent file changes are NOT recoverable if accidentally deleted, overwritten, etc.

No off-site backups for disaster recovery are provided for any storage. Please make sure to do your own backups of any important data on the Campus Cluster to permanent storage as often as necessary.

Data Compression
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
