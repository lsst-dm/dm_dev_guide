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

+--------------+----------------------------------------------------+
|    Label     |                      Meaning                       |
+==============+====================================================+
| ``auxtel``   | Work related to the Auxiliary Telescope.           |
+--------------+----------------------------------------------------+
| ``galmodel`` | Work related to galaxy model fitting.              |
+--------------+----------------------------------------------------+
| ``hsc``      | Work requested and/or carried out by the HSC team. |
+--------------+----------------------------------------------------+
| ``pfs``      | Work requested and/or carried out by the PFS team. |
+--------------+----------------------------------------------------+

.. _drp-princeton-hpc-systems:

Princeton HPC Systems
=====================

In addition to the :doc:`regular LSST-provided compute systems </usdf/lsst-login>`, DRP team members have access to a number of clusters hosted by the `Research Computing Group <https://researchcomputing.princeton.edu>`_ in Princeton.
Please refer to the Research Computing Group's pages for information on getting started, how to connect with SSH, usage policies, FAQs, etc.
Be aware that you *must* comply with all their rules when using these systems.

.. _drp-princeton-obtaining-accounts:

Obtaining Accounts
------------------

Accounts are issued on demand at the request of an appropriate PI.
For our group, that means you should speak to either Robert or Yusra, and they will arrange one for you.
When your account has been created, you should check that you are a member of the groups ``astro``, ``hsc``, and ``lsst`` (use the :command:`groups` command).

.. note::

  A new user account may not have the ``lsst`` group added by default.
  This group is not being used for anything at present, so it shouldn't be a problem if you are not a member of it.
  If you find that you do need to be a member of this group, please contact Robert or Yusra.

.. _drp-princeton-available-systems:

Available Systems
-----------------

Typically, LSST (and HSC/DECam) data processing is carried out using the `Tiger`_ cluster.

.. _Tiger: https://researchcomputing.princeton.edu/systems/tiger

The Princeton astronomical software group owns a head node on the Tiger cluster called ``tiger2-sumire``.
You can use this node for building software and running small and/or short-lived jobs.

.. _drp-princeton-shared-stack:

Shared Stack
------------

The Tiger cluster has access to regularly-updated installations of the LSST Science Pipelines (the “stack”) through the shared :file:`/scratch/gpfs` filesystem.
The stack is automatically updated every Thursday evening (i.e., 24h after a new weekly gets cut). To initialize the stack in your shell, run:

.. code-block:: shell

  source /scratch/gpfs/HSC/LSST/stack/loadLSST.sh
  setup lsst_distrib

By default, the most recent Rubin Environment will be used, as provided by the ``LSST_CONDA_ENV_NAME`` variable within the ``loadLSST.sh`` script.
If you wish to use a different version of the stack, you can do so by first setting the ``LSST_CONDA_ENV_NAME`` variable to the desired version before running ``setup lsst_distrib``:

.. code-block:: shell

  export LSST_CONDA_ENV_NAME="lsst-scipipe-4.0.1"
  source /scratch/gpfs/HSC/LSST/stack/loadLSST.sh
  setup lsst_distrib

  # To reset to the default, uncomment this line:
  # unset LSST_CONDA_ENV_NAME

A list of all currently installed Rubin Environments can be found by running: ``mamba env list``.

.. note::

  The current default shared stack, described above, is a symbolic link to the latest build using the post-:jira:`RFC-584` Conda environment.
  Older builds, if any, are available in ``/scratch/gpfs/HSC/LSST/`` with the syntax ``stack_YYYYMMDD``.

.. _drp-princeton-repositories:

Repositories
------------

The primary HSC/LSST butler data repository is located at: ``/projects/HSC/repo/main``.
All raw HSC data on-disk has been ingested into this gen3 repo.
For information on accessing and using this repository, including setting up required permissions, see the contained ``/projects/HSC/repo/main/README.md`` file.

.. note::

  You will not be able to access the data within this repository without first following the **Database Authentication** instructions in the above ``README.md`` file.

.. _drp-princeton-storage:

Storage
-------

HSC data (both public data releases and private data, which may not be shared outside the collaboration) are available in :file:`/projects/HSC`.
This space may also be used to store your results.
Note however that space is at a premium; please clean up any data you are not actively using.
Also, be sure to set :command:`umask 002` so that your colleagues can reorganize the shared space.

For temporary data processing storage, shared space is available in :file:`/scratch/gpfs/<YourNetID>` (you may need to make this directory yourself).
This General Parallel File System (GPFS) space is large and visible from all Princeton clusters, however, it is **not** backed up.
More information on `Princeton cluster data storage <https://researchcomputing.princeton.edu/support/knowledge-base/data-storage>`_ can be found online.

Space is also available in :file:`/scratch/<yourNetID>` and in your home directory, but note that they are not shared across clusters (and, in the case of ``/scratch``, not backed up).

Use the :command:`checkquota` command to check your current storage and your storage limits.
More information on storage limits, including on how to request a quota increase, can be found at `this link <https://researchcomputing.princeton.edu/support/knowledge-base/checkquota>`_.

.. _drp-princeton-cluster-usage:

Cluster Usage
-------------

Jobs are managed on cluster systems using `SLURM <https://slurm.schedmd.com>`_; refer to its documentation for details.

Batch processing functionality with the Science Pipelines is provided by the `LSST Batch Processing Service (BPS) <https://pipelines.lsst.io/modules/lsst.ctrl.bps>`_ module.
BPS on the Princeton clusters is configured to work with the `ctrl_bps_parsl plugin <https://github.com/lsst/ctrl_bps_parsl>`_, which uses the `Parsl <https://parsl-project.org>`_ workflow engine to submit jobs to SLURM.

