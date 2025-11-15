#######################
Data Release Production
#######################

.. _drp-travel-calendar:

Travel Calendar
===============

We use Google Calendar to keep track of group travel.
Please ask Jim, Robert or Yusra for access.
Use it to share details of any substantial travel plans: vacations, conferences, etc.
It is not expected that you record the minutiae of everyday life: please don't bother telling us about your trip to the dentist, DMV, etc!

.. _drp-jira-usage:

JIRA Usage
==========

Use the following JIRA labels to identify related work.
Please feel free to define more labels as needed; list those which might be of interested to others here.
See also the project-wide :ref:`jira-labels`.

.. list-table:: Label and Meaning
   :header-rows: 1

   * - Label
     - Meaning
   * - ``auxtel``
     - Work related to the Auxiliary Telescope.
   * - ``galmodel``
     - Work related to galaxy model fitting.
   * - ``hsc``
     - Work requested and/or carried out by the HSC team.
   * - ``pfs``
     - Work requested and/or carried out by the PFS team.

.. _drp-princeton-hpc-systems:

Princeton HPC Systems
=====================

In addition to the `regular LSST-provided compute systems <https://df-ops.lsst.io/users/lsst-login.html>`__, DRP team members have access to a number of clusters hosted by the `Research Computing Group <https://researchcomputing.princeton.edu>`_ in Princeton.
Please refer to the Research Computing Group's pages for information on getting started, how to connect with SSH, usage policies, FAQs, etc.
Be aware that you *must* comply with all their rules when using these systems.

.. _drp-princeton-obtaining-accounts:

Obtaining Accounts
------------------

Accounts are issued on demand at the request of an appropriate PI.
For our group, that means you should speak to either Robert or Yusra, and they will arrange one for you.
When your account has been created, you should check that you are a member of the groups ``astro``, ``hsc``, ``lsst`` and ``rubin`` (use the :command:`groups` command to check).

.. note::

   The ``lsst`` group is a shared group which allows all Tiger3 users to access the shared stack.
   Being a member of this group does not provide access to shared Rubin data.
   Instead, the ``rubin`` group is used to control access to Rubin data repositories.
   In the prior Tiger2 cluster, the ``hsc`` group was used for both purposes.
   If you find that you need to be made a member of any of these groups, please contact Robert, Yusra or Lee.

.. _drp-princeton-available-systems:

Available Systems
-----------------

Typically, LSST (and HSC/DECam) data processing is carried out using the `Tiger`_ cluster.

.. _Tiger: https://researchcomputing.princeton.edu/systems/tiger

The Princeton astronomical software group owns a head node on the Tiger cluster called ``tiger3-sumire``.
You can use this node for building software and running small and/or short-lived jobs.

.. note::

   The ``/project`` filesystems are NFS-mounted on the Princeton clusters.
   As a consequence, the performance of these filesystems will be limited by the network speed between our head node and the filesystem.
   For anything more than even the most basic testing, it is therefore strongly recommended that batch processing takes place in your ``/scratch/gpfs/RUBIN/user/${USER}`` space (see :ref:`drp-princeton-cluster-usage`).

.. _drp-princeton-shared-stack:

Shared Stack
------------

The Tiger cluster has access to regularly-updated installations of the LSST Science Pipelines (the “stack”) through the shared :file:`/scratch/gpfs` filesystem.
The stack is automatically updated every Thursday evening (i.e., 24h after a new weekly gets cut), and is usually ready for use by Friday morning.
To initialize the stack in your shell, run:

.. code-block:: shell

   source /scratch/gpfs/LSST/stack/loadLSST.sh
   setup lsst_distrib

By default, the most recent Rubin Environment will be used, as provided by the ``LSST_CONDA_ENV_NAME`` variable within the ``loadLSST.sh`` script.
If you wish to use a different Rubin Environment, you can do so by first setting the ``LSST_CONDA_ENV_NAME`` variable to the desired version before setting up the Science Pipelines:

.. code-block:: shell

   export LSST_CONDA_ENV_NAME="lsst-scipipe-12.0.0"
   source /scratch/gpfs/LSST/stack/loadLSST.sh
   setup lsst_distrib -t <old_version_tag>

   # To reset to the default, unset the variable before sourcing the script:
   # unset LSST_CONDA_ENV_NAME

