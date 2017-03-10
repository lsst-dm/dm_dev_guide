Getting started
===============

Setting up your :file:`$HOME/.lsst` directory
---------------------------------------------

Your :file:`$HOME/.lsst` directory requires two Config files:
:file:`db-auth.py` and :file:`condor-info.py`

:file:`db-auth.py`
    database authentication configuration file

    The form of the file is:

    .. code-block:: text

       root.database.authInfo"auth1".host = "lsst10.ncsa.illinois.edu"
       root.database.authInfo"auth1".user = "juser"
       root.database.authInfo"auth1".password = "funkystuff"
       root.database.authInfo"auth1".port = 3306
       root.database.authInfo"auth2".host = "ds33.ncsa.illinois.edu"
       root.database.authInfo"auth2".user = "juser"
       root.database.authInfo"auth2".password = "stunkyfluff"
       root.database.authInfo"auth2".port = 3306

    where:

    * host - the name of the MySQL host
    * user - the MySQL user name
    * password - the MySQL password
    * port - the MySQL port number

    Note that the $HOME/.lsst directory must have permissions 700 (owner read,
    write, execute) and the db-auth.py file must have permissions 600 (owner
    read, write).

:file:`condor-info.py`
    HTCondor information file

    .. code-block:: text

       root.platform["lsst"].user.name = "juser"
       root.platform["lsst"].user.home = "/lsst/home/juser"
       root.platform["gordon"].user.name = "thx1138"
       root.platform["gordon"].user.home = "/usr/thx1138"

    Where:

    * ``platform[<platform name>]`` specifies the platform on which you're
      going to run jobs
    * ``user.name`` specifies the account name on that platform
    * ``user.home`` specifies your account home directory on that platform

Setting up for runs on the LSST cluster
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Create the directory :file:`$HOME/condor_scratch`.  This is the directory where
directories and files used by Condor will be written. Each run will have its
own directory.  The directory name is the same as the runid for that run.

Setting up for runs on gordon
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

1. Create the directory :file:`$HOME/condor_scratch`

   This is the directory where directories and files used by Condor will be
   written.  Each run will have its own directory.  The directory name is the
   same as the runid for that run.

2. Login to **gordon.sdsc.edu**.

   Information for access to Gordon is  available on the SDSC site.  You can
   set up an account on  the XSEDE portal.

3. On gordon, create the directory :file:`$HOME/condor_scratch`

   This is the directory where files created by the allocateNodes (the PBS file
   for glidein, and the custom Condor configuration file) will be written.

4. Create the directory :file:`$HOME/condor_local`

   This is the local directory space the Condor will use during it's runs.

5. Create the directory
   :file:`/oasis/scratch/<YOUR_USER_NAME/temp_project/defaultRoot`

Running Jobs
^^^^^^^^^^^^

Packages
""""""""

The packages used by the self-service orchestration utilities:

ctrl_execute
    contains the self-service orchestration utilities. 
ctrl_platform_lsst
    setup required to run on the LSST 
cluster ctrl_platform_gordon
    setup required to run on gordon.sdsc.edu

To run on the LSST cluster:
"""""""""""""""""""""""""""

.. prompt:: bash

   setup ctrl_execute
   setup ctrl_platform_lsst

To run on gordon.sdsc.edu
"""""""""""""""""""""""""

.. prompt:: bash

   setup ctrl_execute
   setup ctrl_platform_gordon

Node allocation on XSEDE nodes
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If you are going to run jobs on the XSEDE nodes, you must first take the
following steps to allocate nodes from an XSEDE cluster.

Allocating nodes
""""""""""""""""

Condor node allocation is only required if you plan on running on a supported
XSEDE cluster.  The nodes in the LSST cluster Condor flock are permanently
allocated, and are a shared resource.

You specify now many nodes you want to allocate, how many slots per node to
use, and the maximum amount of time you want to use those nodes once they are
allocated to you.

For example, if you wanted to allocate two nodes, using twelve cores per node
for 30 minutes, you would execute the following:

.. code-block:: shell

   $ allocateNodes.py gordon -n 2 -s 12 -m 00:30:00
   alloc_juser_2012_0927_112607.pbs              100% 3290     3.2KB/s   3.2KB/s   00:00
   condor_juser_2012_0927_112607.config          100% 1047     1.0KB/s   1.0KB/s   00:00
   328255.gordon-fe2.local
   2 nodes allocated on gordon with 12 slots per node and maximum time limit of 00:30:00
   Node set name:
   juser_19

When you execute the command, it writes a PBS file, and a Condor config file
which are both transferred to the condor_scratch directory in your
``$HOME`` directory.  It then submits the PBS file on gordon.sdsc.edu.
The last thing that is printed is the "node set" name of the nodes you just
allocated.  The “node set” is a way of naming all the nodes that you just
allocated.  Remember that node set name. You’ll use it when executing the
"runOrca.py" command.

Obtaining the node allocation can take some time, depending on how busy the
system is, how many jobs are running, and the size of your request.

If you want to see the status of your allocation you can run, the
:command:`condor_status` command.

.. prompt:: bash

   condor_status -const 'NODE_SET == "juser_19"'

which will show you all of the nodes that have joined the Condor flock that
match node-set "juser_19".  If you see a list of nodes, they've joined the
flock. If you don't see anything, they aren't available on the Condor flock
yet.

If you want see the status of the queued node allocation request on gordon (or
delete it), you can use the following commands:

* :command:`qstatus.py` shows the status of the PBS request for nodes to be
  allocated.
* :command:`qdelete.py` deletes a specific PBS request.

In the following example, I allocate 2 nodes with 2 cores each.

.. code-block:: shell

   $ allocateNodes.py gordon -n 2 -s 2 -m 00:30:00
   alloc_srp_2012_0928_132607.pbs               100% 3287     3.2KB/s   3.2KB/s   00:00
   condor_srp_2012_0928_132607.config           100% 1047     1.0KB/s   1.0KB/s   00:00
   330278.gordon-fe2.local
   2 nodes allocated on gordon with 2 slots per node and maximum time limit of 00:30:00
   Node set name:
   srp_21

The nodes are allocated for node-set "srp_21".

I now run the qstatus.py command to see the status of the request on the remote
machine:

.. code-block:: shell

   $ bin/qstatus.py gordon
   gordon-fe2.sdsc.edu:
                                                                            Req'd  Req'd   Elap
   Job ID               Username Queue    Jobname          SessID NDS   TSK Memory Time  S Time
   -------------------- -------- -------- ---------------- ------ ----- --- ------ ----- - -----
   330278.gordon-fe     srp      normal   srp_21              --      2   4    --  00:30 Q   --

The "Q" in the status line shows that the command has been queued.

If we run it again a minute or two later:

.. code-block:: shell

   $ qstatus.py gordon
   gordon-fe2.sdsc.edu: 
                                                                            Req'd  Req'd   Elap
   Job ID               Username Queue    Jobname          SessID NDS   TSK Memory Time  S Time
   -------------------- -------- -------- ---------------- ------ ----- --- ------ ----- - -----
   330278.gordon-fe     srp      normal   srp_21              --      2   4    --  00:30 R   -- 

We see that the "Q" has been changed to "R", meaning the request is running.

Shortly afterward, the nodes should show up in the Condor Flock:

.. code-block:: shell

   $ condor_status
   Name               OpSys      Arch   State     Activity LoadAv Mem   ActvtyTime

   slot1@12597@gcn-6- LINUX      X86_64 Unclaimed Idle     0.180  32257  0+00:00:04
   slot2@12597@gcn-6- LINUX      X86_64 Unclaimed Idle     0.000  32257  0+00:00:05
   slot1@26427@gcn-6- LINUX      X86_64 Unclaimed Idle     0.000  32257  0+00:00:04
   slot2@26427@gcn-6- LINUX      X86_64 Unclaimed Idle     0.000  32257  0+00:00:05

   [other output deleted]

