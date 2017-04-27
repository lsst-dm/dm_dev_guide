Configuration and templates
===========================

The :file:`runOrca.py` and :file:`allocateNodes.py` utilities in the
**ctrl_execute** package use a template system that is similar to the Condor
plug-in that Orca uses. The **ctrl_platform_lsst** and **ctrl_platform_gordon**
contain platform specific information for running jobs on each of those
platforms. These are all discussed below. You should be familiar with the
concepts laid out in the explanation of the Condor plug in, available on this
:doc:`page <htcondor-plugin>`.

The command line arguments and config files contain values which are substituted
for their corresponding $VAR type names in the template files when the utilities
are run. 

For example, the :file:`$HOME/.lsst/condor-info.py` is used to store
information about the user's login name and home directory for each platform.

.. code-block:: text

   root.platform["gordon"].user.name = "juser"
   root.platform["gordon"].user.home = "/home/juser"

   root.platform["lsst"].user.name = "joeuser"
   root.platform["lsst"].user.home = "/lsst/home/joeuser"

- ``user.name`` in the config file is ``$USER_NAME`` in template files
- ``user.home`` in the config file is ``$USER_HOME`` in template files

If ``$USER_NAME`` or ``$USER_HOME`` is encountered anywhere in a template file,
the corresponding values are substituted there. For example, a file written
using template that looks like this:

.. code-block:: shell

   cd $USER_HOME
   echo "hello" > $USER_NAME

will end up looking like this for the "gordon" platform:

.. code-block:: shell

   cd /home/juser
   echo "hello" > juser

This substitution method is used throughout all the template files.

The values for these variables are noted below in the discussion of the config
files.

:command:`allocateNodes.py`
---------------------------

The :command:`allocateNodes.py` command is the interface to the PBS submissions
queue and is used to submit Condor glide-in requests to XSEDE nodes. The
**pex_config** files and templates in the **ctrl_platform** directories are
used to configure the PBS file submitted to XSEDE.

:command:`pbsConfig.py`
-----------------------

The :command:`allocateNodes.py` command executes PBS jobs to “glide-in” Condor
nodes to the local cluster.

The file :file:`etc/config/pbsConfig.py` under the **ctrl_platform_*** packages
contains information to configure those PBS jobs. This file does not exist, and
is not needed in **ctrl_platform_lsst**, because we do have to allocate nodes to
the Condor cluster on that platform. They're permanently allocated.

From **ctrl_platform_gordon**:

.. code-block:: text

   root.platform.queue = "normal"
   root.platform.email = "#PBS -m be"
   root.platform.scratchDirectory = "$USER_HOME/condor_scratch"
   root.platform.loginHostName = "gordon.sdsc.edu"
   root.platform.utilityPath = "/opt/torque/bin"

- ``root.platform.queue`` - the name of the PBS queue to submit jobs to.
  Template variable: $QUEUE
- ``root.platform.email`` - value to insert into the PBS file to send the user
  e-mail before and after jobs execute. Template variable:
  ``$EMAIL_NOTIFICATION``
- ``root.platform.scratchDirectory`` - the directory on the REMOTE system to use  for Condor scratch space. Template variable: ``$SCRATCH_DIR``
- ``root.platform.loginHostName`` - the node to log into execute shell and copy
  commands. Template variable: ``$HOST_NAME``
- ``root.platform.utilityPath`` - the REMOTE system's directory where the PBS
  utilities (:command:`qsub`, :command:`qdel`, etc.) are located. Template
  variable: ``$UTILITY_PATH``

:file:`generic.pbs.template`
----------------------------

This file generic.pbs.template in the :file:`etc/templates` directory of XSEDE
node **ctrl_platform** packages is the template that is filled out changed into
the PBS file which is used to submit glide-in requests to the PBS queue on the
target platform.  IMPORTANT: The top part of this file looks like a comment
block, but is actually part of the PBS script. Do not delete that portion of the
file. It contains the "#PBS" statements which are used to configure the PBS
request.

Below that PBS statement block is a shell script that is executed once the nodes
are allocated. The ``$PBS_NODEFILE`` referenced in this part of the PBS
file will contain a list the slots allocated by the PBS job. This part of the
script runs through the list of slots, and runs an SSH command which sets up a
condor-glidein to run:

