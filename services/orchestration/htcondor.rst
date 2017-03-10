Typical HTCondor Commands
=========================

HTCondor has been configured on the local LSST cluster, and can be used to
submit jobs to local resources, or to remote (XSEDE) systems.

There are several commands to be aware of, outlined below:

::command:`condor_q`
    The command shows which jobs are in the queue.  When specified without
    arguments, it shows only jobs submitted from the machine on which the
    command was executed.  Here's an example, run on the machine "lsst-dev":

    .. code-block:: shell

       $ condor_q
       -- Schedd: lsst-dev.ncsa.illinois.edu : <141.142.225.160:37253>

       ID      OWNER            SUBMITTED     RUN_TIME ST PRI SIZE CMD
       7092.0   srp             8/21 09:04   0+03:40:23 R  0   0.3  condor_dagman
       7094.0   srp             8/21 09:05   0+00:43:04 I  0   97.7 matrix.sh visit=88
       7095.0   srp             8/21 09:05   0+00:42:54 I  0   97.7 matrix.sh visit=88
       7096.0   srp             8/21 09:05   0+00:42:54 I  0   97.7 matrix.sh visit=88

       4 jobs; 0 completed, 0 removed, 3 idle, 1 running, 0 held, 0 suspended

:command:`condor_rm`
    You can use :command:`condor_rm` to remove jobs from the queue.  If you
    want to remove job 7096, run:

    .. code-block:: shell

       $ condor_rm 7096
       Cluster 7096 has been marked for removal.
       $ condor_q

       -- Submitter: lsst-dev.ncsa.illinois.edu : <141.142.225.160:37253> : lsst-dev.ncsa.illinois.edu

       ID      OWNER            SUBMITTED     RUN_TIME ST PRI SIZE CMD               
       7092.0   srp             8/21 09:04   0+03:48:26 R  0   0.3  condor_dagman     
       7094.0   srp             8/21 09:05   0+00:43:04 I  0   97.7 matrix.sh visit=88
       7095.0   srp             8/21 09:05   0+00:42:54 I  0   97.7 matrix.sh visit=88
       3 jobs; 0 completed, 0 removed, 2 idle, 1 running, 0 held, 0 suspended

    Usually the :command:`condor_rm` command doesn't instantaneously remove the
    job from the queue; it may take several seconds for it to be removed.

    To remove all the jobs you submitted, use the ``-all`` option:

    .. code-block:: shell

       $ condor_rm -all
       All jobs marked for removal.
       $ condor_q
       -- Submitter: lsst-dev.ncsa.illinois.edu : <141.142.225.160:37253> : lsst-dev.ncsa.illinois.edu
       ID      OWNER            SUBMITTED     RUN_TIME ST PRI SIZE CMD

       0 jobs; 0 completed, 0 removed, 0 idle, 0 running, 0 held, 0 suspended

:command:`condor_status`
    The :command:`condor_status` command shows the status of machines in your
    Condor pool.

    .. code-block:: shell

       $ condor_status
       Name               OpSys      Arch   State     Activity LoadAv Mem   ActvtyTime
       slot1@lsst-run1.nc LINUX      X86_64 Unclaimed Idle     0.000  1916  0+23:05:16
       slot2@lsst-run1.nc LINUX      X86_64 Unclaimed Idle     0.000  1916  0+23:05:19
       slot1@lsst-run2.nc LINUX      X86_64 Unclaimed Idle     0.000  1916 11+01:31:35
       slot2@lsst-run2.nc LINUX      X86_64 Unclaimed Idle     0.000  1916 11+01:31:58

       Total Owner Claimed Unclaimed Matched Preempting Backfill
                X86_64/LINUX     4     0       0         4       0          0        0
                       Total     4     0       0         4       0          0        0

    Further details on Condor, and other commands are available from the
    `HTCondor manual <http://research.cs.wisc.edu/condor/manual>`_.
