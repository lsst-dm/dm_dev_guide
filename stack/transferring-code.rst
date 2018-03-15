##################################
Transferring Code Between Packages
##################################

When transferring code between LSST packages with different git repositories,
the following procedure should be used:

#. Create a JIRA issue that includes the code transfer as part of its work package.

#. In the origin repository:

    #. Create the usual ``tickets/DM-XXXX`` issue branch.

    #. Create a ``tickets/DM-XXXX-transfer`` branch from the
       ``tickets/DM-XXXX`` branch.

    #. On the transfer branch, remove code and files that will be transferred.
       All commit messages should contain the name of the destination package
       and the transfer branch name (``tickets/DM-xxxx-transfer``).

    #. On the transfer branch, make any additional modifications to the origin
       repository to return it to a buildable/testable state (one or more
       commits, distinct from the remove commit(s)).

    #. Merge the transfer branch back to the regular issue branch using
       ``--no-ff`` to preserve the transfer branch name in the merge commit.

#. In the destination repository:

    #. Create the usual ``tickets/DM-XXXX`` issue branch.

    #. Create a ``tickets/DM-XXXX-transfer`` branch from the
       ``tickets/DM-XXXX`` branch.

    #. On the transfer branch, add the new code and files from the origin
       repository.  All commit messages should contain the name of the origin
       package and the transfer branch name (``tickets/DM-xxxx-transfer``).

    #. On the transfer branch, make any additional modifications to the origin
       repository to return it to a buildable/testable state (one or more
       commits, distinct from the commit(s) that added code from the origin
       repository).

    #. Merge the transfer branch back to the regular issue branch using
       ``--no-ff`` to preserve the transfer branch name in the git commit.

#. Make further changes as necessary on the ``tickets/DM-XXXX`` branches and have
   the issue reviewed and merged to master as usual.

#. Summarize the code transfer on the `DM Stack Package History`_ page.

Requirements to keep in mind:

* Commits made directly on the ``tickets/DM-XXXX`` branch should be
  buildable/testable.

* The ``tickets/DM-XXXX-transfer`` branch should contain only commits that move
  code or are necessary to get it working at a basic level in the new package.

* Commits that transfer code should not be mixed with commits that modify the
  code to adapt it to its new home (e.g. namespace changes).

Note that this procedure contains no attempt to actually move, filter, or
summarize the git history from the origin package in the destination package.
Instead, we expect to retain that history in the origin package, using commit
messages, the transfer branches, and the `DM Stack Package History`_ page to
provide a link between the destination and the origin packages.

See `RFC-33`_ for the motivation and discussion behind this policy.

.. _RFC-33: https://jira.lsstcorp.org/browse/rfc-33
.. _DM Stack Package History: https://confluence.lsstcorp.org/display/DM/DM+Stack+Package+History
