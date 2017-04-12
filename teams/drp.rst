#######################
Data Release Production
#######################

Princeton HPC Systems
=====================

In addition to the regular LSST-provided compute systems (:doc:`lsst-dev </services/lsst-dev>`, the :doc:`Verification Cluster </services/verification>`, etc), DRP team members have access to two clusters hosted by the `Research Computing Group <http://www.princeton.edu/researchcomputing/index.xml>`_ in Princeton.
Please refer to the Research Computing Group's pages for general information on getting started, usage policies, FAQs, etc, and be aware that you must comply with all their rules when using these systems

Obtaining Accounts
------------------

Accounts are issued on demand at the request of an appropriate PI.
For our group, that means you should speak to either Robert or John, and they will arrange one for you.
When your account has been created, you should check that you are a member of the groups ``astro``, ``hsc``, and ``lsst`` (use the :command:`groups` command).

Available Systems
-----------------

Tiger
^^^^^

`Tiger <http://www.princeton.edu/researchcomputing/computational-hardware/tiger/>`_ is a Dell/SGI cluster, providing around 10,000 CPU cores, with at least 4 GB of RAM per core, spread over 644 compute nodes.
When connecting to Tiger, you should connect to the head node ``tiger-sumire.princeton.edu`` (also known as ``tiger3.princeton.edu``) which has been reserved for HSC/LSST use.

Tiger runs version 6.8 of `Springdale Linux <https://puias.math.ias.edu>`_ (a derivative of `RHEL <https://www.redhat.com/en/technologies/linux-platforms/enterprise-linux>`_).
As such, the default toolchain is too old to work with the LSST stack.
You should therefore enable ``devtoolset-3`` before proceeding:

.. prompt:: bash

  scl enable devtoolset-3 bash

A regularly-updated LSST “shared stack” is available in :file:`/tigress/HSC/LSST/stack_tiger/` (note that the name of the cluster is embedded in the path).
To get started, try:

.. prompt:: bash

  . /tigress/HSC/LSST/stack_tiger/loadLSST.bash
  setup lsst_apps

Perseus
^^^^^^^

`Perseus <http://www.princeton.edu/researchcomputing/computational-hardware/perseus/>`_ is a Dell Beowulf cluster, providing 8,960 CPU cores, with 4.5 GB of RAM per core, spread over 320 compute nodes.
It provides broadly equivalent capabilities to Tiger, but is often less heavily loaded.
Unlike Tiger, there is no head node reserved for HSC/LSST use.
Connect to ``perseus.princeton.edu``, and be especially considerate of other users before starting long-running jobs on the head node.

Tiger runs version 7.3 of `Springdale Linux <https://puias.math.ias.edu>`_ (a derivative of `RHEL <https://www.redhat.com/en/technologies/linux-platforms/enterprise-linux>`_).
This provides a default toolchain which is appropriate for working with the LSST stack.
You should *not* enable ``devtoolset-3`` (or any other ``devtoolset``) when working with LSST code on this system.

A regularly-updated LSST “shared stack” is available in :file:`/tigress/HSC/LSST/stack_perseus/` (note that the name of the cluster is embedded in the path).
To get started, try:

.. prompt:: bash

  . /tigress/HSC/LSST/stack_perseus/loadLSST.bash
  setup lsst_apps

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
      ProxyCommand ssh hammer5.astro.princeton.edu nc %h %p

See also the `Peyton Hall tips on using SSH <http://www.astro.princeton.edu/docs/SSH>`_.

Help & Support
--------------

Contact `cses@princeton.edu <mailto:cses@princeton.edu>`_ for technical support when using these systems.
Note that neither the regular Peyton Hall sysadmins (help@astro) nor the LSST Project can provide help.