.. code-block:: shell

   ssh ${hostname[$num]} 'export CONDOR_CONFIG=$SCRATCH_DIR/$GENERATED_CONFIG;export _condor_CONDOR_HOST=lsst-launch.ncsa.illinois.edu;export _condor_GLIDEIN_HOST=lsst-launch.ncsa.illinois.edu;export _condor_LOCAL_DIR=$USER_HOME/condor_local;export _condor_SBIN=/oasis/projects/nsf/nsa101/srp/condor/condor-7.4.4-r1/sbin;export _condor_NUM_CPUS=$SLOTS;export _condor_UID_DOMAIN=ncsa.illinois.edu;export _condor_FILESYSTEM_DOMAIN=sdsc.edu;export _condor_MAIL=/bin/mail;export _condor_STARTD_NOCLAIM_SHUTDOWN=1800; /oasis/projects/nsf/nsa101/srp/condor/glidein/glidein_startup_gordon -dyn -f' &

- ``CONDOR_CONFIG`` points at the ``allocateNodes.py`` generated Condor config
  file. This is not a ``pex_config`` style file.
- ``_condor_CONDOR_HOST`` points at the head node of the Condor flock
- ``_condor_GLIDEIN_HOST`` points at the host configurated to accept glide-in
  requests to the Condor flock.
- ``_condor_LOCAL_DIR`` points at the Condor's local directory for job
  execution.
- ``_condor_SBIN`` points at the directory containing the binaries used by
  Condor
- ``_condor_NUM_CPUS`` assigns the number of slots per node
- ``_condor_UID_DOMAIN`` assigns the network domain name of the Condor flock
  that will host the glide-in
- ``_condor_FILE_SYSTEM_DOMAIN`` assigns the network domain name of the file
  system which the glide-in is coming from
- ``_condor_MAIL`` assigns the mail program Condor will use to send mail
  messages
- ``_condor_STARTD_NOCLAIM_SHUTDOWN`` assigns the time, in seconds, which a
  glide-in slot can be inactive before it is removed from the Condor flock. In
  other words, if no jobs are assigned to this slot within this time, it is
  removed from the Condor flock and is no longer available for jobs. If DAGman
  does not fill up the queue fast enough, a portion of a large glide-in request
  could be deallocated before any jobs are assigned.

:file:`glidein_condor_config.template`
--------------------------------------

This is the template for Condor config file which condor uses on startup. This
is a very simple Condor config file. The only additional non-standard value
used here is the ``NODE_SET`` variable:

.. code-block:: text

   NODE_SET = "$NODE_SET"

Note the use of the double quotes around the value. Those are required. If you
forget those, ``NODE_SET`` will not be set properly. 

When the template is written, the real value of ``$NODE_SET`` is
substituted.  The Condor matching algorithm has this value available to match
jobs. When a job is submitted, it has a "Requirements" line like this (from the
preJob, postJob and worker Condor submission file): [{{ Requirements =
(FileSystemDomain? == "sdsc.edu") && (Arch != "") && (OpSys? != "") && (Disk !=
-1) && (Memory != -1) && (DiskUsage? >= 0) && (NODE_SET == "$NODE_SET") }}}

When Condor matches jobs to machines, it matches this line. Our custom addition
of ``NODE_SET`` allows us to match particular jobs to particular sets of
machines. That's how we keep two different sets of allocated machines and two
sets of jobs from using each other's resources.

:file:`$HOME/.lsst/node-set.seq`
--------------------------------

Stores the sequence number of the node-set value. This is incremented by the
:file:`allocateNodes.py` utility.

Variables available for templates when using :command:`allocateNodes.py`
------------------------------------------------------------------------

- ``$USER_NAME`` - remote login name
- ``$USER_HOME`` - remote home directory
- ``$NODE_COUNT`` - number of nodes requested
- ``$SLOTS`` - number of Condor slots per node
- ``$WALL_CLOCK`` - maximum time to allocate these nodes. This is in the form
  "HH:MM:SS"
- ``$QUEUE`` - PBS queue to submit to
- ``$EMAIL_NOTIFICATION`` - string to insert into the PBS file for e-mail notification of job execution
- ``$SCRATCH_DIR`` - remote scratch directory
- ``$UTILITY_PATH`` - remote directory where the PBS utilities are located.
- ``$NODE_SET`` - the name of the node set for this glide-in
- ``$OUTPUT_LOG`` - the name of the output log for the entire Condor job
- ``$ERROR_LOG`` - the name of the error log for the entire Condor Job
- ``$GENERATED_CONFIG`` - the name of the template file generated Condor config
  file.

