###################################################################
Using the HTCondor DAC Cluster
###################################################################

NCSA hosts a few of `HTCondor <https://research.cs.wisc.edu/htcondor/>`_ clusters for LSST. Of particular interest to LSST DM developers will be:

- ``HTCondor DAC Cluster`` - general user HTCondor pool
- ``HTCondor Prod Cluster`` - HTCondor pool for formal data products

This page is designed primarily to assist users of the ``HTCondor DAC Cluster``.

#. :ref:`condor-overview`
#. :ref:`condor-connect`
#. :ref:`condor-config`
#. :ref:`condor-status`
#. :ref:`condor-submit`
#. :ref:`condor-workflow`


.. _condor-overview:

Overview of the HTCondor DAC Cluster
====================================

.. ATTENTION:: Access to the ``HTCondor DAC Cluster`` is currently limited to select users and the cluster is currently small in size compared to the :doc:`Slurm Verification Cluster <verification>`. Access to the ``HTCondor DAC Cluster`` will be opened up to the LSST developer community as a whole (and the cluster will be scaled) as batch workflows are updated to utilize Gen3 middleware. But if you have an interest in using the ``HTCondor DAC Cluster`` sooner please `file a JIRA ticket <https://jira.lsstcorp.org/secure/CreateIssueDetails!init.jspa?pid=12200&issuetype=10901&priority=10000&customfield_12211=12223&components=14213>`_ in the IT Helpdesk Support (IHS) project.

The ``HTCondor DAC Cluster`` has the following submit (schedd) nodes from which users can submit jobs and run workflows:

- ``lsst-condordac-sub01.ncsa.illinois.edu``

In the near future it will also be possible to submit standalone jobs from the :doc:`lsst-login <lsst-login>` nodes. (Please do not run workflows outside of HTCondor on the ``lsst-login`` nodes; e.g., do not run Dask workflows on the login nodes.)

The ``HTCondor DAC Cluster`` also has a number of dedicated compute (startd) nodes configured with partitionable slots. Commands such as those described below in :ref:`condor-status` can be used to view the resources available in the cluster.

The nodes in the cluster utilize the General Parallel File System (GPFS) to provide shared storage across all of the nodes. Please see :doc:`Storage Resources <storage>` for more information.

Report system issues by `filing a JIRA ticket <https://jira.lsstcorp.org/secure/CreateIssueDetails!init.jspa?pid=12200&issuetype=10901&priority=10000&customfield_12211=12223&components=14205>`_ in the IT Helpdesk Support (IHS) project.


.. _condor-connect:

Connecting and Authenticating
=============================

The ``HTCondor DAC Cluster`` submit nodes can be accessed after first connecting to the :doc:`lsst-login <lsst-login>` nodes. Once connected to an ``lsst-login`` node a user can connect to a submit node via its short hostname (e.g., ``lsst-condordac-sub01``) without having to enter a password (Kerberos authentication should be used by default).

For various suggestions on streamlining connections through the ``lsst-login`` nodes ("jump host" configurtaion, port forwarding, Kerberos) see :doc:`related documentation <lsst-login>`.

In order to use HTCondor commands on the submit nodes you must have a valid Kerberos ticket. The following commands may be helpful in working with Kerberos tickets on the submit nodes:

.. code-block:: text

    # list current Kerberos tickets
    $ klist

    # renew your current Kerberos ticket
    $ kinit -R

    # create a new Kerberos ticket
    $ kinit

If you using an ``lsst-login`` node as a "jump host" and are authenticating to an ``HTCondor DAC Cluster`` submit node using a Kerberos ticket from your local machine (workstation/laptop), you may not have a Kerberos ticket when you arrive on the submit node itself. You can ``kinit`` on the submit node as described. Alternatively may wish to configure ``GSSAPIDelegateCredentials yes`` in your local ``~/.ssh/config`` file in order to forward your Kerberos credentials to the submit node and automatically create a ticket there upon connection.


.. _condor-config:

HTCondor Configuration
======================

The ``HTCondor DAC Cluster`` has intentionally been configured to be somewhat like a traditional "batch" compute cluster. This makes it a little less traditional in relation to a typical HTCondor pool. In particular:

- nodes are organized into Nodesets (queues/partitions)
- jobs can be submitted to a particular Nodeset (a default Nodeset is applied if the user does not specify one)
- jobs are submitted with a Walltime (a default Walltime is set if the user does not specify one; a maximum Walltime is configured per Nodeset)
- jobs are scheduled according to the default/requested Walltime; jobs that exceed their promised Walltime are killed
- maintenance reservations can be set to facilitate preventing jobs from running during a full outage of the system

That being said, the ``HTCondor DAC Cluster`` is different from a traditional batch cluster, and HTCondor is different from Slurm, in various ways. Users familiar with HTCondor should find that they can submit jobs to the ``HTCondor DAC Cluster`` and expect it to behave largely like a standard HTCondor pool. Submitting a job without specifying a Nodeset or Walltime should result in the job running in the main (NORMAL) set of nodes with the long, default Walltime (3 days) essentially acting as a failsafe.