Now, to remove those nodes from the condor flock, we run the qdelete command:

.. prompt:: bash

   qdelete.py gordon 330278

And then check to see when the PBS job is cancelled:

.. code-block:: shell

   $ qstatus.py gordon
   gordon-fe2.sdsc.edu: 
                                                                            Req'd  Req'd   Elap
   Job ID               Username Queue    Jobname          SessID NDS   TSK Memory Time  S Time
   -------------------- -------- -------- ---------------- ------ ----- --- ------ ----- - -----
   330278.gordon-fe     srp      normal   srp_21              --      2   4    --  00:30 R   -- 

It hasn't been cancelled yet. Wait a minute or two, and then issue the command
again:

.. code-block:: shell

   $ qstatus.py gordon
   gordon-fe2.sdsc.edu: 
                                                                            Req'd  Req'd   Elap
   Job ID               Username Queue    Jobname          SessID NDS   TSK Memory Time  S Time
   -------------------- -------- -------- ---------------- ------ ----- --- ------ ----- - -----
   330278.gordon-fe     srp      normal   srp_21             8397     2   4    --  00:30 C 00:00

Running a job
^^^^^^^^^^^^^

Whether you're running a job on XSEDE or the LSST cluster, the command for
running a job is virtually identical.

The runOrca.py command takes the following arguments at a minimum:

- ``-p <platform>``
- ``-c <command>``
- ``-i <input_file>``
- ``-e <EUPS_PATH>``

The following invocation runs the command :command:`processCcdSdss.py sdss
/lsst7/stripe82/dr7-coadds/v5/run0/jbosch_2012_0710_192216/input --output
./output` using input file :file:`$HOME/short.input` and a stack located at
:file:`/lsst/DC3/stacks/gcc445-RH6/default` on the lsst cluster:

.. code-block:: shell

   runOrca.py -p lsst -c "processCcdSdss.py sdss /lsst7/stripe82/dr7-coadds/v5/run0/jbosch_2012_0710_192216/input --output ./output" -i $HOME/short.input -e /lsst/DC3/stacks/gcc445-RH6/default

Note that in the command above, ``--output ./output`` refers to the output
directory in which the :file:`processCcdSdss.py` command is run, not the
directory from which :file:`runOrca.py` is run.  More details on that below.

On the XSEDE cluster, the following argument should be added ``-N <node-set>``.

The following invocation runs the command :command:`processCcdSdss.py sdss
/oasis/projects/nsf/nsa101/srp/inputdata/Sept2012/input --output ./output`
using input file :file:`$HOME/short.input` and a stack located at
:file:`/oasis/scratch/ux453102/temp_project/lsst/beta-0713/lsst_home` targeted
at node set ``srp_21``

.. code-block:: shell

   runOrca.py -p gordon -c "processCcdSdss.py sdss /oasis/projects/nsf/nsa101/srp/inputdata/Sept2012/input --output ./output" -i $HOME/short.input -e  /oasis/scratch/ux453102/temp_project/lsst/beta-0713/lsst_home -N srp_21

Note that in the command above, ``--output ./output`` refers to the output
directory in which the :file:`processCcdSdss.py` command is run, not the
directory from which :file:`runOrca.py` is run.  More details on that below.

Notes on the execution environment
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

When you run a job, whether it's on an XSEDE cluster or the LSST cluster, we
take a snapshot of the current environment you have setup in the shell you are
executing commands in, and duplicate that environment when the job runs. This
is done in one of three ways.

1. On the LSST cluster, the environment variables you have currently "setup" is
   duplicated during job execution by using Condor's environment copying
   mechanism.  This makes the initial "preJob.sh" run very quickly. This does
   not copy files, only the environment variables.

2. On the LSST cluster, if you specify the ``--setup <pkg> <pkg_ver>`` on the
   command line, Condor's environment setup mechanism is by passed and all
   packages are created by using ``setup -j <pkg> <pkg_ver>`` in the initial
   preJob script of the DAGman job that is submitted. After the environment is
   setup it is saved and used for re-loading quickly when the worker jobs
   execute. This takes as long as it would on the regular command line, which
   can take some time in the preJob, but loads quickly.

