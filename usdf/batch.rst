#################
Batch Resources
#################

This document describes the batch resources available at the US Data Facility hosted at the SLAC Shared Scientific Data Facility (S3DF).

Use of S3DF batch is documented at

https://s3df.slac.stanford.edu/

and more general Slurm documentation is available at https://slurm.schedmd.com/.

S3DF has two Slurm partitions ``roma`` and ``milano``. Both of these partitions have AMD nodes with 128 cores, composed of two sockets, each with a 64-core processor (hyperthreading disabled).
A Slurm job can be submitted with markup ``#SBATCH -p roma,milano`` to run on either of the partitions.

For light interactive work, e.g., running *small* ``pipetask`` jobs, one can obtain an interactive session on the batch nodes using ``srun``.  For example,

.. code-block:: bash
   :name: srun-interactive-example

   srun --pty --cpus-per-task=4 --mem=16GB --nodes=1 --time=02:00:00 --partition=roma,milano --account=rubin --qos normal bash 

will create a 2-hour, 4-core bash session with a total of 16GB memory.  Specifying the total memory with ``--mem`` means that the memory can be distributed among the cores as needed, whereas using ``--mem-per-cpu`` sets the memory available for each individual core; and the option ``--nodes=1`` ensures that all of the cores are on the same node.  With this set up, one can then run ``pipetask -j 4``, making use of the 4 allocated cores.  Adding the ``--exclusive`` option will request a whole node, but in that case, one probably should be submitting a non-interactive batch job anyway. The account parameter is mandatory.

Four "repos" have been created to apportion the batch allocation. We have yet to determine the relative allocations per repo - at the time of writing, accounting has not yet been enabled. Repos are selected by appending a ":" with the repo name, eg ``--account rubin:developers``. The non-default repos are not pre-emptible.

- default - always preemptible
- production - PanDA production jobs, eg DRP
- developers
- commissioning

All Rubin account holders can submit to any but the production repo. We will give guidance as it is developed on which to choose.

In general, using BPS is preferred to running ``pipetask`` directly since many concurrent ``pipetask`` jobs that are run like this can cause registry database contention.

Running LSST Pipelines with BPS
===============================
The LSST Batch Processing Service (`BPS <https://github.com/lsst/ctrl_bps>`__) is the standard execution framework for running LSST pipelines using batch resources.  There are a few different plugins to BPS that are available that can be used for running BPS on various computing systems:

- :ref:`ctrl_bps_htcondor <ctrl_bps_htcondor>` 
- ctrl_bps_panda
- :ref:`ctrl_bps_parsl <ctrl_bps_parsl>`

.. _ctrl_bps_htcondor:

ctrl_bps_htcondor 
=================
This section describes how to obtain an `HTCondor <https://htcondor.org>`__ pool in S3DF for use with BPS workflows.  Upon logging in via ``ssh rubin-devl`` to either sdfrome001 or sdfrome002, one can see that htcondor is installed and running, but that no computing slots are available::

   $ condor_q
   -- Schedd: sdfrome002.sdf.slac.stanford.edu : <172.24.33.226:9618?... @ 01/31/23 11:51:35
   OWNER BATCH_NAME      SUBMITTED   DONE   RUN    IDLE   HOLD  TOTAL JOB_IDS

   Total for query: 0 jobs; 0 completed, 0 removed, 0 idle, 0 running, 0 held, 0 suspended
   Total for daues: 0 jobs; 0 completed, 0 removed, 0 idle, 0 running, 0 held, 0 suspended
   Total for all users: 0 jobs; 0 completed, 0 removed, 0 idle, 0 running, 0 held, 0 suspended

   $ condor_status
   $