Note that MPI is not explicitly supported on the ``HTCondor DAC Cluster``. This cluster is intended for use with Gen3 LSST middleware (rather than Gen2).

Compute (startd) Slots
----------------------

Compute nodes are configured with partitionable slots. This means that the compute resources (CPUs and RAM) can be subdivided continuously and allocated according to the resources requested by jobs in the queue.

Submit (schedd) nodes also each have a subset of their own CPU and RAM resources dedicated to a partitionable compute (startd) slot. This is to allow for local, priority execution of processes associated with job workflows.

Jobs can also be submitted to run in the Scheduler Universe (#7) on each submit (schedd) node. Default and maximum Walltime are currently not set for jobs submitted in the Scheduler Universe (#7).

.. NOTE:: Use of the Scheduler Universe should be limited to workflow management processes. Such jobs would manage the sequence and execution of other "payload" job but would themselves be largely idle most of the time, despite potentially running for days.

Job submission from the :doc:`lsst-login <lsst-login>` nodes will soon be possible. The ``lsst-login`` nodes do not have any startd slots nor do they accept submission to the Scheduler or Local Universes (#7 & #12). (The ``lsst-login`` nodes are **not** intended to support long-running compute processes.)

Nodeset Details
---------------

Compute (startd) slots are organized by "Nodeset" (queue/partition) as follows:

``NORMAL``:

- default Nodeset
- longer Walltime (def: 3 days; max: 30 days)

``DEBUG``:

- for short jobs w/ more immediate start time
- shorter Walltime (30 min)

<schedd> e.g., ``lsst-condordac-sub01``:

- a submit node's Nodeset is equal to its short hostname
- for local, priority job execution (for workflows)
- longer Walltime (same as ``NORMAL``)

Shared and Local Storage
------------------------

The nodes in the ``HTCondor DAC Cluster`` all have access to the :doc:`GPFS shared filesystem <storage>` (including /datasets, /home, /project, /scratch, /software).

The HTCondor LOCAL_DIR mostly lives on local disk on each node. Notably the SPOOL sub-directory on each submit node takes advantage of a fast SSD RAID for better performance. (``lsst-login`` nodes will have much smaller and somewhat slower SPOOL directories. More involved HTCondor work should be submitted from the dedicated submit nodes.) The EXECUTE (job scratch) directory is located in GPFS scratch space in order to provide plenty of space.

The /tmp directory on each submit node is moderate in size. GPFS scratch space should be used when significant, temporary space is needed on submit nodes. (``lsst-login`` nodes have much smaller and somewhat slower /tmp directories.) Also note that /tmp is mapped into the HTCondor EXECUTE (job scratch) directory within Vanilla Universe (default, #5) jobs, so utilizing local /tmp storage on compute (startd) nodes will generally not be an option.

Viewing Configuration Details
-----------------------------

The configuration of any HTCondor node can be viewed with the ``condor_config_val`` command, e.g.:

.. code-block:: text

    # config for the local node
    $ condor_config_val -dump

    # config for another node in the pool
    $ condor_config_val -name nodename -dump

    # view the value of a particular parameter (in this case the next maintenance scheduled in HTCondor)
    $ condor_config_val NEXTMAINTENANCE


.. _condor-status:

Status of Jobs, Slots, and Schedd Queues
========================================

In HTCondor jobs are submitted as/grouped into clusters. A job submitted individually simply forms a cluster of one. Below ``JobID`` may be of the form ``ClusterID`` or ``ClusterID.ProcessID``.

The following commands can be run from submit nodes to check the status of the queue and jobs:

.. code-block:: text

    # show queued and running jobs submitted from the submit (schedd) node you are on
    $ condor_q

    # show queued and running jobs submitted from **all** submit (schedd) nodes in the pool
    $ condor_q -global

    # show only queued/running jobs owned by a particular user
    $ condor_q [-global] <owner>

    # show running jobs including where they are running
    $ condor_q [-global] -run

    # show stats on running/recent jobs for each submit (schedd) node
    $ condor_status -run

    # list status of all startd slots
    $ condor_status

    # see which nodes "are willing to run jobs now"
    $ condor_status -avail

    # show more detailed information (job ClassAds) for queued and running jobs
    $ condor_q -l [<JobID>|<owner>]

    # show specific fields for queued/running jobs
    ## a particularly useful example for the HTCondor DAC Cluster might be as follows
    $ condor_q -l [-global] [<JobID>|<owner>] -af Nodeset RemoteHost Walltime PromisedWalltime

    # see jobs on hold (and optionally see reason)
    $ condor_q -hold [<JobID>|<owner>] [-af HoldReason]

    # see status info for queued/running jobs
    $ condor_q [<JobID>|<owner>] -an|-analyze|-bet|-better-analyze [-verb|-verbose]

    # investigate machine requirements as compared to a job
    ## it is highly advised to narrow to a single slot so the output is more manageable
    $ condor_q -bet|-better-analyze [-verb|-verbose] [<jobID>|<owner>] -rev|-reverse [-mach|-machine <FQDN|slotname>]
 
    # view all slots on a node (including dynamic slots that have been allocated from partionable slots)
    $ condor_status -l <short_hostname>

    # view detailed information about a particular slot
    $ condor_status -l <slotID@full_hostname>

    # view job history
    $ condor_history


.. _condor-submit:

Job Submission
==============

Jobs can be submitted with the ``condor_submit`` command. ``man condor_submit`` provides detailed information and there are many tutorials available on the web. But we can provide some very basic usage here.

Details of the job request are usually provided in a "submit description file". Here this file will be called ``job.submit``. Our other submission materials will be an executable script (``test.sh``) and an input file (``test.in``). These look like this:

.. code-block:: text

    # contents of "job.submit" file

    executable = test.sh
    arguments = test.in 20 $(ClusterId).$(ProcId)
    log = job.log.$(ClusterId).$(ProcId)
    output = job.out.$(ClusterId).$(ProcId)
    error = job.err.$(ClusterId).$(ProcId)
    request_cpus = 1
    request_memory = 1G
    queue 1

    # contents of "test.sh" file
    INPUT=$1
    SLEEP=$2
    JOBID=$3

    cat $INPUT
    hostname
    date
    echo "JobID = $JOBID"
    echo "sleeping $SLEEP"
    sleep $SLEEP
    date

    # contents of "test.in" file
    this is my input

The above job description file could be used in job submission as follows:

.. code-block:: text

    $ condor_submit job.submit

This would result in a job being queued and (hopefully) running. In this case it ran with JobID = 63.0 and resulted with an output file ``job.out.63.0`` with the following contents:

.. code-block:: text

    # contents of job.out.63.0
    this is my input
    lsst-verify-worker40
    Tue Apr 14 11:53:31 CDT 2020
    JobID = 63.0
    sleeping 20
    Tue Apr 14 11:53:52 CDT 2020

It also produced a ``job.err.63.0`` file (empty) and a ``job.log.63.0`` file (containing detailed information from HTCondor about the job's lifecycle and resource utilization).

Elements from the job description file can also generally be specified at the command line instead. For instance, if we were to omit ``queue 1`` from the above job description file, the job could still be submitted as follows:

.. code-block:: text

    $ condor_submit job.submit -queue 1

Again, ``man condor_submit`` offers more detailed information on this.

Nodeset and Walltime
--------------------

In the ``HTCondor DAC Cluster`` there are two additional custom parameters that a user might want to specify for their jobs:

``Nodeset``: By default ``NORMAL`` is used but this can be explicitly specified or overridden at submission. Available Nodesets are discussed in above in :ref:`condor-config`.

``Walltime``: Request a Walltime in seconds. Default and maximum Walltimes for each Nodeset are also discussed above.

These would be specified in a job description file as follows:

.. code-block:: text

    ...
    +Nodeset="DEBUG"
    +Walltime=600
    ...

The above submits to the ``DEBUG`` Nodeset with a Walltime of 600 seconds.

Or at the command line:

.. code-block:: text

    $ condor_submit job.submit -append '+Nodeset="lsst-condordac-sub01"' -append '+Walltime=7200'

The above submits to the ``lsst-condordac-sub01`` Nodeset (that is, the partitionable slot local to that submit node) with a Walltime of 7200 seconds.

SSH to Running Job
------------------

It is possible to SSH into the allocated slot of a running job as follows:

.. code-block:: text

    $ condor_ssh_to_job <JobID>

Interactive Job
---------------

An interactive (SSH only) job can be requested as follows:

.. code-block:: text

    $ condor_submit -i
    Submitting job(s).
    1 job(s) submitted to cluster 85.
    Welcome to slot1_1@lsst-verify-worker40.ncsa.illinois.edu!
    You will be logged out after 7200 seconds of inactivity.

This will allocate a job/slot with a single CPU and a minimal amount of RAM and start a terminal session in that slot as soon as the job starts.

Note that the automatic logout after inactivity is in addition to our Walltime enforcement. That is, your job may still hit its promised Walltime and be killed even without even reaching an inactive state.

Additional resources could be requested as follows:

.. code-block:: text

    # contents of simple submit description file "int.submit"
    request_cpus = 4
    request_memory = 16G
    queue 1

    # job submission command
    $ condor_submit -i int.submit
    ...

It is also possible to request additional resources at the command line as follows:

.. code-block:: text

    $ condor_submit -append request_cpus=4 -append request_memory=16G -i


.. _condor-workflow:

Running Workflows
=================

Workflow managers such as Dask and Pegasus can be used to launch jobs in the ``HTCondor DAC Cluster``. The following ports have been set aside to support Dask workflows in particular but could be utilized for similar purposes:

- 20000-20999: Dask dashboard (Bokeh server), JupyterLab, etc. - these ports are open between all workers (compute nodes) and to/from workers and submit nodes
- 29000-29999: Dask scheduler and Dask worker processes - these ports are not open but processes that need to listen locally for this type of purpose should be configured to use this range/a port within this range
