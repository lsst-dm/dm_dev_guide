###########################
Overall Resources 
###########################

These are the resources in a list form that are currently (8/10/2020) available to lsst developers.  


1. :ref:`Machines on the floor <machines>`.
2. :ref:`Storage filesystems <filesystems>`.


.. _machines:

Machines:  (includes VM and Baremetal)
======================================

- :doc:`lsst-login</services/lsst-login>` - login nodes, "jump" host to get into the NCSA lsst infrasturcture environment
- lsst-web - web services machine 
- VM server machines - running VMware vSphere software.   (@ NCSA 3003, NCSA NPCF) 
   - virtual machines for numberous development environments 
   - databackbone test beds, container type test beds, demo type machines, monitoring machines 
- lsst-demo - VM for demos and docker image needs 
- ATS gateway - VM
- DAQ - camera simulator systems 
- L1 test stand - collection of machines for simulating and testing the camera software 
- ATS archiver - Auxiliary Telecope Archiver system 
- Slurm Batch cluster - 48 compute nodes for processing DRP and other compute needs 
- Kubernetes (K8s) - 20 compute nodes for containers 
- Oracle Rac - 6 nodes for the consolidated DB 
- PDAC - 35 compute nodes for QSERV and SUI systems 
- Backup - machines dedicated for data movement to and from DR 
- Xcat and Puppet configuration management machines
- DTN nodes - data transfer nodes, 2 compute nodes 
- Monitor DB node and other infrastucture machines (influxDB, loghost...) 
- identity.lsst.org - reset and password machine 
- network emulator - latency injection environment for simulating the roundtrip to Chile and back in networks.
- Bro cluster - networking scanning software/hardware (Chile Base) 
- NCSA provided shared resources : 
     -Jira, LDAP (ncsa3003, ncsanpcf, Chile base, chile summit), kerberos, IDM, Qualys scans for security, Nearline tape, and Firewall systems, Bro clusters (network scanning security) 
 

.. _filesystems:

Filesystems - in GPFS (4.9PB of storage) 
========================================

- ``/datasets`` - Long term storage of project-approved shared data, primarily precursor and simulated datasets. Contains immutable data. This is under a disaster recovery policy that every 30 days it is stored and written to nearline tape.
- ``/lsstdata`` - Long term storage of LSST project data, including production, engineering, and test stand datasets. Contains immutable data. This is under a disaster recovery policy.
- ``/home`` - Storage of individual-user data. This data is backed up on a daily basis and ncsa retains 30 days of those backups in a snapshot.  It does have quotas on this file system for 1TB for each "directory", and a 1 million INODE quota.  
- ``/software`` - Central location for maintenance of project-shared software installations that require access from multiple resources. (ie batch, Nebula).
- ``/sui`` - Shared storage for ephemeral data for the purpose of supporting SUI/T in the PDAC enclave. This file system has no backups or purging.  
- ``/scratch`` - Ephemeral big-data storage for use in computation and other project-related activities. This is not backed up.  This file system is purged.   Every 30 days a purge policy deleteing files over 180 days.    
- ``/project`` - Long term big-data storage for use in computation and other project-related activities. This is backed up with 7 days of snapshots.  This file system is not subject to purge.  