In order to run BPS workflows via htcondor at S3DF, it is necessary to submit glide-in jobs to the S3DF Slurm scheduler using the ``allocateNodes.py`` utility of the ``ctrl_execute`` package which will reference the ``ctrl_platform_s3df`` package`.
After these two packages are setup the glide-ins may be submitted.

The ``allocateNodes.py`` utility has the following options::

   $ allocateNodes.py --help
    usage: [...]/ctrl_execute/bin/allocateNodes.py [-h] [--auto] -n NODECOUNT -c CPUS [-a ACCOUNT] [-s QOS] 
                                                    -m MAXIMUMWALLCLOCK [-q QUEUE] [-O OUTPUTLOG] 
                                                    [-E ERRORLOG] [-g GLIDEINSHUTDOWN] [-p] [-v]
                                                    [-r RESERVATION] [-d [DYNAMIC]]
                                                    platform

    positional arguments:
      platform              node allocation platform

    options:
      -h, --help            show this help message and exit
      --auto            use automatic detection of jobs to determine glide-ins
      -n NODECOUNT, --node-count NODECOUNT
                        number of glideins to submit; these are chunks of a node, size the number of cores/cpus
      -c CPUS, --cpus CPUS  cores / cpus per glidein
      -a ACCOUNT, --account ACCOUNT
                        Slurm account for glidein job
      -s QOS, --qos QOS     Slurm qos or glidein job
      -m MAXIMUMWALLCLOCK, --maximum-wall-clock MAXIMUMWALLCLOCK
                        maximum wall clock time; e.g., 3600, 10:00:00, 6-00:00:00, etc
      -q QUEUE, --queue QUEUE
                        queue / partition name
      -O OUTPUTLOG, --output-log OUTPUTLOG
                        Output log filename; this option for PBS, unused with Slurm
       -E ERRORLOG, --error-log ERRORLOG
                        Error log filename; this option for PBS, unused with Slurm
       -g GLIDEINSHUTDOWN, --glidein-shutdown GLIDEINSHUTDOWN
                        glide-in inactivity shutdown time in seconds
       -p, --pack       encourage nodes to pack jobs rather than spread
       -v, --verbose    verbose
       -r RESERVATION, --reservation RESERVATION
                        target a particular Slurm reservation
       -d [DYNAMIC], --dynamic [DYNAMIC]
                        configure to use dynamic/partitionable slot; legacy option: this is always enabled now

The ``allocateNodes.py`` utility requires a small measure of configuration in the user's home directory (replace the username ``daues`` with your own)::

   $  cat  ~/.lsst/condor-info.py
   config.platform["s3df"].user.name="daues"
   config.platform["s3df"].user.home="/sdf/home/d/daues"

A typical ``allocateNodes.py`` command line for obtaining resources for a BPS workflow could be::

   $ allocateNodes.py -v --dynamic -n 20 -c 32 -m 4-00:00:00 -q roma,milano -g 900 s3df

``s3df`` is specified as the target platform. 
The ``-q roma,milano`` option specifies that the glide-in jobs may run in either the roma or milano partition. 
The ``-n 20 -c 32`` options request 20 individual glide-in slots of size 32 cores each (each is a Slurm job that obtains a partial node).
The maximum possible time is set to 4 days via ``-m 4-00:00:00``. 
The glide-in Slurm jobs may not run for the full 4 days however, as the option ``-g 900`` specifies a 
condor glide-in shutdown time of 900 seconds or 15 minutes. This means that the htcondor daemons will shut themselves 
down after 15 minutes of inactivity (for example, after the workflow is complete), and the glide-in Slurm jobs 
will exit at that time to avoid wasting idle resources. The ``--dynamic`` option requests that the htcondor slots be dynamic, partionable slots; this is the recommended setting as it supports possible multi-core jobs in the workflow. 

There is support for setting USDF S3DF Slurm account, repo and qos values. By default the account ``rubin`` 
with the ``developers`` repo (``--account rubin:developers``) will be used, and the qos will be ``normal`` by default. 
If one wants to target a different repo, this is 
handled as part of the account setting, placed following a colon after the account value proper, 
e.g., ``--account rubin:commissioning``.  A cautionary note on account and qos values: if one sets 
the fairly benign looking value ``--account rubin``, this will lead to the job having ``preemptable`` qos, 
and the job will be less likely to run to completion without interruption. 

After submitting the ``allocateNodes.py`` command line above, the user may see Slurm jobs and htcondor slots along the lines of::

   $ squeue -u <username>

             JOBID PARTITION     NAME     USER ST       TIME  NODES NODELIST(REASON)
           4246331      roma glide_da    daues  R       0:05      1 sdfrome016
           4246332      roma glide_da    daues  R       0:05      1 sdfrome016
           4246333      roma glide_da    daues  R       0:05      1 sdfrome016
           4246334      roma glide_da    daues  R       0:05      1 sdfrome016
           4246335      roma glide_da    daues  R       0:05      1 sdfrome011
           4246336      roma glide_da    daues  R       0:05      1 sdfrome011
           4246337      roma glide_da    daues  R       0:05      1 sdfrome011
           4246338      roma glide_da    daues  R       0:05      1 sdfrome011
           4246339      roma glide_da    daues  R       0:05      1 sdfrome012
           4246340      roma glide_da    daues  R       0:05      1 sdfrome012
           4246341      roma glide_da    daues  R       0:05      1 sdfrome012
           4246342      roma glide_da    daues  R       0:05      1 sdfrome020
           4246343      roma glide_da    daues  R       0:05      1 sdfrome020
           4246344      roma glide_da    daues  R       0:05      1 sdfrome020
           4246345      roma glide_da    daues  R       0:05      1 sdfrome021
           4246346      roma glide_da    daues  R       0:05      1 sdfrome021
           4246347      roma glide_da    daues  R       0:05      1 sdfrome021
           4246348      roma glide_da    daues  R       0:05      1 sdfrome021
           4246349      roma glide_da    daues  R       0:05      1 sdfrome023
           4246350      roma glide_da    daues  R       0:05      1 sdfrome023
   $ condor_status
   Name                                                OpSys      Arch   State     Activity LoadAv Mem     ActvtyTime

   slot_daues_1455_1@sdfrome011.sdf.slac.stanford.edu  LINUX      X86_64 Unclaimed Idle      0.000 128000  0+00:00:00
   slot_daues_10693_1@sdfrome011.sdf.slac.stanford.edu LINUX      X86_64 Unclaimed Idle      0.000 128000  0+00:00:00
   slot_daues_27645_1@sdfrome011.sdf.slac.stanford.edu LINUX      X86_64 Unclaimed Idle      0.000 128000  0+00:00:00
   slot_daues_32041_1@sdfrome011.sdf.slac.stanford.edu LINUX      X86_64 Unclaimed Idle      0.000 128000  0+00:00:00
   slot_daues_2010_1@sdfrome012.sdf.slac.stanford.edu  LINUX      X86_64 Unclaimed Idle      0.000 128000  0+00:00:00
   slot_daues_24423_1@sdfrome012.sdf.slac.stanford.edu LINUX      X86_64 Unclaimed Idle      0.000 128000  0+00:00:00
   slot_daues_31147_1@sdfrome012.sdf.slac.stanford.edu LINUX      X86_64 Unclaimed Idle      0.000 128000  0+00:00:00
   slot_daues_4125_1@sdfrome016.sdf.slac.stanford.edu  LINUX      X86_64 Unclaimed Idle      0.000 128000  0+00:00:00
   slot_daues_12576_1@sdfrome016.sdf.slac.stanford.edu LINUX      X86_64 Unclaimed Idle      0.000 128000  0+00:00:00
   slot_daues_14984_1@sdfrome016.sdf.slac.stanford.edu LINUX      X86_64 Unclaimed Idle      0.000 128000  0+00:00:00
   slot_daues_25023_1@sdfrome016.sdf.slac.stanford.edu LINUX      X86_64 Unclaimed Idle      0.000 128000  0+00:00:00
   slot_daues_5936_1@sdfrome020.sdf.slac.stanford.edu  LINUX      X86_64 Unclaimed Idle      0.000 128000  0+00:00:00
   slot_daues_12034_1@sdfrome020.sdf.slac.stanford.edu LINUX      X86_64 Unclaimed Idle      0.000 128000  0+00:00:00
   slot_daues_24875_1@sdfrome020.sdf.slac.stanford.edu LINUX      X86_64 Unclaimed Idle      0.000 128000  0+00:00:00
   slot_daues_7366_1@sdfrome021.sdf.slac.stanford.edu  LINUX      X86_64 Unclaimed Idle      0.000 128000  0+00:00:00
   slot_daues_7575_1@sdfrome021.sdf.slac.stanford.edu  LINUX      X86_64 Unclaimed Idle      0.000 128000  0+00:00:00
   slot_daues_9335_1@sdfrome021.sdf.slac.stanford.edu  LINUX      X86_64 Unclaimed Idle      0.000 128000  0+00:00:00
   slot_daues_23816_1@sdfrome021.sdf.slac.stanford.edu LINUX      X86_64 Unclaimed Idle      0.000 128000  0+00:00:00
   slot_daues_18562_1@sdfrome023.sdf.slac.stanford.edu LINUX      X86_64 Unclaimed Idle      0.000 128000  0+00:00:00

               Total Owner Claimed Unclaimed Matched Preempting Backfill  Drain

  X86_64/LINUX    19     0       0        19       0          0        0      0

         Total    19     0       0        19       0          0        0      0

The htcondor slots will have a label with the username, so that one user's glide-ins may be distinguished from another's.  In this case the glide-in slots are partial node 32-core chunks, and so more than one slot can appear on a given node. The decision as to whether to request full nodes or partial nodes would depend on the general load on the cluster, i.e., if the cluster is populated with other numerous single core jobs that partially fill nodes, it will be necessary to request partial nodes to acquire available resources.
Larger ``-c`` values (and hence smaller ``-n`` values for the same total number of cores) will entail less process overhead, but there may be inefficient unused cores within a slot/"node", and slots may be harder to schedule.
We recommend selecting ``-c`` such that ``-n`` is in the range of 1 to 32; ``-c 32`` is often reasonable for jobs using dozens to hundreds of cores.

The ``allocateNodes.py`` utility is set up to be run in a maintenance or cron type manner, where reissuing the exact same command line request for 20 glide-ins will not directly issue 20 additional glide-ins. Rather ``allocateNodes.py`` will strive to maintain 20 glide-ins for the workflow, checking to see if that number of glide-ins are in the queue, and resubmit any missing glide-ins that may have exited due to lulls in activity within the workflow.

With htcondor slots present and visible with ``condor_status``, one may proceed with running ``ctrl_bps`` ``ctrl_bps_htcondor`` workflows in the same manner as was done on the project's previous generation computing cluster at NCSA.

Usage of the ``ctrl_bps_htcondor`` plugin and module has been extensively documented at

https://pipelines.lsst.io/modules/lsst.ctrl.bps.htcondor/userguide.html

For running at S3DF, the following ``site`` specification can be used in the BPS configuration file:

.. code-block:: yaml
   :name: bps-htcondor-site-config

   site:
     s3df:
       profile:
         condor:
           +Walltime: 7200

allocateNodes auto
------------------

The ``ctrl_execute`` package now provides an ``allocateNodes --auto`` mode in which the user does not have to specify the number of glideins to run. This mode is not the default, and must be explicitly invoked. In this mode the user's idle jobs in the htcondor queue will be detected and an appropriate number of glideins submitted. At this stage of development the allocateNodes auto is used in conjuction with a bash script that runs alongside a BPS workflow, workflows, or generic HTCondor jobs.  The script will invoke allocateNodes auto at regular intervals to submit the number of glideins needed by the workflow(s) at the particular time.  A sample ``service.sh`` script is::

    #!/bin/bash
    export LSST_TAG=w_2023_46
    lsstsw_root=/sdf/group/rubin/sw
    source ${lsstsw_root}/loadLSST.bash
    setup -v lsst_distrib -t ${LSST_TAG}
 
    # Loop for a long time, executing "allocateNodes auto" every 10 minutes.
    for i in {1..500}
    do
        allocateNodes.py --auto --dynamic --qos normal --account rubin:developers -n 100 -c 16 -m 4-00:00:00 -q milano -g 240 s3df
        sleep 600
    done

On the allocateNodes auto command line the option ``-n 100`` no longer specifies the desired number of glideins, but rather specifies an upper bound. There are two time scales in the script above, the first is the glidein shutdown with inactivity time ``-g 240``. This can be fairly short (here 240 seconds / four minutes) to avoid idle cpus, since new glideins will be resubmitted for the user if needed in later cycles. The second time scale is the sleep time ``sleep 600``. This provides the frequency with which to run allocateNodes, and a typical time scale is 600 seconds / ten minutes. With each invocation queries are made to the htcondor schedd and the Slurm scheduler, so it is best not run with unnecessary frequency. Each invocation of allocateNodes queries the htcondor schedd on the current development machine (e.g., ``sdfrome002``). 

After the workflow is complete all of the glideins will expire and the ``service.sh`` process can be removed with Ctrl-C, killing the process, etc.  If a user has executed a ``bps submit`` and acquired resources via the ``service.sh`` / ``allocateNodes`` and everything is running, but then wishes to terminate everything, how best to proceed? A good path is to issue a ``bps cancel``, which would take the precise form ``bps cancel --id <condor ID or path to run submit dir (including timestamp)>``. After the cancel all htcondor jobs will be terminated soon, and the glideins will become idle and expire shortly after the glidein shutdown time with inactivity. The last item that might remain is to stop the ``service.sh`` script, as described above.  For the future we are investigating if BPS itself can manage the allocateNodes auto invocations that a workflow requires, eliminating the need for the user to manage the ``service.sh`` script. 

.. _ctrl_bps_parsl:

ctrl_bps_parsl
==============
The `ctrl_bps_parsl <https://github.com/lsst/ctrl_bps_parsl/>`__ package uses the `Parsl parallel programming library <https://parsl-project.org/>`__ to enable running on HPC resources.  This plugin can also be configured for running on a single node, such as a laptop, which is useful for testing and development.  An `earlier version <https://github.com/LSSTDESC/gen3_workflow/>`__ of this plugin was developed by DESC and has been used extensively by DESC at `NERSC <https://www.nersc.gov/>`__, `CC-IN2P3 <https://cc.in2p3.fr/en/>`__, and `CSD3 <https://www.hpc.cam.ac.uk/high-performance-computing>`__ for running the LSST Science Pipelines at scale.  The ctrl_bps_parsl package `README <https://github.com/lsst/ctrl_bps_parsl#readme>`__ has further details about the history, development, and usage of this plugin.   The `README  <https://github.com/lsst/ctrl_bps_parsl#readme>`__ also has instructions for installing Parsl for use with the LSST Science Pipelines code.