A list of all currently installed Rubin Environments can be found by running: ``mamba env list``.

.. note::

   The current default shared stack, described above, is a symbolic link to the latest build using the post-:jira:`RFC-584` Conda environment.
   Older builds, if any, are available in ``/scratch/gpfs/LSST/stacks`` with the syntax ``stack_YYYYMMDD``.

.. _drp-princeton-repositories:

Repositories
------------

We currently maintain a single data repository for general use on the Princeton clusters:

- ``/scratch/gpfs/RUBIN/repo/main``: The primary HSC/LSST butler data repository, containing raw HSC RC2 data.

For information on accessing repositories, including setting up required permissions, see the top-level ``/scratch/gpfs/RUBIN/repo/README.md`` file.

.. note::

   You will not be able to access the data within these repositories without first following the **Database Authentication** instructions in the above ``README.md`` file.

.. _drp-princeton-storage:

Storage
-------

HSC data (both public data releases and private data, which may not be shared outside the collaboration) are available in :file:`/projects/HSC`.
This space may also be used to store your results.
Note however that space is at a premium; please clean up any data you are not actively using.
Also, be sure to set :command:`umask 002` so that your colleagues can reorganize the shared space.

For long-term storage of user data, shared space is available in :file:`/projects/HSC/users/<YourNetID>` (you may need to make this directory yourself).
This space is backed up, but it is **not** visible to the compute nodes.

For temporary data processing storage, shared space is available in :file:`/scratch/gpfs/RUBIN/user/<YourNetID>` (you may need to make this directory yourself).
This General Parallel File System (GPFS) space is large and visible from all Princeton clusters, however, it is **not** backed up.
More information on `Princeton cluster data storage <https://researchcomputing.princeton.edu/support/knowledge-base/data-storage>`_ can be found online.

Space is also available in your home directory, but note that it is not shared across clusters.

Use the :command:`checkquota` command to check your current storage and your storage limits.
More information on storage limits, including on how to request a quota increase, can be found at `this link <https://researchcomputing.princeton.edu/support/knowledge-base/checkquota>`_.

.. _drp-princeton-cluster-usage:

Cluster Usage
-------------

Jobs are managed on cluster systems using `SLURM <https://slurm.schedmd.com>`_; refer to its documentation for details.

Batch processing functionality with the Science Pipelines is provided by the `LSST Batch Processing Service (BPS) <https://pipelines.lsst.io/modules/lsst.ctrl.bps>`_ module.
BPS on the Princeton clusters is configured to work with the `ctrl_bps_parsl plugin <https://github.com/lsst/ctrl_bps_parsl>`_, which uses the `Parsl <https://parsl-project.org>`_ workflow engine to submit jobs to SLURM.

To submit a job to the cluster, you will first need to create a YAML configuration file for BPS.
For convenience, two generic configuration files have been constructed on disk at ``/scratch/gpfs/RUBIN/bps/bps_tiger.yaml`` and ``/scratch/gpfs/RUBIN/bps/bps_tiger_clustering.yaml``.
The former is intended for general use, while the latter is intended for use with quantum clustering enabled.
These files may either be used directly when submitting a job or copied to your working directory and modified as needed.
The following example shows how to submit a job using the generic configuration file:

.. code-block:: shell

   # Set the following environment variables to ensure that
   # the Science Pipelines and BPS do not try to use more
   # threads than are available on a single node.
   export OMP_NUM_THREADS=1
   export NUMEXPR_MAX_THREADS=1

   # All submissions must be made from your /scratch/gpfs directory.
   cd /scratch/gpfs/RUBIN/user/${USER}

   # Save the output of the BPS submit command to a log file
   # (optional, but recommended).
   LOGFILE=$(realpath bps_log.txt)

   # Submit a job to the cluster.
   date | tee $LOGFILE; \
   $(which time) -f "Total runtime: %E" \
   bps submit /scratch/gpfs/RUBIN/bps/bps_tiger.yaml \
   --compute-site tiger_1n_112c_1h \
   -b /scratch/gpfs/RUBIN/repo/main \
   -i HSC/RC2/defaults \
   -o u/${USER}/scratch/bps_test \
   -p $DRP_PIPE_DIR/pipelines/HSC/DRP-RC2.yaml#step1 \
   -d "instrument='HSC' AND visit=1228" \
   2>&1 | tee -a $LOGFILE; \
   date | tee -a $LOGFILE

   # Additional command-line arguments may be passed to BPS using the
   # --extra-qgraph-options argument, for example, to add a config override:
   # --extra-qgraph-options "-c isr:doOverscan=False"

