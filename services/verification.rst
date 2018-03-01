###################################################################
Using the Verification Cluster
###################################################################

The ``Verification Cluster`` is a cluster of servers run by NCSA for LSST DM development work.

To get an account, see the :doc:`Onboarding Checklist </team/onboarding>`.

This page is designed help you get started on the ``Verification Cluster``:

#. :ref:`verification-overview`
#. :ref:`verification-password`
#. :ref:`verification-gpfs`
#. :ref:`verification-stack`
#. :ref:`verification-slurm`


.. _verification-overview:

Overview of the Verification Cluster
====================================

``lsst-dev01`` is a system with 24 physical cores, 256 GB RAM, running the latest CentOS 7.x that serves as the front end of the
``Verification Cluster``.  ``lsst-dev01`` is described in further detail at :doc:`lsst-dev` and on the
page of `available development servers <https://confluence.lsstcorp.org/display/LDMDG/DM+Development+Servers>`_ .

The ``Verification Cluster`` consists of 48  Dell C6320 nodes with 24 physical cores (2 sockets, 12 cores per processor) and 128 GB RAM.  As such, the system provides a total of 1152 physical cores. Due to hyperthreading, each physical core appears as 2 Linux cores, so users can access 48 logical or virtual cores per node.

The ``Verification Cluster`` runs the Simple Linux Utility for Resource Management (SLURM) cluster management and job scheduling system.  ``lsst-dev01`` runs the SLURM controller and serves as the login or head node , enabling LSST DM users to submit SLURM jobs to the ``Verification Cluster``.

``lsst-dev01`` and the ``Verification Cluster`` utilize the General Parallel File System (GPFS) to provided shared-disk across all of the nodes.  The GPFS will have spaces for archived datasets and scratch space per user to support computation/analysis.

The legacy NFS /home directories are available on the front end ``lsst-dev01`` (serving as the current
home directories), but are not mounted on the compute nodes of the ``Verification Cluster``.

Report system issues by `filing a JIRA ticket <https://jira.lsstcorp.org/secure/CreateIssueDetails!init.jspa?pid=12200&issuetype=10901&priority=10000&customfield_12211=12223&components=14205>`_ in the IT Helpdesk Support (IHS) project.


.. _verification-password:

Account Password
================

You can log into LSST development servers at NCSA such as ``lsst-dev01`` with your NCSA account and password. You can reset your NCSA password at the following URL:

   - https://identity.ncsa.illinois.edu/reset


.. _verification-gpfs:

GPFS Directory Spaces
=====================

GPFS is available on the login node ``lsst-dev01`` and on all of the compute nodes of the ``Verification Cluster``. For convenience the bind mounts  :file:`/scratch`  , :file:`/project` , :file:`/datasets` ,  and :file:`/software`  have been created to provide views into corresponding spaces in GPFS.  Users will find directories

:file:`/scratch/<username>`

ready and available for use.  The per user :file:`/scratch` space is volatile with a 180 day purge policy
and is not backed up.
The :file:`/project` space is volatile, not backed up, and has no purge policy; cooperative self-management of this space for longer-lived but non-permanent files is expected.
As examples, :file:`/project/<username>` directories could be created, or, for shared data, :file:`/project/<projectname>` directories might be appropriate.

Project managed datasets will be stored within the :file:`/datasets` space.  The population of
:file:`/datasets` with reference data collections is still in the early stages; a first
example is the SDSS DR7 Stripe82 data, which can be found at

:file:`/datasets/stripe82/dr7/runs`

To add/change/delete datasets, see :doc:`Common Dataset Organization and Policy </services/datasets>`.

.. _verification-stack:

Shared Software Stack in GPFS
=============================
A shared software stack on the GPFS file systems, suitable for computation on the
``Verification Cluster``, has been provided and is maintained by Science Pipelines and
is available under :file:`/software/lsstsw`.  This stack may be initialized via:  ::

     % .  /software/lsstsw/stack/loadLSST.bash


.. _verification-slurm:

SLURM Job Submission
====================

Documentation on using SLURM client commands and submitting jobs may be found
at standard locations (e.g., a `quickstart guide <http://slurm.schedmd.com/quickstart.html>`_).
In addition to the basic SLURM client commands, there are higher level tools
that can serve to distribute jobs to a SLURM cluster, with one example being
the combination of `pipe_drivers <https://github.com/lsst/pipe_drivers>`_ and
`ctrl_pool   <https://github.com/lsst/ctrl_pool>`_ within LSST DM.
For exhaustive documentation and specific use cases, we refer the user
to such resources. On this page we display some simple examples for
getting started with submitting jobs to the ``Verification Cluster``.

The ``Verification Cluster`` SLURM is configured with 2 queues (partitions):

   - **normal**: 45 nodes, no run time limit.  For runs after your code is debugged.  Default.
   - **debug**:  3 nodes, 30 min run time limit.  For short testing & debugging runs.

The ``normal`` queue is the default, so any ``debug`` jobs will need to be told to run in the debug queue. This can be done by adding ``-p debug`` to your sbatch command line, or adding the following to your job's batch file::

     #SBATCH -p debug