3. On XSEDE nodes, we use EUPS to look at all the packages you currently have
   "setup", record the versions of those packages, and attempt to set those up
   when the job runs.  You must have the current version of those packages in
   the stack you specify on the command line, or you will get an error.  Any
   locally setup packages (which you can see listed with version prefix LOCAL:
   when you run "eups list") ARE NOT SETUP on the remote system.

Note that in all of these cases, all code is expected to be on the execution
platform. No local package files are ever copied to the execution nodes.

Job Execution Directory
^^^^^^^^^^^^^^^^^^^^^^^

Jobs are executed on the LSST cluster in the :file:`/lsst/DC3root`` directory,
in a directory named after the runid.

Jobs are executed on the LSST cluster in the
:file:`/oasis/scratch/<YOUR_REMOTE_USER_NAME>/temp_project/defaultRoot`
directory, in a directory named after the runid.

While the directories named in this directory are up to the command issued,
there are some file that are consistent no matter what command is run.

The :file:`eups.list` file shows the environment that was used to do this run.

The logs directory has logs of what each machine and “slot” on that machine in
the Condor execution ran.  Below that directory, there’s a log file that is
stamped with the job id number that ran.

For example, a simple execution that had three jobs to run.  They all ran on
one slot on machine gcn-15-65.  The log file directory structure looks like
this:

.. code-block:: shell

   logs
   logs/gcn-15-65
   logs/gcn-15-65/1
   logs/gcn-15-65/1/S2012Pipe-1.log
   logs/gcn-15-65/1/S2012Pipe-2.log
   logs/gcn-15-65/1/S2012Pipe-3.log

Look in these log files for specific information about your run.

Your :file:`$HOME/condor_scratch` directory
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The :file:`$HOME/condor_scratch` directory is where condor files are written.
The "configs" directory is where :command:`allocateNodes.py` and
:command:`runOrca.py` write their PBS files, Condor configuration files and
Orca config files are written.  The "runid" directory is where Orca writes the
DAGman file that is submitted, where the pre-job, worker job, and post-job
scripts are created, and where the condor log files are written.  Generally you
won't need to look at these files, but if you're trying to see what the actual
execution scripts that are used by Condor look like, look for them here.

Debugging
^^^^^^^^^

Errors in setup
"""""""""""""""

By design, the EUPS environment that you're launching on and duplicates it on
the remote system where the jobs run.  This is currently done through a series
of EUPS setup calls. Because of this, no LOCAL: setups are duplicated, since
the file system indicated in LOCAL: won't be available on the remote system.

Because of this, you might run into an issue where your setups fail on the
remote system.  If you suspect this, look in the runid directory under
~condor_scratch, you'll see a "logs" directory.  Below that, you'll see where
all the log files are written before the job actually starts (the actual logs
for the jobs are currently written to disk on the remote side, in this case
gordon).

However, the logs you were looking for are kept in the "preJob" scripts under:

.. code-block:: shell

   worker-pre.*

In particular, you can find setup errors in the .err files. For example the
file :file:`~/condor_scratch/krughoff_2012_1109_123511/logs/worker-pre.err`
looks like this:

.. code-block:: shell

   Failed to setup datarel 6.1.0.1+1: Product datarel 6.1.0.1+1 not found
   Failed to setup ctrl_platform_gordon 6.1.0.2+2: Product ctrl_platform_gordon 6.1.0.2+2 not found
   Failed to setup ctrl_execute 6.1.0.7+2: Product ctrl_execute 6.1.0.7+2 not found
   Failed to setup scipy 0.10.1+1: Product scipy 0.10.1+1 not found

This indicates that the tagged versions of your software on the local system
(where you launched the Condor job from), are unavailable on the remote system.
You must install those tagged versions in your stack on the remote system to
fix this issue.
