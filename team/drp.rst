#######################
Data Release Production
#######################

Travel Calendar
===============

We use Google Calendar to keep track of group travel.
Please ask Jim, Robert or John for access.
Use it to share details of any substantial travel plans: vacations, conferences, etc.
It is not expected that you record the minutiae of everyday life: please don't bother telling us about your trip to the dentist, DMV, etc!

JIRA Usage
==========

Use the following JIRA labels to identify related work.
Please feel free to define more labels as needed; list those which might be of interested to others here.
See also the project-wide :ref:`jira-labels`.

==================== =============================================================================================================================================
Label                Meaning
==================== =============================================================================================================================================
``auxtel``           Work related to the Auxiliary Telescope.
``galmodel``         Work related to galaxy model fitting.
``hsc``              Work requested and/or carried out by the HSC team.
``pfs``              Work requested and/or carried out by the PFS team.
``SciencePipelines`` Work which should be performed by either AP (02C.03) or DRP (02C.04), but it's not (yet) clear which so we can't easily set the “team” field.
==================== =============================================================================================================================================

Princeton HPC Systems
=====================

In addition to the regular LSST-provided compute systems (:doc:`lsst-dev </services/lsst-dev>`, the :doc:`Verification Cluster </services/verification>`, etc), DRP team members have access to two clusters hosted by the `Research Computing Group <https://researchcomputing.princeton.edu>`_ in Princeton.
Please refer to the Research Computing Group's pages for information on getting started, how to connect with SSH, usage policies, FAQs, etc, and be aware that you *must* comply with all their rules when using these systems

Obtaining Accounts
------------------

Accounts are issued on demand at the request of an appropriate PI.
For our group, that means you should speak to either Robert or John, and they will arrange one for you.
When your account has been created, you should check that you are a member of the groups ``astro``, ``hsc``, and ``lsst`` (use the :command:`groups` command).

Available Systems
-----------------

Typically, LSST (and HSC) data processing is carried out using either the `Tiger`_ or `Perseus`_ clusters.
Both of these have access to regularly-updated installations of the LSST “stack” through the shared :file:`/tigress` filesystem.
Be aware, however, that you must use a version of the stack corresponding to
the operating system installed on the system you are using:

- The Tiger system (accessed through the head node ``tiger2-sumire``) should use :file:`/tigress/HSC/LSST/stack_tiger2`;
- Perseus should use :file:`/tigress/HSC/LSST/stack_perseus`.

To initialize the stack in your ``bash`` shell, run:

.. prompt:: bash

  module load rh/devtoolset/6
  . /tigress/HSC/LSST/stack_tiger2/loadLSST.bash  # Or stack_perseus, as appropriate.
  setup lsst_apps

.. note::

   The current default shared stack, described above, provides access to LSST weeklies ``w_2019_12`` and later, build using the post-:jira:`RFC-584` Conda environment.
   The alternative environment at :file:`/tigress/HSC/LSST/stack_tiger2-sumire.princeton.edu_20181028` provides access to weeklies ``w_2018_42`` through ``w_2019_12``.
   This environment may be used on either Perseus or Tiger, but be aware that it is no longer being updated.

.. _Tiger: http://www.princeton.edu/researchcomputing/computational-hardware/tiger
.. _Perseus: http://www.princeton.edu/researchcomputing/computational-hardware/perseus

Storage
-------

HSC data (both public data releases and private data, which may not be shared outside the collaboration) is available in :file:`/tigress/HSC` on both clusters.
This filesystem is available from both clusters, and you may use it to store your results.
However, note that space is at a premium, especially during our periodic HSC data release processing: please clean up any data you are not actively using.

Space is also available in your home directory, but note that it is not shared across clusters.

Cluster Usage
-------------

Jobs are managed on both systems using `SLURM <https://slurm.schedmd.com/man_index.html>`_; refer to its documentation for details.

It is occasionally useful to be able to bring up an interactive shell on a compute node.
The following should work:

.. prompt:: bash

  salloc --nodes 1 --ntasks 16 --time=1:00:00  # hh:mm:ss

Connecting from Outside Princeton
---------------------------------

Access to all of the Princeton clusters is only available from within the Princeton network.
If you are connecting from the outside, you will need to bounce through another host on campus first.
Options include:

- Bouncing your connection through a `host on the Peyton network <http://www.astro.princeton.edu/docs/Hardware>`_ (this is usually the easiest way to go);
- Making use of the `University's VPN service <https://www.net.princeton.edu/vpn/>`_.

If you choose the first option, you may find the ``ProxyCommand`` option to SSH helpful.
For example, adding the follwing to :file:`~/.ssh/config` will automatically route your connection to the right place when you run :command:`ssh tiger`::

  Host tiger
      Hostname tiger3.princeton.edu
      ProxyCommand ssh coma.astro.princeton.edu -W %h:%p

See also the `Peyton Hall tips on using SSH <http://www.astro.princeton.edu/docs/SSH>`_.

Help & Support
--------------

Contact `cses@princeton.edu <mailto:cses@princeton.edu>`_ for technical support when using these systems.
Note that neither the regular Peyton Hall sysadmins (help@astro) nor the LSST Project can provide help.