There are nominally four different site configuration classes in ctrl_bps_parsl that can be used for running BPS jobs on the SLAC S3DF cluster.  Here is an example BPS configuration file that illustrates possible configurations for each one:

.. code-block:: yaml
   :name: bps-parsl-config-example

   pipelineYaml: "${DRP_PIPE_DIR}/ingredients/LSSTCam-imSim/DRP.yaml"

   wmsServiceClass: lsst.ctrl.bps.parsl.ParslService
   computeSite: local

   parsl:
     log_level: INFO

   site:
     local:
       class: lsst.ctrl.bps.parsl.sites.Local
       cores: 8
     slurm:
       class: lsst.ctrl.bps.parsl.sites.Slurm
       nodes: 2
       walltime: 2:00:00     # This is 2 hours
       cores_per_node: 100
       qos: normal
       scheduler_options: |
         #SBATCH --partition=roma
         #SBATCH --exclusive
     triple_slurm:
       class: lsst.ctrl.bps.parsl.sites.TripleSlurm
       nodes: 1
       cores_per_node: 100
       qos: normal
       small_memory: 2.0     # Units are GB
       medium_memory: 4.0
       large_memory: 8.0
       small_walltime: 10.0   # Units are hours
       medium_walltime: 10.0
       large_walltime: 40.0
     work_queue:
       class: lsst.ctrl.bps.parsl.sites.work_queue.LocalSrunWorkQueue
       worker_options: "--memory=480000"   # work_queue expects memory in MB
       nodes_per_block: 10