Files used by :command:`runOrca.py`
-----------------------------------

The :command:`runOrca.py` command is an interface to the :command:`orca.py`
command available in the **ctrl_orca** package. It's job is to configure
templates for the Orca Condor plug-in, and then execute the Orca command on
those resulting templates.  Those templates specify how to construct a Condor
DAG file, and what gets executed in a Condor "pre-job", "worker", and
"post-job".

Job Operating Environment
^^^^^^^^^^^^^^^^^^^^^^^^^

The :command:`runOrca.py` takes the LSST stack environment at the time of
execution on the launching platform, and duplicates it on the target platform.
This is done in one of two ways, depending on the platform, and depending on
the command line arguments you give it.

If you launch jobs to the LSST cluster, :command:`runOrca.py` will set up the
Condor jobs it launch to inherit your shell environment at the time you launch
the job. That means that anything you have set up in the LSST stack will
automatically be set up an used on the LSST cluster nodes when the jobs runs.
We can do this because we’re running on a system with duplicate system software
and a shared filesystem across the nodes. All versions are set up, including
anything that set up in your local space (shown as LOCAL: in eups list).  Job
Operating Environment

If you launch jobs to an XSEDE node, :command:`runOrca.py` will note all the
versions of the software you're running, and use a remote stack to set up those
same versions. Note that no locally setup packages (shown as LOCAL: in the eups
listing for that package) are setup remotely. 

In order to speed up the worker tasks, there is an initial job (called the
``preJob``) that sets everything up, and saves the environment into a shell
script called :file:`env.sh`. When a worker job starts, it executes that shell
script to set up the environment.

Because of these different operating environments, we need to set things up
differently in the configuration file that is given to Orca to execute. In the
:file:`ctrl_execute/etc/templates` directory, you’ll find the files:

.. code-block:: text

   config_with_getenv.py.template
   config_with_setups.py.template

These templates are very similar. The differences are that they point to
different ``preJob``, ``worker``, and ``postJob`` templates in the
**ctrl_platform_*** packages, the "setups" templates adds keywords for
``NODE_SET`` and ``CTRL_EXECUTE_SETUP_PACKAGES``.

The ``NODE_SET`` variable is used to specify which Condor "node set" to
run on.  See http://dev.lsstcorp.org/trac/wiki/Orchestration/SelfService for
more information about the node set concept. Note that while it is specified
here, if the Condor job is on the LSST cluster, this value is never used, since
it never appears in the **ctrl_platform_lsst** scripts.

The ``CTRL_EXECUTE_SETUP_PACKAGES`` variable is used by Orca to
substitute the setup commands in the preJob script.

Config files in **ctrl_platform** packages
------------------------------------------

:file:`execConfig.py`
^^^^^^^^^^^^^^^^^^^^^

The names of directories were Condor jobs are executed, where data is located,
etc., are different from platform to platform, as you would expect. This
information is kept in the :file:`etc/config/execConfig.py` Config file, for
each platform.

From **ctrl_platform_gordon**:

.. code-block:: text

   root.platform.localScratch = "$HOME/condor_scratch"
   root.platform.defaultRoot = "/oasis/scratch/$USER_NAME/temp_project/defaultRoot"
   root.platform.dataDirectory = "/oasis/projects/nsf/nsa101/srp/inputdata/Sept2012/input"
   root.platform.fileSystemDomain = "sdsc.edu"

- ``root.platform.localScratch`` - this is where Condor stores its files when
  you execute runOrca.py. Template variable: $LOCAL_SCRATCH
- ``root.platform.defaultRoot`` - this is the remote directory where orca jobs
  are executed. Output files and log files for the job appear here. Template
  variable: ``$DEFAULT_ROOT``
- ``root.platform.dataDirectory`` - this is where the data that jobs use is
  kept. Template variable: ``$DATA_DIRECTORY``
- ``root.platform.fileSystemDomain`` - this is the domain of the nodes of the
  remote cluster. Template variable: ``$FILE_SYSTEM_DOMAIN``

Template files in **ctrl_platform** packages

Under the :file:`etc/template` directory you’ll find subdirectories containing
template files. Under :file:`ctrl_platform_lsst/etc/templates` you’ll find the
directories :file:`setups` and :file:`getenv`. Under
:file:`ctrl_platform_gordon/etc/templates` you’ll find "setups". These are the
directories specified in the ``config_with_getenv.py.template`` and
``config_with_setups.py.template`` files mentioned above. Each of those
directories contain the following six files:

.. code-block:: text

   postJob.condor.template
   postJob.sh.template
   preJob.condor.template
   preJob.sh.template
   workerJob.condor.template
   worker.sh.template

The files with the condor.template suffix are all Condor templates that Orca
command will use to create “real” Condor submission files. For the most part,
these are standard Condor files. The main difference between these files in the
**ctrl_platform** packages is that the ``FileSystemDomain?`` is set to the
platform's network domain. For jobs that allocate remote nodes for glideins,
``NODE_SET`` is also specified here.

The files with the sh.template suffix are the scripts used during execution.
The preJob.sh.template and postJob.sh.template files are processed and turned
into .sh files which are executed once, and the worker.sh.template file is
turned into a worker.sh file which is executed as many times as specified by a
combination of the input file size and the number of ids per job that are
processed. This is all setup and used by a generated DAGman script. Note that
the :file:`setups/preJob.sh.template` contains code to handle setting up the
stack and saving the environment in the file :file:`env.sh`

.. code-block:: shell

   cd $EUPS_PATH
   . $EUPS_PATH/eups/default/bin/setups.sh
   setup lsst

   cd $ORCA_DEFAULTROOT
   cd $ORCA_RUNID
   echo "Begin setups:"
   date
   $CTRL_EXECUTE_SETUP_PACKAGES
   echo "Finished setups:"
   date

This portion of the script sets up the stack, moves to the correct run
directory, and then executes the setups. The :file:`runOrca.py` command takes
the snapshot of the users EUPS environment and creates a series of ``setup -j
<pkgname>`` references which it inserts in place of the
``$CTRL_EXECUTE_SETUP_PACKAGES`` variable. After everything has been setup, a
small portion of python code is executed which saves the environment.

As a reference, a processed :file:`preJob.sh.template` file would look something
like this, for the portion of code listed above:

.. code-block:: shell

   cd /oasis/scratch/ux453102/temp_project/lsst/beta-0713/lsst_home
   . /oasis/scratch/ux453102/temp_project/lsst/beta-0713/lsst_home/eups/default/bin/setups.sh

   setup lsst

   cd /oasis/scratch/srp/temp_project/defaultRoot
   cd srp_2012_1004_163420
   echo "Begin setups:"
   date
   setup -j cfitsio 3290+2
   setup -j astrometry_net 0.30
   setup -j sqlite 3.7.10+1
   setup -j eigen 3.0.2+1
   setup -j apr 1.3.3+1
   setup -j ctrl_sched 5.1.0.0+16
   setup -j datarel 5.2.1.5+4

   [...setup lines deleted...]

   setup -j gsl 1.15+1
   setup -j astrometry_net_data sdss-2012-05-01-0
   echo "Finished setups:"
   date

The ``worker.sh.template`` setups up the user's environment, runs the EUPS
environment shell script :file:`env.sh` and processes the command line ``—id``
arguments for the command given to :command:`runOrca.py`, appending those id
arguments to the command itself. It also saves the resulting log file to a
subdirectory below the directory below "logs". These log files are divided into
subdirectories based on the machine they ran on, and the Condor "slot" they ran
on, finally specified by the worker id number they were in the entire job.

Variables available for templates when using :command:`runOrca.py`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``$USER_NAME`` - remote login name
- ``$USER_HOME`` - remote home directory
- ``$DEFAULT_ROOT`` - remote default root for job execution directories to be
  created.
- ``$LOCAL_SCRATCH`` - local directory where files used by Condor are stored.
- ``$DATA_DIRECTORY`` - remote directory where the data used for execution is
  stored.
- ``$IDS_PER_JOB`` - the number of ids to assign per worker jobs
- ``$NODE_SET`` - the name of the node set to match jobs with
- ``$INPUT_DATA_FILE`` - the name of the input data file containing ids to
  process
- ``$FILE_SYSTEM_DOMAIN`` - the network domain name of the remote file system
- ``$EUPS_PATH`` - the directory containing the LSST stack used by EUPS
- ``$COMMAND`` - the command passed into the :command:`runOrca.py` job.  This
  is the command that executes across all ids given in the input data file
- ``$CTRL_EXECUTE_SETUP_PACKAGES`` - This is the listing of the :command:`setup
  -j <pkg> <version>` commands of the LSST EUPS environment at the time
  :command:`runOrca.py` is run.
