Execution Statistics
====================

HTCondor DAGMAN Log Files
-------------------------

The HTCondor DAGMAN utility writes a variety of files to your
:file:`$HOME/condor_scratch` directory.  One of the files is a log of all
processing done through HTCondor.  All log messages are in the form of records,
which are delimited by an ellipses.

Records are delimited with an ellipses. Here is a portion of one of the files,
with "updated", "submitted" and "terminated" records:

.. code-block:: shell

   006 (61916.000.000) 10/04 11:48:51 Image size of job updated: 120060
       0  -  ResidentSetSize of job (KB)
   ...
   000 (61931.000.000) 10/04 11:48:56 Job submitted from host: <141.142.225.136:37267>
       DAG Node: A51
   ...
   005 (62891.000.000) 10/04 12:54:29 Job terminated.
       (1) Normal termination (return value 0)
           Usr 0 00:11:24, Sys 0 00:00:05  -  Run Remote Usage
           Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage
           Usr 0 00:11:24, Sys 0 00:00:05  -  Total Remote Usage
           Usr 0 00:00:00, Sys 0 00:00:00  -  Total Local Usage
       2647  -  Run Bytes Sent By Job
       1912  -  Run Bytes Received By Job
       2647  -  Total Bytes Sent By Job
       1912  -  Total Bytes Received By Job
       Partitionable Resources :    Usage  Request
          Cpus                 :                 1
          Disk (KB)            :       12       12
          Memory (MB)          :               871

**ctrl_stats** package
----------------------

The **ctrl_stats** package contains commands to ingest Condor log files into a
database by taking the event "records" HTCondor emits during execution. The
utilities group all of these records according to Condor job id in order to get
an overview of what happened during the job. These records are then reduced
into two tables, one that describes each submitted dag node and one that
describes all of the events that happens to each condor job id. Note that the
dag node can be submitted more than one time for a variety of reasons. All of
this information is captured in the database records.  Note that you have to
have database write capabilities to execute the ingest command.echo

The following commands are available:

:command:`condorLogIngest.py`
    Takes a list of log files and ingests them into a database 

    .. code-block:: shell

       usage: condorLogIngest.py [-h] -H HOST [-p PORT] -d DATABASE -f FILENAMES [FILENAMES ...] [-v]

    example:

    .. prompt:: bash

       cd ~/condor_scratch/srp_2012_1211_090023
       condorLogIngest.py -H lsst10 -p 3600 -d testing -f logs/worker-pre.log

:command:`condorDirectoryIngest.py`
    Given a directory in ``~/condor_scratch``, take the preJob, worker and
    postJob log files and add them into a database named after the directory.
     
    .. code-block:: shell

       usage: condorDirectoryIngest -H HOST -p PORT -d directory

    example:

    .. prompt:: bash

       cd ~/condor_scratch
       condorDirectoryIngest -H lsst10 -p 3600 -d srp_2012_0925_160117