Different configurations are listed, with user-provided labels, under the ``site`` section, and the configuration that's used in the actual BPS submission is specified in the ``computeSite`` field via one of those labels.

Monitoring of the pipetask job progress can be enabled by adding the lines

.. code-block:: yaml
   :name: enable-parsl-monitoring

       monitorEnable: true
       monitorFilename: runinfo/monitoring.db

to the desired ``site`` subsection.  The ``monitorFilename`` field specifies the name of the sqlite3 file into which the Parsl workflow tracking information is written.  Parsl has a web-app for displaying the monitoring information, and installation of the packages needed to support that web-app are described in the ctrl_bps_parsl `README <https://github.com/lsst/ctrl_bps_parsl#parsl-with-monitoring-support>`__.  This `python module <https://github.com/LSSTDESC/gen3_workflow/blob/master/python/desc/gen3_workflow/query_workflow.py>`__ provides an example for reading the info from that monitoring database.

.. note::

  As of 2022-09-27, the ``parsl`` module and its dependencies are only available at S3DF via the CVMFS distributions of ``lsst_distrib`` for weekly ``w_2022_37`` and later.  However, the modules needed for Parsl *monitoring* are not available in the CVMFS distributions.  They can be installed in ``~/.local`` with the following commands::

   $ source /cvmfs/sw.lsst.eu/linux-x86_64/lsst_distrib/w_2022_39/loadLSST-ext.bash
   $ setup lsst_distrib
   $ pip install 'parsl[monitoring]' --user
   $ pip uninstall sqlalchemy

  The ``pip uninstall sqlalchemy`` command is needed since the ``pip install 'parsl[monitoring]'`` command installs an earlier version of ``sqlalchemy`` that's incompatible with ``lsst_distrib``.