To examine the current state and availability of the nodes in the ``Verification Cluster``,
one can use the SLURM command  ``sinfo``::

     % sinfo
     PARTITION AVAIL  TIMELIMIT  NODES  STATE NODELIST
     normal*      up   infinite     15  alloc lsst-verify-worker[02-16]
     normal*      up   infinite     30   idle lsst-verify-worker[01,17-45]
     debug        up      30:00      1 drain* lsst-verify-worker48
     debug        up      30:00      2   idle lsst-verify-worker[46-47]

     % sinfo  -N -l --states="idle"
     Wed Jan 31 10:53:52 2018
     NODELIST              NODES PARTITION       STATE CPUS    S:C:T MEMORY TMP_DISK WEIGHT AVAIL_FE REASON
     lsst-verify-worker01      1   normal*        idle   48   48:1:1      1        0      1   (null) none
     lsst-verify-worker17      1   normal*        idle   48   48:1:1      1        0      1   (null) none
     lsst-verify-worker18      1   normal*        idle   48   48:1:1      1        0      1   (null) none
     lsst-verify-worker19      1   normal*        idle   48   48:1:1      1        0      1   (null) none
     lsst-verify-worker20      1   normal*        idle   48   48:1:1      1        0      1   (null) none
     ...
     lsst-verify-worker44      1   normal*        idle   48   48:1:1      1        0      1   (null) none
     lsst-verify-worker45      1   normal*        idle   48   48:1:1      1        0      1   (null) none
     lsst-verify-worker46      1     debug        idle   48   48:1:1      1        0      1   (null) none
     lsst-verify-worker47      1     debug        idle   48   48:1:1      1        0      1   (null) none


In this view ``sinfo`` shows the nodes to reside within a single partition ``debug``, and the worker nodes show 48 possible hyperthreads on a node (in the future this may be reduced to reflect the actual 24 physical cores per node). At the time of this ``sinfo`` invocation there were 42 verification nodes available, shown by the "idle" state.  The SLURM configuration currently does not perform accounting, and places no quotas on users' total time usage.

Simple SLURM jobs
-----------------------------

In submitting SLURM jobs to the ``Verification Cluster`` it is advisable to have the
software stack, data, and any utilities stored on the GPFS :file:`/scratch` , :file:`/datasets` , and/or :file:`/software` spaces so that all are reachable from ``lsst-dev01`` and each of the worker nodes.  Some simple SLURM job description files that make use of the ``srun`` command
are shown in this section. These are submitted to the queue from a standard login shell on the front end ``lsst-dev01`` using the SLURM client command ``sbatch``, and their status can be checked with the
command ``squeue`` :

For a single task on a single node: ::

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

This example job was assigned jobid 109 by the SLURM scheduler, and consequently the standard output and error of the job were written to a default file :file:`slurm-109.out` in the current working directory. ::

    % cat slurm-109.out
     lsst-verify-worker11.ncsa.illinois.edu
     Sleeping for 30 ...

To distribute this script for execution to 6 nodes by 24 tasks per node (total 144 tasks), the form of the job description is:  ::

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

For these test submissions a user might submit from a working directory
in the :file:`/scratch/<username>`  space with the executable script :file:`sleep.sh` and the job description file located in the current working directory.


Interactive SLURM jobs
-----------------------------

A user can schedule and gain interactive access to ``Verification Cluster`` compute nodes
using the SLURM ``salloc`` command. Example usage is:

For a single node: ::

    % salloc  -N  1 -p debug -t 00:30:00  /bin/bash
    salloc: Granted job allocation 108

    % squeue
             JOBID PARTITION     NAME     USER ST       TIME  NODES NODELIST(REASON)
               108     debug     bash    daues  R       0:58      1 lsst-verify-worker46
    % hostname -f
    lsst-dev01.ncsa.illinois.edu

    % srun hostname -f
    lsst-verify-worker46.ncsa.illinois.edu

One can observe that after the job resources have been granted, the user shell is still on
the login node ``lsst-dev01``. The command ``srun`` can be utilized to run commands on the job's allocated
compute nodes. Commands issued without ``srun``  will still be executed locally on ``lsst-dev01``.

You can also use ``srun`` without first being allocated resources (via ``salloc``).
For example, to immediately obtain a command-line prompt on a compute node: ::

    % srun -I --pty bash


SLURM Example Executing Tasks with Different Arguments
------------------------------------------------------

In order to submit multiple tasks that each have distinct command line arguments (e.g., data ids),
one can utilize the ``srun`` command with the ``--multi-prog`` option.   With this option, rather than
specifying a single script or binary for ``srun`` to execute, a filename is provided as the argument
of  the ``--multi-prog`` option. In this scenario an example job description file is:   ::


    % cat test1_24.sl
    #!/bin/bash -l

    #SBATCH -p debug
    #SBATCH -N 1
    #SBATCH -n 24
    #SBATCH -t 00:10:00
    #SBATCH -J sdss24

    srun --output job%j-%2t.out --ntasks=24 --multi-prog cmds.24.conf

This description specifies that 24 tasks will be executed on a single node,
and the standard output/error from each of the tasks will be written to a unique filename with format specified by the argument to ``--output``. The 24 tasks to be executed are specified in the file
:file:`cmds.24.conf`  provided as the argument to the  ``--multi-prog`` option. This
commands file will have a format that maps SLURM process ids (SLURM_PROCID) to programs to execute
and their commands line arguments.  An example command file has the form : ::

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