.. note::

  Due to changes that occurred in Q1 2023 relating to how disks are mounted on the Tiger cluster, use of the ``ctrl_bps_parsl`` plugin will return an ``OSError`` when used in conjunction with any weeklies older than ``w_2023_09``.
  To make use of BPS with older weeklies, you will need to build and set up the ``ctrl_bps_parsl`` plugin yourself.
  Refer to the `ctrl_bps_parsl plugin documentation <https://github.com/lsst/ctrl_bps_parsl>`_ and links therein for further details.

To submit a job to the cluster, you will first need to create a YAML configuration file for BPS.
For convenience, a generic configuration file has been constructed on disk at ``/projects/HSC/LSST/bps/bps_tiger.yaml``.
This file may either be used directly when submitting a job or copied to your working directory and modified as needed.
The following example shows how to submit a job using the generic configuration file:

.. code-block:: shell

  # Set the following environment variables to ensure that
  # the Science Pipelines and BPS do not try to use more
  # threads than are available on a single node.
  export OMP_NUM_THREADS=1
  export NUMEXPR_MAX_THREADS=1

  # All submissions must be made from your /scratch/gpfs directory.
  cd /scratch/gpfs/$USER

  # Save the output of the BPS submit command to a log file
  # (optional, but recommended).
  LOGFILE=/path/to/my/log/file.log

  # Submit a job to the cluster.
  date | tee -a $LOGFILE; \
  $(which time) -f "Total runtime: %E" \
  bps submit /projects/HSC/LSST/bps/bps_tiger.yaml \
  --compute-site tiger_1h_1n_40c \
  -b /projects/HSC/repo/main \
  -i HSC/RC2/defaults \
  -o u/$USER/test \
  -p $DRP_PIPE_DIR/pipelines/HSC/DRP-RC2.yaml#step1 \
  -d "instrument='HSC' AND visit=1228" \
  2>&1 | tee -a $LOGFILE; \
  date | tee -a $LOGFILE

  # Additional command-line arguments may be passed to BPS
  # using the --extra-qgraph-options argument, e.g.:
  # --extra-qgraph-options "isr:doOverscan=False"

A number of different compute sites are available for use with BPS as defined in the generic configuration file.
Select a compute site using the syntax ``tiger_Xh_Xn_Xc``, where ``X`` is replaced by the appropriate number of hours, nodes, and cores.
You may check the available compute sites defined in the generic configuration file using: ``grep "tiger" /projects/HSC/LSST/bps/bps_tiger.yaml``.
The following table lists the available compute site dimensions and their associated options:

+------------------+-----------+
|    Dimension     |  Options  |
+==================+===========+
| Walltime (Hours) | 1, 5, 24  |
+------------------+-----------+
| Nodes            | 1, 4      |
+------------------+-----------+
| Cores per Node   | 1, 10, 40 |
+------------------+-----------+

It is occasionally useful to be able to bring up an interactive shell on a compute node.
The following should work:

.. code-block:: shell

  salloc --nodes 1 --ntasks 16 --time=1:00:00  # hh:mm:ss

A list of all available nodes is given using the :command:`snodes` command.
To get an estimate of the start time for any submitted jobs, use this command:

.. code-block:: shell

  squeue -u $USER --start

See `Useful Slurm Commands <https://researchcomputing.princeton.edu/support/knowledge-base/slurm#commands>`_ for additional tools which may be used in conjunction with Slurm.

.. _drp-princeton-connecting-outside:

Connecting from Outside Princeton
---------------------------------

Access to all of the Princeton clusters is only available from within the Princeton network.
If you are connecting from the outside, you will need to bounce through another host on campus first.
Options include:

- Bouncing your connection through a `host on the Peyton network <http://www.astro.princeton.edu/docs/Hardware>`_ (this is usually the easiest way to go);
- Making use of the `University's VPN service <https://www.net.princeton.edu/vpn/>`_.
- Using the Research Computing gateway.

If you choose the first option, you may find the ``ProxyCommand`` option to SSH helpful.
For example, adding the following to :file:`~/.ssh/config` will automatically route your connection to the right place when you run :command:`ssh tiger`::

  Host tiger
      HostName tiger2-sumire.princeton.edu
      ProxyCommand ssh coma.astro.princeton.edu -W %h:%p

The following SSH configuration allows access via the Research Computing gateway::

    Host tigressgateway
        HostName tigressgateway.princeton.edu
    Host tiger* tigressdata*
        ProxyCommand ssh -q -W %h:%p tigressgateway.princeton.edu
    Host tiger
        Hostname tiger2-sumire.princeton.edu

(It may also be necessary to add a ``User`` line under ``Host tigressgateway`` if there is a mismatch between your local and Princeton usernames.)
Entry to ``tigressgateway`` requires `2FA <https://www.princeton.edu/duoportal>`_;
we recommend using the ``ControlMaster`` feature of SSH to persist connections, e.g.::

    ControlMaster auto
    ControlPath ~/.ssh/controlmaster-%r@%h:%p
    ControlPersist 5m

See also the `Peyton Hall tips on using SSH <http://www.astro.princeton.edu/docs/SSH>`_.

.. _drp-princeton-help-support:

Help & Support
--------------

Contact the Computational Science and Engineering Support group using `cses@princeton.edu <mailto:cses@princeton.edu>`_ for technical support when using these systems.
Note that neither the regular Peyton Hall sysadmins (help@astro) nor the LSST Project can provide help.