Notes on each of the example configurations follow (Each class listed below lives in the ``lsst.ctrl.bps.parsl.sites`` namespace):

Local
-----
This class should be used for running on a single node.  The ``cores`` field should be set to the number of cores that will be reserved for running the individual ``pipetask`` commands, with one core allocated per pipetask job.  For example, a ``Local`` configuration can be used in an interactive Slurm session obtained using ``srun``

.. prompt:: bash

   srun --pty --cpus-per-task=8 --mem-per-cpu=4G --time=01:00:00 --partition=roma bash

Note that the ``--cpus-per-task`` matches the number of ``cores`` in the ``local`` config.

Slurm
-----
This class uses a generic Slurm site configuration that can, in principle, be used with any Slurm submission system.

In the above example, an allocation of 2 nodes with at least 100 cores per node is requested.   Various ``sbatch`` options can be passed to slurm via the ``scheduler_options`` entry.  In the above example, we've chosen the ``roma`` partition at S3DF and requested exclusive use of the nodes.

The ``bps submit <bps config yaml>`` command will have Parsl submit a pilot job request to the Slurm queues, and once the pilot job starts, Parsl will run the pipetask jobs on that allocation.  Meanwhile, the ``bps submit`` command will continue to run on the user's command line, outputting various log messages from BPS and Parsl.   The ``Slurm`` configuration class uses Parsl's `HighThroughputExecutor <https://parsl.readthedocs.io/en/stable/stubs/parsl.executors.HighThroughputExecutor.html#parsl.executors.HighThroughputExecutor>`__ to manage the job execution on the allocated nodes, assigning one core per pipetask job.  An important caveat is that the per-pipetask memory requests provided by the BPS config are ignored, so if the average memory per pipetask exceeds 4GB and all of the cores on a S3DF batch node are running, an out-of-memory error will occur, and the Slurm job will terminate.  The ``TripleSlurm`` and ``LocalSrunWorkQueue`` configuration classes provide ways of handling the per-pipetask memory requests.

