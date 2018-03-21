#################################
Adding a New Package to the Build
#################################

New packages intended for distribution to end users should generally be added
as a dependency of a "top-level product:" these are the roots of the LSST
package hierarchy. They include ``lsst_apps``, ``lsst_distrib``,
``qserv_distrib`` and ``lsst_sims``.

Before adding a new dependency to any of these products, it must be approved
through the :doc:`RFC process </processes/decision_process>`. Consensus must be
reached regarding both the name and the suitability of the new package. Before
adopting the RFC, implementation tickets should be created to cover package
creation.

After approval, code written internally by Data Management should be packaged
following the template in the `lsst/templates`_ repository. DM packaging of
third party code should proceed as described in :doc:`packaging-third-party-eups-dependencies`.

New packages must be added to the `LSST organization on GitHub`_ and access
must be granted to appropriate teams. For DM-written code, these include "Data
Management" and "Overlords." For third-party code, use the "DM Externals" and
"Overlords" (but *not* "Data Management") teams.

The new package must be added to the `etc/repos.yaml file in the lsst/repos
repository`_ along with its corresponding GitHub URL. This file is governed by
a "self-merge" policy: upon opening a pull request, it will be checked by the
:doc:`stack-os-matrix Jenkins job </stack/jenkins-stack-os-matrix>`, and developers may merge without further review
on success. Refer to :jira:`RFC-75` for background.

The new package then needs to be added to the :file:`ups/*.table` file (and
possibly the :file:`ups/*.cfg` file) of one or more other packages in the
stack where it is used.

.. _github-repository-configuration:

Configuring GitHub Repositories
===============================

All LSST DM repositories on GitHub must be configured to protect the ``master`` branch and to ensure that the merge button for pull requests can not be pushed without the branch being up to date with ``master``.
There are a number of settings required to ensure this and they are described below with URLs referring to the ``afw`` package.
Replace ``afw`` with the relevant package name to get to the correct page on GitHub.

1. On the main settings page for the repository, https://github.com/lsst/afw/settings, disable squash and rebase merging:

.. image:: /_static/build-ci/github_merge_button_settings.png

2. Configure ``master`` branch to enable protections.
For ``afw`` this is located at https://github.com/lsst/afw/settings/branches/master and can also be found from the "Branches" sidebar item on the settings screen.
Select the "Protect this branch" option and this will make available additional checks.
You should also enable status checks and require that branches be up to date before merging.
With this enabled people will be able to use the GitHub merge button on Pull Requests and know that the :ref:`standard process <workflow-code-review-merge>` is being adhered to.

.. image:: /_static/build-ci/github_branch_protection.png

In the image above no automated status checks are being performed.
Whilst not required, we recommend that some basic checks are enabled on repositories using Travis.
This will not replace normal testing with :doc:`Jenkins job <jenkins-stack-os-matrix>` but for packages that have been updated to :ref:`use flake8 <testing-flake8>` it is useful to add a simple Travis script like the following:

.. literalinclude:: examples/flake8-travis.yml
  :language: yaml

For packages containing C++ that have been tidied up using ``clang`` tools, you may consider adding a Travis check that runs the tidy tool and does a ``diff`` with the repository.

Once the Travis script has been written, Travis can be enabled on the "Integrations & services" settings screen, https://github.com/lsst/afw/settings/installations, and Travis can then be added to the branch protection settings.
Your branch protections screen should then look something like this:

.. image:: /_static/build-ci/github_branch_protection_travis.png

.. note::
  It takes a few minutes from enabling Travis to GitHub making the Travis option available on the branch protection screen.

.. _lfs-repos:

Handling Git LFS-backed repos
=============================

New :doc:`Git LFS-backed </git/git-lfs>` repos (or existing repos
being converted to LFS) require additional configuration.

- The `repos.yaml`_ entry must declare that the repository is LFS backed:

  .. code-block:: yaml

      afwdata:
        url: https://github.com/lsst/afwdata.git
        lfs: true

  See the comment block at the top of `repos.yaml`_ for additional details.

- At present, the EUPS distrib packaging mechanism does not support
  LFS-backed repos. These products **must not** be added to any top-level
  meta-package or as a mandatory (non-``optional``) recursive dependency of a
  top-level package.

- *Optional* dependencies must be added to `manifest.remap`_ to prevent the
  creation of broken EUPS distrib packages. Please note that the "self-merge"
  policy (:jira:`RFC-75`) does not apply to `manifest.remap`_.

  Unlike changes merged into `repos.yaml`_, modifications to
  `manifest.remap`_ do not take immediate affect.

  We recommend that you attach the modification PR to a DM Jira issue on the
  ``Continuous Integration`` component.

.. _LSST organization on GitHub: https://github.com/lsst
.. _lsst/templates: https://github.com/lsst/templates/tree/master/project_templates/stack_package
.. _Distributing third-party packages with EUPS: https://confluence.lsstcorp.org/display/LDMDG/Distributing+third-party+packages+with+EUPS
.. _etc/repos.yaml file in the lsst/repos repository: https://github.com/lsst/repos/blob/master/etc/repos.yaml
.. _repos.yaml: https://github.com/lsst/repos/blob/master/etc/repos.yaml
.. _manifest.remap:  https://github.com/lsst/lsstsw/blob/master/etc/manifest.remap