:command:`condorLogInfo.py`
    A debugging utility to view record groups. This was used as a debugging
    tool, but is useful in viewing records without having to do a complete
    database ingest.

    .. code-block:: shell

       usage: condorLogInfo.py [-h] [-v] [-c CONDORIDS [CONDORIDS ...]] -f FILENAMES [FILENAMES ...]

    example:

    .. prompt:: bash

       cd ~/condor_scratch
       condorLogInfo.py -c 630.000.000 -f srp_2012_0925_160117/*nodes.log

Record Groups
-------------

The are examples of how these individual records are grouped:

Job was executing, increase it's image size to 118472, and was evicted because
job id 68101 (the dagman job which submitted this dag) was removed.

.. code-block:: shell

   Submitted 2012-10-18 16:54:01 jobNum=68103.000.000 dagNode=A1
   Executing 2012-10-18 16:54:03 host=198.202.102.162:53706
   Updated 2012-10-18 16:54:12 imageSize=118472
   Evicted 2012-10-18 16:57:04
   Aborted 2012-10-18 16:57:04 	removed because <OtherJobRemoveRequirements = DAGManJobId == 68101> fired when j

Job was submitted, but never executed, and was evicted when the dagman job was removed.

.. code-block:: shell

   Submitted 2012-10-18 16:57:02 jobNum=68247.000.000 dagNode=A145
   Aborted 2012-10-18 16:57:03 	removed because <OtherJobRemoveRequirements = DAGManJobId == 68101> fired when j

Job was submitted, executed, updated its image size to 117796, then again
updated it's image size to 689000, and terminated.

.. code-block:: shell

   Submitted 2012-10-03 10:57:10 jobNum=59179.000.000 dagNode=A1078
   Executing 2012-10-03 10:57:12 host=198.202.101.70:58180
   Updated 2012-10-03 10:57:21 imageSize=117796
   Updated 2012-10-03 11:02:22 imageSize=689000
   Terminated 2012-10-03 11:07:49

Job was submitted, executed on node 198.202.100.66, updated its image size to
100916, then again to 891028, communication to the node was lost, reconnection
failed once, executing started on node 198.202.100.198, and then terminated.

.. code-block:: shell

   Submitted 2012-10-04 09:39:07 jobNum=60540.000.000 dagNode=A6
   Executing 2012-10-04 09:39:28 host=198.202.100.66:39897
   Updated 2012-10-04 09:39:36 imageSize=100916
   Updated 2012-10-04 09:44:36 imageSize=891028
   SocketLost 60540.000.000 2012-10-04 09:53:55
   SocketReconnectFailure 60540.000.000 2012-10-04 10:13:55
   Executing 2012-10-04 10:13:58 host=198.202.100.198:43111
   Terminated 2012-10-04 10:25:29

Submitted, executing on node 198.202.101.206, updated to image size 119476, an
exception in the Shadow daemon occurs, execution starts on 198.202.101.110,
updated image size to 102492, and then again to 682660, disconnected from node,
reconnection to node failed, execution starts on 198.202.101.185, and then
terminates.

.. code-block:: shell

   Submitted 2012-10-04 09:41:41 jobNum=60660.000.000 dagNode=A126
   Executing 2012-10-04 09:42:08 host=198.202.101.206:51636
   Updated 2012-10-04 09:42:17 imageSize=119476
   ShadowException 60660.000.000 2012-10-04 09:48:18
   Executing 2012-10-04 09:48:45 host=198.202.101.110:48658
   Updated 2012-10-04 09:48:53 imageSize=120492
   Updated 2012-10-04 09:54:24 imageSize=682660
   SocketLost 60660.000.000 2012-10-04 09:56:47
   SocketReconnectFailure 60660.000.000 2012-10-04 10:16:47
   Executing 2012-10-04 10:16:52 host=198.202.101.185:60256
   Terminated 2012-10-04 10:29:13

Database Table Formats
----------------------

Nodes Table
^^^^^^^^^^^

The following is the definition of the nodes table which **ctrl_stats** writes
into:

.. code-block:: shell

   CREATE TABLE IF NOT EXISTS `nodes` (
     `id` int(11) unsigned NOT NULL auto_increment,
     `condorId` varchar(24) default NULL,
     `dagNode` varchar(10) default NULL,
     `submitTime` datetime default NULL,
     `executionHost` varchar(24) default NULL,
     `executionStartTime` datetime default NULL,
     `executionStopTime` datetime default NULL,
     `updateImageSize` int(11) default NULL,
     `updateMemoryUsageMB` int(11) default NULL,
     `updateResidentSetSizeKB` int(11) default NULL,
     `userRunRemoteUsage` int(11) default NULL,
     `sysRunRemoteUsage` int(11) default NULL,
     `finalMemoryUsageMB` int(11) default NULL,
     `finalMemoryRequestMB` int(11) default NULL,
     `bytesSent` int(11) default NULL,
     `bytesReceived` int(11) default NULL,
     `terminationTime` datetime default NULL,
     `terminationCode` varchar(3) default NULL,
     `terminationReason` varchar(4096) default NULL,
     PRIMARY KEY  (`id`)
   ) ENGINE=MyISAM DEFAULT CHARSET=latin1;

- condorId - the number Condor assigns for this job
- dagNode - the DAGMan node name associated with this job
- submitTime - the time that DAGMan submitted this job to Condor
- executionHost - The host on which this job started executing. This may be
  blank if the job was never executed.
- executionStartTime - The time at which this job started executing. This may
  be listed as "0000-00-00 00:00:00" if the job was never started.
- executionStopTime - The time at which this job stop executing. This may be
  listed as "0000-00-00 00:00:00" if the job did not terminate normally.
- updateImageSize - Condor can sometimes send out information about the
  imageSize of the job. This is the last updated received before the job ended.
  This may be 0.
- updateMemoryUsageMB - In updates, Condor sometimes adds additional
  information about the memory usage in MB. This may be 0, if this information
  is not reported.
- updateResidentSetSizeKB - in updates, Condor sometimes adds additional
  information about the portion of the process's memory that is held in RAM.
  This may be 0, if this information is not reported.
- userRunRemoteUsage - At termination, the amount of remote user time that this
  job took to execute.
- sysRunRemoteUsage - At termination, the amount of remote system time that
  this job took to execute. 
- finalMemoryUsageMB - At termination, the last reported memory usage statistic
  reported by Condor
- finalMemroryRequestMB - At termination, the last reported memory request
  statistic reported by Condor. This may be 0.
- bytesSent - the number of bytes set to this job.
- bytesReceived - the number of bytes received from this job.
- terminationTime - The time recorded for this job's termination.
- terminationCode - The Condor event code for this terminated job.
- terminationReason - The text description reported by Condor as the reason for
  this job's termination.

Event Code Table
^^^^^^^^^^^^^^^^

Each time Condor outputs a record it puts out an event code.

.. table:: Condor exit codes.

   =========  =======================================
   eventCode  eventName
   =========  =======================================
      000     Job submitted                          
      001     Job executing                          
      002     Error in executable                    
      003     Job was checkpointed                   
      004     Job evicted from machine               
      005     Job Terminated                         
      006     Image size of job updated              
      007     Shadow exception                       
      008     Generic log event                      
      009     Job aborted                            
      010     Job was suspended                      
      011     Job was unsuspended                    
      012     Job was held                           
      013     Job was released                       
      014     Parallel node executed                 
      015     Parallel node terminated               
      016     POST script terminated                 
      017     Job submitted to Globus                
      018     Globus submit failed                   
      019     Globus resource up                     
      020     Detected Down Globus Resource          
      021     Remote error                           
      022     Remote system call socket lost         
      023     Remote system call socket reestablished
      024     Remote system call reconnect failure   
      025     Grid Resource Back Up                  
      026     Detected Down Grid Resource            
      027     Job submitted to grid resource         
      028     Job ad information event was triggered 
      029     The job's remote status is unknown     
      030     The job's remote statis is known again 
      031     unused                                 
      032     unused                                 
      033     Attribute update                       
   =========  =======================================

