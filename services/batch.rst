############################
Using the LSST Batch Systems
############################

NCSA hosts a few `HTCondor <https://research.cs.wisc.edu/htcondor/>`_ clusters and a `Slurm <https://slurm.schedmd.com/overview.html>`_ cluster for LSST. Of particular interest to LSST DM developers will be:

- ``HTCondor DAC Cluster`` - general user HTCondor pool
- ``HTCondor Prod Cluster`` - HTCondor pool for formal data products
- ``Slurm Cluster`` - general use Slurm cluster (replaces legacy Slurm "verification cluster")

This page is designed primarily to assist users of the ``HTCondor DAC Cluster`` and ``Slurm Cluster``.

#. :ref:`batch-overview`
#. :ref:`batch-connect`
#. :ref:`batch-gpfs`
#. :ref:`batch-stack`
#. :ref:`batch-condor`
#. :ref:`batch-slurm`


.. _batch-overview:

LSST Batch Systems: Overview
============================

THe ``HTCondor DAC Cluster`` has the following submit (schedd) nodes from which users can submit jobs and run workflows:

- ``lsst-condordac-sub01.ncsa.illinois.edu``
- ``lsst-condordac-sub02.ncsa.illinois.edu``

The ``HTCondor DAC Cluster`` also has a number of dedicated compute (startd) nodes configured with partitionable slots. Commands such as those described below in :ref:`batch-condor` can be used to view the resources available in the cluster.

Access to the ``HTCondor Prod Cluster`` is restricted to users working formal data products. It has the following dedicated submit (schedd) nodes:

- ``lsst-condorprod-sub01.ncsa.illinois.edu``

Jobs can be submitted to the ``Slurm Cluster`` from any of the above submit nodes.

Report system issues by `filing a JIRA ticket <https://jira.lsstcorp.org/secure/CreateIssueDetails!init.jspa?pid=12200&issuetype=10901&priority=10000&customfield_12211=12223&components=14205>`_ in the IT Helpdesk Support (IHS) project.


.. _batch-connect:

LSST Batch Systems: Connecting and Authenticating
=================================================

The batch submit nodes can be accessed after first connecting to the :doc:`lsst-login <lsst-login>` nodes. Once connected to an ``lsst-login`` node a user can connect to a submit node via its short hostname (e.g., ``lsst-condordac-sub01``) without having to enter a password (Kerberos authentication should be used by default; if your Kerberos ticket expires on the login node you may need to ``kinit`` again before proceeding to the submit node).

For various suggestions on streamlining connections through the ``lsst-login`` nodes ("jump host" configuration, port forwarding, Kerberos) see :doc:`related documentation <lsst-login>`.

In order to use HTCondor commands on the submit nodes you must have a valid Kerberos ticket. The following commands may be helpful in working with Kerberos tickets on the submit nodes:

.. code-block:: text

    # list current Kerberos tickets
    $ klist

    # renew your current Kerberos ticket
    $ kinit -R

    # create a new Kerberos ticket
    $ kinit

If you using an ``lsst-login`` node as a "jump host" and are authenticating to a submit node using a Kerberos ticket from your local machine (workstation/laptop), you may not have a Kerberos ticket when you arrive on the submit node itself. You can ``kinit`` on the submit node as described. Alternatively may wish to configure ``GSSAPIDelegateCredentials yes`` in your local ``~/.ssh/config`` file in order to forward your Kerberos credentials to the submit node and automatically create a ticket there upon connection.


.. _batch-gpfs:

LSST Batch Systems: GPFS Directory Spaces
=========================================

The nodes in the batch clusters utilize the General Parallel File System (GPFS) to provide shared storage across all of the nodes.

For convenience the bind mounts  :file:`/scratch` , :file:`/project` , :file:`/datasets` ,  and :file:`/software`  have been created to provide views into corresponding spaces in GPFS.

Please see :doc:`Storage Resources <storage>` for more general information.

To add/change/delete datasets, see :doc:`Common Dataset Organization and Policy </services/datasets>`.


.. _batch-stack:

LSST Batch Systems: Shared Software Stack in GPFS
=================================================
A shared software stack on the GPFS file systems, suitable for computation on the
``Verification Cluster``, has been provided and is maintained by Science Pipelines and
is available under :file:`/software/lsstsw`.  This stack may be initialized via:  ::

     % .  /software/lsstsw/stack/loadLSST.bash


.. _batch-condor:

HTCondor Usage
==============


HTCondor: Overview
------------------

The ``HTCondor DAC Cluster`` and ``HTCondor Prod Cluster`` have intentionally been configured to be somewhat like traditional "batch" compute clusters. This makes them a little less traditional in relation to typical HTCondor pools. In particular:

- nodes are organized into Nodesets (equivalent to queues or partitions)
- jobs can be submitted to a particular Nodeset (a default Nodeset is applied if the user does not specify one)
- jobs are submitted with a Walltime (a default Walltime is set if the user does not specify one; a maximum Walltime is configured per Nodeset)
- jobs are scheduled according to the default/requested Walltime; jobs that exceed their promised Walltime are killed
- maintenance reservations can be set to facilitate preventing jobs from running during a full outage of the system

That being said, the ``HTCondor DAC Cluster`` and ``HTCondor Prod Cluster`` are different from a traditional batch cluster, and HTCondor is different from Slurm, in various ways. Users familiar with HTCondor should find that they can submit jobs to these clusters and expect them to behave largely like standard HTCondor pools. Submitting a job without specifying a Nodeset or Walltime should result in the job running in the main (NORMAL) set of nodes with the long, default Walltime (3 days) essentially acting as a failsafe.

NOTE: Walltime policies are somewhat more relaxed on the ``HTCondor Prod Cluster``.

NOTE: MPI is not explicitly supported on the ``HTCondor DAC Cluster`` and ``HTCondor Prod Cluster``. These clusters are intended for use with Gen3 LSST middleware (rather than Gen2).

Report system issues by `filing a JIRA ticket <https://jira.lsstcorp.org/secure/CreateIssueDetails!init.jspa?pid=12200&issuetype=10901&priority=10000&customfield_12211=12223&components=14205>`_ in the IT Helpdesk Support (IHS) project.


HTCondor: Compute (startd) Slots
--------------------------------

The HTCondor compute nodes are configured with partitionable slots. This means that the compute resources (CPUs and RAM) can be subdivided continuously and allocated according to the resources requested by jobs in the queue.

The submit (schedd) nodes also each have a subset of their own CPU and RAM resources dedicated to a partitionable compute (startd) slot. This is to allow for local, priority execution of processes associated with job workflows.

