#################################
Adding a New Package to the Build
#################################

New packages intended for distribution to end users should generally be added
as a dependency of a "top level product": these are the roots of the LSST
package hierarchy. They include ``lsst_apps``, ``lsst_distrib``,
``qserv_distrib`` and ``lsst_sims``.

Before adding a new dependency to any of these products, it must be approved
through the usual :doc:`/processes/decision_process`: consensus must be
reached regarding both the name and the suitability of the new package. Before
adopting the RFC, implementation tickets should be created to cover package
creation.

After approval, code written internally by Data Management should be packaged
following the template in the `lsst/templates`_ repository. DM packaging of
third party code should proceed as described in :doc:`third_party`.

New packages must be added to the `LSST organization on GitHub`_ and access
must be granted to appropriate teams. For DM written code, these include "Data
Management" and "Overlords"; for third party code, "DM Externals" and
"Overlords" (but *not* Data Management).

The new package must be added to the `etc/repos.yaml file in the lsstsw
package`_ along with its corresponding GitHub URL. This file is
governed by a "self-merge" policy: upon opening a pull request, it will be
checked by the :ref:`build-ci-travis` system, and developers may merge without
further review on success. Refer to `RFC-75`_ for background.

The new package then needs to be added to the :file:`ups/*.table` file (and
possibly the :file:`ups/*.cfg` file) of one or more other packages in the
stack where it is used.

.. _lfs-repos:

Handling Git LFS backed repos
=================================

New Git LFS (see :doc:`/tools/git_lfs`) backed repos (or existing repos
being converted to `lfs`) require additional configuration.

- The `repos.yaml`_ entry must declare that the repository is LFS backed.

  .. code-block:: yaml

    afwdata:
      url: https://github.com/lsst/afwdata.git
      lfs: true

  See the comment block at the top of `repos.yaml`_ for additional details.

- At present, the EUPS `distrib` packaging mechanism does not support `lfs`
  backed repos.  These products **must not** be added to any ``top`` level
  meta-package or as a mandatory (non-``optional``) recursive dependency of a
  ``top`` level package.

- *Optional* dependencies must be added to `manifest.remap`_ to prevent the
  creation of broken EUPS `distrib` packages.  Please note that the "self-merge"
  policy of `RFC-75`_ does not apply to `manifest.remap`_.

  *Unlike changes merged into* `repos.yaml`_, *modifications to*
  `manifest.remap`_ *do not take immediate affect*

  recommend procedure is to attach the modification PR to a DM Jira issue on the
  ``Continuous Integration`` component.

.. _LSST organization on GitHub: https://github.com/lsst
.. _lsst/templates: https://github.com/lsst/templates
.. _Distributing third-party packages with EUPS: https://confluence.lsstcorp.org/display/LDMDG/Distributing+third-party+packages+with+EUPS
.. _etc/repos.yaml file in the lsstsw package: https://github.com/lsst/lsstsw/blob/master/etc/repos.yaml
.. _repos.yaml:  https://github.com/lsst/lsstsw/blob/master/etc/repos.yaml
.. _manifest.remap:  https://github.com/lsst/lsstsw/blob/master/etc/manifest.remap
.. _RFC-75: https://jira.lsstcorp.org/browse/RFC-75
