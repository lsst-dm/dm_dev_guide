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

+---------------+-----------------------------------------------------+
| Label         | Meaning                                             |
+===============+=====================================================+
| ``auxtel``    | Work related to the Auxiliary Telescope.            |
+---------------+-----------------------------------------------------+
| ``galmodel``  | Work related to galaxy model fitting.               |
+---------------+-----------------------------------------------------+
| ``hsc``       | Work requested and/or carried out by the HSC team.  |
+---------------+-----------------------------------------------------+
| ``pfs``       | Work requested and/or carried out by the PFS team.  |
+---------------+-----------------------------------------------------+

.. _drp-princeton-hpc-systems:

Princeton HPC Systems
=====================

In addition to the :doc:`regular LSST-provided compute systems </usdf/lsst-login>`, DRP team members have access to a number of clusters hosted by the `Research Computing Group <https://researchcomputing.princeton.edu>`_ in Princeton.
Please refer to the Research Computing Group's pages for information on getting started, how to connect with SSH, usage policies, FAQs, etc.
Be aware that you *must* comply with all their rules when using these systems

.. _drp-princeton-obtaining-accounts:

Obtaining Accounts
------------------

Accounts are issued on demand at the request of an appropriate PI.
For our group, that means you should speak to either Robert or Yusra, and they will arrange one for you.
When your account has been created, you should check that you are a member of the groups ``astro``, ``hsc``, and ``lsst`` (use the :command:`groups` command).

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

The Tiger cluster has access to regularly-updated installations of the LSST “stack” through the shared :file:`/tigress` filesystem.
The stack is automatically updated every Thursday evening (i.e., 24h after a new weekly gets cut).
To initialize the stack in your shell, run:

.. prompt:: bash

  source /tigress/HSC/LSST/stack/loadLSST.sh
  setup lsst_distrib

.. note::

   The current default shared stack, described above, is a symbolic link to the latest build using the post-:jira:`RFC-584` Conda environment.
   Older builds are also available in ``/tigress/HSC/LSST/stack`` with the syntax ``stack_YYYYMMDD``.

.. _drp-princeton-repositories:

Repositories
------------

The primary HSC/LSST butler data repository is located at: ``/projects/HSC/repo/main``.
All raw HSC data on-disk has been ingested into this gen3 repo.
For more information on accessing and using this repository, including setting up required permissions, see the contained ``README.md`` file.

.. _drp-princeton-storage:

Storage
-------

HSC data (both public data releases and private data, which may not be shared outside the collaboration) are available in :file:`/tigress/HSC`.
This space may also be used to store your results.
Note however that space is at a premium; please clean up any data you are not actively using.
Also, be sure to set :command:`umask 002` so that your colleagues can reorganize the shared space.

For temporary data processing storage, shared space is available in :file:`/scratch/gpfs/<YourNetID>` (you may need to make this directory yourself).
This General Parallel File System (GPFS) space is large and visible from all Princeton clusters, however, it is **not** backed up.
More information on `Princeton cluster data storage <https://researchcomputing.princeton.edu/support/knowledge-base/data-storage>`_ can be found online.

Space is also available :file:`/scratch/<yourNetID>` and in your home directory, but note that they are not shared across clusters (and, in the case of ``/scratch``, not backed up).

Use the :command:`checkquota` command to check your current storage and your storage limits.
More information on storage limits, including on how to request a quota increase, can be found at `this link <https://researchcomputing.princeton.edu/support/knowledge-base/checkquota>`_.

.. _drp-princeton-cluster-usage:

Cluster Usage
-------------

Jobs are managed on both systems using `SLURM <https://slurm.schedmd.com>`_; refer to its documentation for details.

It is occasionally useful to be able to bring up an interactive shell on a compute node.
The following should work:

.. prompt:: bash

  salloc --nodes 1 --ntasks 16 --time=1:00:00  # hh:mm:ss

A list of all available nodes is given using the :command:`snodes` command.
To get an estimate of the start time for any submitted jobs, use this command:

.. prompt:: bash

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
