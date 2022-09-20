#################
Batch Resources
#################

This document describes the batch resources available at the LSST Data
Facility during the interim period where the Rubin filesystems at SLAC
go into production mode on our own hardware, and while user and
project data are being transferred from NCSA.

Use of SDF batch is documented at

https://sdf.slac.stanford.edu/public/doc/#/batch-compute

Rubin currently has an allocation of 2000 cores. Currently only a single slurm partition is defined, called "roma". No
special batch queues exist yet.


Running LSST Pipelines with BPS
===============================
The LSST Batch Processing Service (`BPS <https://github.com/lsst/ctrl_bps>`__) is the standard execution framework for running LSST pipelines using batch resources.  There are a few different plugins to BPS that are available that can be used for running BPS on various computing systems:

- ctrl_bps_htcondor
- ctrl_bps_panda
- :ref:`ctrl_bps_parsl <ctrl_bps_parsl>`

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
       nodes: 10
       walltime: 2:00:00     # This is 2 hours
       cores_per_node: 100
       qos: normal
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

Notes on each of the example configurations follow (Each class listed below lives in the ``lsst.ctrl.bps.parsl.sites`` namespace):

Local
-----
This class should be used for running on a single node.  The ``cores`` field should be set to the number of cores that will be reserved for running the individual ``pipetask`` commands, with one core allocated per pipetask job.  For example, a ``Local`` configuration can be used in an interactive Slurm session obtained using ``srun``

.. prompt:: bash

   srun --pty --cpus-per-task=8 --mem-per-cpu=4G --time=01:00:00 --partition=rubin bash

Note that the ``--cpus-per-task`` matches the number of ``cores`` in the ``local`` config.

Slurm
-----
This class uses a generic Slurm site configuration that can, in principle, be used with any Slurm submission system.  However, there is no interface (yet) to specify the Slurm partition, so for running at S3DF, the default ``roma`` partition will be used.

In the above example, an allocation of 10 nodes with at least 100 cores per node is requested.  Note that ``qos: normal`` needs to be set explicitly for running at S3DF.

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