Jobs can also be submitted to run in the Scheduler Universe (#7) on each submit (schedd) node. Default and maximum Walltime are currently not set for jobs submitted in the Scheduler Universe (#7).

.. NOTE:: Use of the Scheduler Universe should be limited to workflow management processes. Such jobs would manage the sequence and execution of other "payload" job but would themselves be largely idle most of the time, despite potentially running for days.


.. _batch-condor-nodesets:

HTCondor: Nodeset Details
-------------------------

Compute (startd) slots are organized by "Nodeset" (queue/partition) as follows:

``NORMAL``:

- default Nodeset
- longer Walltime (def: 3 days; max: 30 days)
- NOTE: there is no default walltime for the ``NORMAL`` Nodeset on the ``HTCondor Prod Cluster``

``DEBUG``:

- for short jobs w/ more immediate start time
- shorter Walltime (30 min)
- NOTE: there may not be any nodes in the DEBUG nodeset during the earlier stages of our migration from Slurm to HTCondor

``<schedd>`` e.g., ``lsst-condordac-sub01``:

- a submit node's Nodeset is equal to its short hostname
- for local, priority job execution (for workflows)
- longer Walltime (same as ``NORMAL``)
- NOTE: there are no default or maximum walltimes for the ``<schedd>`` Nodesets on the ``HTCondor Prod Cluster``


HTCondor: Shared and Local Storage
----------------------------------

The nodes in the ``HTCondor DAC Cluster`` and ``HTCondor Prod Cluster`` all have access to the :doc:`GPFS shared filesystem <storage>` (including /datasets, /home, /project, /scratch, /software).

The HTCondor LOCAL_DIR mostly lives on local disk on each node. Notably the SPOOL sub-directory on each submit node takes advantage of a fast SSD RAID for better performance. The EXECUTE (job scratch) directory is located in GPFS scratch space in order to provide plenty of space.

The /tmp directory on each submit node is moderate in size. GPFS scratch space should be used when significant, temporary space is needed on submit nodes. Also note that /tmp is mapped into the HTCondor EXECUTE (job scratch) directory within Vanilla Universe (default, #5) jobs, so utilizing local /tmp storage on compute (startd) nodes will generally not be an option.


HTCondor: Viewing Configuration Details
---------------------------------------

The configuration of any HTCondor node can be viewed with the ``condor_config_val`` command, e.g.:

.. code-block:: text

    # config for the local node
    $ condor_config_val -dump

    # config for another node in the pool
    $ condor_config_val -name nodename -dump

    # view the value of a particular parameter (in this case the next maintenance scheduled in HTCondor)
    $ condor_config_val NEXTMAINTENANCE


HTCondor: Status of Jobs, Slots, and Schedd Queues
--------------------------------------------------

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


HTCondor: Job Submission
------------------------

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


HTCondor: Nodeset and Walltime
------------------------------

The ``HTCondor DAC Cluster`` and ``HTCondor Prod Cluster`` have two custom parameters that a user might want to specify for their jobs:

``Nodeset``: By default ``NORMAL`` is used but this can be explicitly specified or overridden at submission. Available Nodesets are discussed above at :ref:`batch-condor-nodesets`.

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


HTCondor: SSH to Running Job
----------------------------

It is possible to SSH into the allocated slot of a running job as follows:

.. code-block:: text

    $ condor_ssh_to_job <JobID>


HTCondor: Interactive Job
-------------------------

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


HTCondor: Running Workflows
---------------------------

Workflow managers such as Dask and Pegasus can be used to launch jobs in the ``HTCondor DAC Cluster`` and ``HTCondor Prod Cluster``. The following ports have been set aside to support Dask workflows in particular but could be utilized for similar purposes:

- 20000-20999: Dask dashboard (Bokeh server), JupyterLab, etc. - these ports are open between all workers (compute nodes) and to/from workers and submit nodes
- 29000-29999: Dask scheduler and Dask worker processes - these ports are not open but processes that need to listen locally for this type of purpose should be configured to use this range/a port within this range


.. _batch-slurm:

Slurm Usage
===========


Slurm: Overview
---------------

The ``Slurm Cluster`` is a cluster of servers run by NCSA for LSST DM development work. It uses `Slurm <https://slurm.schedmd.com/overview.html>`_ for scheduling and resource management.

Submit nodes for the ``Slurm Cluster`` are listed above at :ref:`batch-overview`. Users can submit jobs to Slurm from any of the submit nodes.

Users can view the compute resources available in the ``Slurm Cluster`` using commands such as `sinfo -Nl`, `scontrol show part`, and `scontrol show node`.

The nodes in the ``Slurm Cluster`` all have access to the :doc:`GPFS shared filesystem <storage>` (including /datasets, /home, /project, /scratch, /software).

Report system issues by `filing a JIRA ticket <https://jira.lsstcorp.org/secure/CreateIssueDetails!init.jspa?pid=12200&issuetype=10901&priority=10000&customfield_12211=12223&components=14205>`_ in the IT Helpdesk Support (IHS) project.


SLURM: Job Submission
---------------------

Documentation on using SLURM client commands and submitting jobs may be found at standard locations (e.g., a `quickstart guide <http://slurm.schedmd.com/quickstart.html>`_). In addition to the basic SLURM client commands, there are higher level tools that can serve to distribute jobs to a SLURM cluster, with one example being the combination of `pipe_drivers <https://github.com/lsst/pipe_drivers>`_ and `ctrl_pool <https://github.com/lsst/ctrl_pool>`_ within LSST DM. There are also likely updated batch tools available for use with LSST pipelines (although some may be designed for use with HTCondor). For exhaustive documentation and specific use cases, we refer the user to such resources.

On this page we display some simple examples for getting started with submitting jobs to the ``Slurm Cluster``.

The ``Slurm Cluster``is configured with 2 queues (partitions):

   - **normal**: more nodes, no run time limit.  For runs after your code is debugged.  Default.
   - **debug**:  ~1-2 nodes, 30 min run time limit.  For short testing & debugging runs.

The ``normal`` queue is the default, so any ``debug`` jobs will need to be told to run in the debug queue. This can be done by adding ``-p debug`` to your sbatch command line, or adding the following to your job's batch file::

     #SBATCH -p debug

To examine the current state and availability of the nodes in the ``Slurm Cluster``,
one can use the SLURM command  ``sinfo``::

     % sinfo
     PARTITION AVAIL  TIMELIMIT  NODES  STATE NODELIST
     normal*      up   infinite     12  alloc lsst-verify-worker[09-18]
     normal*      up   infinite     2   idle lsst-verify-worker[07-08]
     debug        up      30:00      1 drain* lsst-verify-worker48
     debug        up      30:00      2   idle lsst-verify-worker[46-47]

     % sinfo  -N -l --states="idle"
     Wed Jan 31 10:53:52 2018
     NODELIST              NODES PARTITION       STATE CPUS    S:C:T MEMORY TMP_DISK WEIGHT AVAIL_FE REASON
     lsst-verify-worker07      1   normal*        idle   24   2:12:1 128000        0      1   (null) none
     lsst-verify-worker08      1   normal*        idle   24   2:12:1 128000        0      1   (null) none


In this view ``sinfo`` shows the nodes to reside within a single partition ``debug``, and the worker nodes show 24 possible cores on a node (hyperthreading is disabled).

NOTE: The memory displayed per node by `sinfo` does not accurately reflect what is actually schedulable/usable. Please use `scontrol show partition` do see what is available (look for `MaxMemPerNode`).

The Slurm configuration tracks historical usage but does not perform actual accounting per se (all jobs are submitted without an account), and places no quotas on users' total time usage. Historical usage can be displayed with the `sacct` command.


Slurm: Simple Jobs
------------------

In submitting SLURM jobs to the ``Slurm Cluster`` it is advisable to have the software stack, data, and any utilities stored on the GPFS :file:`/scratch` , :file:`/datasets` , and/or :file:`/software` spaces so that all are reachable from both the submit node and each of the worker nodes.  Some simple SLURM job description files that make use of the ``srun`` command are shown in this section. These are submitted to the queue from a standard login shell on submit node using the SLURM client command ``sbatch``, and their status can be checked with the command ``squeue`` :

For a single task on a single node:

.. code-block:: text

    % cat test1.sl
    #!/bin/bash -l
    #SBATCH -p debug
    #SBATCH -N 1
    #SBATCH -n 1
    #SBATCH -t 00:10:00
    #SBATCH -J job1

    srun sleep.sh


    % cat sleep.sh
    #!/bin/bash
    hostname -f
    echo "Sleeping for 30 ... "
    sleep 30


    Submit with :
    % sbatch test1.sl

    Check status :
    % squeue
        JOBID PARTITION     NAME     USER ST       TIME  NODES NODELIST(REASON)
          109     debug     job1    daues  R       0:02      1 lsst-verify-worker11

This example job was assigned jobid 109 by the Slurm scheduler, and consequently the standard output and error of the job were written to a default file :file:`slurm-109.out` in the current working directory. ::

    % cat slurm-109.out
     lsst-verify-worker11.ncsa.illinois.edu
     Sleeping for 30 ...

To distribute this script for execution to 6 nodes by 24 tasks per node (total 144 tasks), the form of the job description is:

.. code-block:: text

    % cat test144.sl
    #!/bin/bash -l
    #SBATCH -p debug
    #SBATCH -N 6
    #SBATCH -n 144
    #SBATCH -t 00:10:00
    #SBATCH -J job2

    srun sleep.sh


    Submit with :
    % sbatch test144.sl

For these test submissions a user might submit from a working directory in the :file:`/scratch/<username>`  space with the executable script :file:`sleep.sh` and the job description file located in the current working directory.


Slurm: Interactive Jobs
-----------------------

A user can schedule and gain interactive access to ``Slurm Cluster`` compute nodes using the SLURM ``salloc`` command. Example usage is:

For a single node: ::

    % salloc  -N  1 -p debug -t 00:30:00  /bin/bash
    salloc: Granted job allocation 108

    % squeue
             JOBID PARTITION     NAME     USER ST       TIME  NODES NODELIST(REASON)
               108     debug     bash    daues  R       0:58      1 lsst-verify-worker46
    % hostname -f
    lsst-condordac-sub01.ncsa.illinois.edu

    % srun hostname -f
    lsst-verify-worker46.ncsa.illinois.edu

One can observe that after the job resources have been granted, the user shell is still on the login node ``lsst-condordac-sub01``. The command ``srun`` can be utilized to run commands on the job's allocated compute nodes. Commands issued without ``srun``  will still be executed locally on ``lsst-condordac-sub01``.

You can also use ``srun`` without first being allocated resources (via ``salloc``). For example, to immediately obtain a command-line prompt on a compute node: ::

    % srun -I --pty bash


Slurm: Executing Tasks with Different Arguments
-----------------------------------------------

In order to submit multiple tasks that each have distinct command line arguments (e.g., data ids), one can utilize the ``srun`` command with the ``--multi-prog`` option.   With this option, rather than specifying a single script or binary for ``srun`` to execute, a filename is provided as the argument of  the ``--multi-prog`` option. In this scenario an example job description file is:

.. code-block:: text

    % cat test1_24.sl
    #!/bin/bash -l

    #SBATCH -p debug
    #SBATCH -N 1
    #SBATCH -n 24
    #SBATCH -t 00:10:00
    #SBATCH -J sdss24

    srun --output job%j-%2t.out --ntasks=24 --multi-prog cmds.24.conf

This description specifies that 24 tasks will be executed on a single node, and the standard output/error from each of the tasks will be written to a unique filename with format specified by the argument to ``--output``. The 24 tasks to be executed are specified in the file :file:`cmds.24.conf`  provided as the argument to the  ``--multi-prog`` option. This commands file will have a format that maps SLURM process ids (SLURM_PROCID) to programs to execute and their commands line arguments.  An example command file has the form : ::

    % cat cmds.24.conf
    0 /scratch/daues/exec_sdss_i.sh run=4192 filter=r camcol=1 field=300
    1 /scratch/daues/exec_sdss_i.sh run=4192 filter=r camcol=4 field=300
    2 /scratch/daues/exec_sdss_i.sh run=4192 filter=g camcol=4 field=297
    3 /scratch/daues/exec_sdss_i.sh run=4192 filter=z camcol=4 field=299
    4 /scratch/daues/exec_sdss_i.sh run=4192 filter=u camcol=4 field=300
    ...
    22 /scratch/daues/exec_sdss_i.sh run=4192 filter=u camcol=4 field=303
    23 /scratch/daues/exec_sdss_i.sh run=4192 filter=i camcol=4 field=298


The wrapper script :file:`exec_sdss_i.sh` used in this example could serve to
"set up the stack" and place the data ids on the command line of :file:`processCcd.py` : ::

    % cat exec_sdss_i.sh
    #!/bin/bash
    # Source an environment setup script that holds the resulting env vars from e.g.,
    #  . ${STACK_PATH}/loadLSST.bash
    #  setup lsst_distrib
    source /software/daues/envDir/env_lsststack.sh

    inputdir="/scratch/daues/data/stripe82/dr7/runs/"
    outdir="/scratch/daues/output/"

    processCcd.py  ${inputdir}  --id $1 $2 $3 $4 --output ${outdir}/${SLURM_JOB_ID}/${SLURM_PROCID}