A useful feature of this class is that it uses the `sbatch <https://slurm.schedmd.com/sbatch.html#OPT_singleton>`__ ``--dependency=singleton`` option to schedule a Slurm job that is able to begin execution as soon as the previous job (with the same job name and user) finishes.  This way long running pipelines need not request a single, long (and difficult to schedule) allocation at the outset and can instead use a series of smaller allocations as needed.

TripleSlurm
-----------
This configuration provides three ``HighThroughputExecutors``, each with different memory limits for the pipetask jobs that are run on them.  In the above example, each executor assigns the specified memory per core, and accordingly limits the number of available cores for running jobs given the total memory per node.  Pipetask jobs that request less than 2GB of memory will be run on the "small" allocation; jobs that request between 2GB and 4GB of memory will be run on the "medium" allocation; and all other jobs will be run on the "large" allocation.  Despite the segregation into small, medium, and large memory requests, there is still the risk of jobs that request more than 8GB on average causing the "large" allocation to suffer an out-of-memory error.

work_queue.LocalSrunWorkQueue
-----------------------------
The ``LocalSrunWorkQueue`` configuration class uses Parsl's `WorkQueueExecutor <https://parsl.readthedocs.io/en/stable/stubs/parsl.executors.WorkQueueExecutor.html#parsl.executors.WorkQueueExecutor>`__ to manage the resource requests by the individual pipetask jobs.   It uses the `work_queue <https://cctools.readthedocs.io/en/stable/work_queue/>`__ module to keep track of overall resource usage in the allocation and launches jobs when and where the needed resources are available.

