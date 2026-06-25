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

    #. Make the appropriate changes to support continued import of public interfaces from the origin
       repository with a deprecation warning. See :ref:`providing-stable-interfaces` for more details.

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
   the issue reviewed and merged to main as usual.

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


.. _providing-stable-interfaces:

Providing Stable Interfaces
===========================

Transferring code between packages is a breaking change and stable interfaces should be provided on a
best-effort basis to support external users.
If the origin repository is downstream of the destination (as is typically the case),
this can be achieved by importing code from the destination repository with an alias,
trivially repackaging it following the deprecation procedure described in
:doc:`Deprecating Interfaces <deprecating-interfaces>`.

As an example, if a Python class ``ConfigurableAction`` is moved from package ``analysis_tools`` (downstream) to ``pex_config`` (upstream),

.. code-block:: python

    from lsst.pex.config import ConfigurableAction as ConfigurableActionNew
    from depecated.sphinx import deprecated

    __all__ = ["ConfigurableAction"]

    @deprecated(reason="Moved to lsst.pex.config",
                version="v22.0",
                category=FutureWarning)
    class ConfigurableAction(ConfigurableActionNew):
        pass

In the relative less common case of moving code downstream, the following pattern can be used:

.. code-block:: python

    import warnings

    try:
        from lsst.drp.tasks.assemble_coadd import *  # noqa: F401, F403
    except ImportError as error:
        error.msg += ". Please import the coaddition tasks from drp_tasks package."
        raise error
    finally:
        warnings.warn("lsst.pipe.tasks.assembleCoadd is deprecated and will be removed after v27; "
                      "Please use lsst.drp.tasks.assemble_coadd instead.",
                      DeprecationWarning,
                      stacklevel=2
                      )

This allows the code to be imported from the old location (with a deprecation warning) with a fully built
version of the Science Pipelines, but does not introduces cyclic dependencies during the build process.