A number of different compute sites are available for use with BPS as defined in the generic configuration file.
Select a compute site using the syntax ``tiger_${NODES}n_${CORES}c_${TIME}h``, replacing the variables by the appropriate number of nodes, cores and hours.
You can check the available compute sites defined in the generic configuration file using: ``grep "tiger_" /scratch/gpfs/RUBIN/bps/bps_tiger.yaml``.
The following table lists the available compute site dimensions and their associated options:

.. list-table::
   :header-rows: 1

   * - Dimension
     - Options
   * - Nodes
     - 1, 10
   * - Cores per Node
     - 1, 28, 112
   * - Walltime (Hours)
     - 1, 5, 24, 72

A list of all available nodes is given using the :command:`snodes` command, or alternatively using :command:`sinfo`:

.. code-block:: shell

   sinfo -N -l

To get an estimate of the start time for any submitted jobs, the :command:`squeue` command may be used:

.. code-block:: shell

   squeue -u ${USER} --start

To show detailed information about a given node, the :command:`scontrol` may be used:

.. code-block:: shell

   scontrol show node <node_name>

It is occasionally useful to be able to directly log in to an interactive shell on a compute node.
The following should work:

.. code-block:: shell

   salloc --nodes 1 --ntasks 16 --time=1:00:00  # hh:mm:ss

See `Useful Slurm Commands <https://researchcomputing.princeton.edu/support/knowledge-base/slurm#commands>`_ for additional tools which may be used in conjunction with Slurm.

.. _drp-princeton-connecting-outside:

Connecting from Outside Princeton
---------------------------------

Access to all of the Princeton clusters is only available from within the Princeton network.
If you are connecting from the outside, you will need to bounce through another host on campus first.
Options include:

- Jumping through the Research Computing ``tigressgateway`` host;
- Bouncing your connection through a `host on the Peyton network <http://www.astro.princeton.edu/docs/Hardware>`_ (this is usually the easiest way to go);
- Making use of the `University's VPN service <https://www.net.princeton.edu/vpn/>`_.

If you choose the first or second options, you may find the ``ProxyCommand`` or ``ProxyJump`` options to SSH helpful.
For example, adding the following to :file:`~/.ssh/config` will automatically route your connection to the right place when you run :command:`ssh tiger`::

    Host tiger
        HostName tiger3-sumire.princeton.edu
        ProxyCommand ssh coma.astro.princeton.edu -W %h:%p

The following SSH configuration allows access via the Research Computing gateway::

    Host tigressgateway
        HostName tigressgateway.princeton.edu
    Host tiger* tigressdata*
        ProxyCommand ssh -q -W %h:%p tigressgateway.princeton.edu
    Host tiger
        Hostname tiger3-sumire.princeton.edu

or alternatively::

    Host tigressgateway
        HostName tigressgateway.princeton.edu
    Host tiger
        Hostname tiger3-sumire.princeton.edu
        ProxyJump tigressgateway

(It may also be necessary to add a ``User`` line under ``Host tigressgateway`` if there is a mismatch between your local and Princeton usernames.)
Entry to ``tigressgateway`` requires `2FA <https://www.princeton.edu/duoportal>`_;
we recommend using the ``ControlMaster`` feature of SSH to persist connections, e.g.::

    ControlMaster auto
    ControlPath ~/.ssh/cm/%r@%h:%p
    ControlPersist 5m

(It may be necessary to create the directory ``~/.ssh/cm``.)

See also the `Peyton Hall tips on using SSH <http://www.astro.princeton.edu/docs/SSH>`_.

.. _drp-princeton-help-support:

Help & Support
--------------

Contact the Computational Science and Engineering Support group using `cses@princeton.edu <mailto:cses@princeton.edu>`_ for technical support when using these systems.
Note that neither the regular Peyton Hall sysadmins (help@astro) nor the LSST Project can provide help.