In this class, a Parsl `LocalProvider <https://parsl.readthedocs.io/en/stable/stubs/parsl.providers.LocalProvider.html#parsl.providers.LocalProvider>`__ manages the resources from within the allocation itself, and so the procedure for running with this class differs from the Slurm-based classes in that the user is responsible for submitting the pilot job using ``sbatch`` command and running the ``bps submit`` command within the submission script.  In the pilot job, one of the nodes serves as the Parsl "submission node" and runs the pipetask jobs on the available nodes (including the submission node) using the Slurm ``srun`` command.   Here is an example submission script with the sbatch options set to match the ``work_queue`` configuration shown above:

.. code-block:: bash
   :name: sbatch-work-queue-example

   #!/bin/bash

   #SBATCH --nodes=10
   #SBATCH --exclusive
   #SBATCH --time=02:00:00

   cd <working_dir>
   source /cvmfs/sw.lsst.eu/linux-x86_64/lsst_distrib/w_2022_38/loadLSST-ext.bash
   setup lsst_distrib
   <other setup commands>
   bps submit <bps yaml file>

Since the Parsl-plugin and other processes running on the submission node have their own memory requirements, one should set the memory available per node to a value somewhat smaller than the total memory capacity.  This is done with the ``worker_options: "--memory=480000"`` option, where memory is in units of MB.  This memory limit applies to all of the nodes in the allocation, so for Slurm jobs that request a large number of nodes, e.g., more than ~20, it would be more efficient to set aside a single node on which to run the ``bps submit`` command and use the other nodes as "worker" nodes.  This can be accomplished by prepending ``srun`` to the ``bps`` command in the Slurm batch script:

.. code-block:: bash
   :name: sbatch-work-queue-srun-example

   srun bps submit <bps yaml file>

In this case, one should set ``#SBATCH --nodes=N`` so that ``N`` is one greater than the ``nodes_per_block`` value in the BPS config entry.

To use this class, the ``work_queue`` module must be installed.  That module is available from the `cctools toolkit <https://cctools.readthedocs.io/en/stable/>`__, which is itself available from conda-forge.
