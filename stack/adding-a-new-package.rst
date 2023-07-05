#################################
Adding a New Package to the Build
#################################

.. _adding_new_package:

Creating a new package
======================

To create a new LSST package, send a "create project" message to ``@sqrbot-jr`` on the LSST Slack and select "LSST EUPS package" as the project type.
Follow the prompts to select the GitHub organization (choose ``lsst`` for the `LSST organization on GitHub`_ for packages that you plan to add to the full distribution via RFC, as described below) and the specific flavor of package (e.g. ``Pipelines Python`` for a typical python package that depends on `pipe_base`_)  to get an appropriate directory structure set up.
The bot uses the templates in the `lsst/templates`_ repository to define the package layout.

DM packaging of third party code should proceed as described in :doc:`packaging-third-party-eups-dependencies`.

If the new package needs a distinct Jira component (most will), any DMLT member (such as your manager) can add one.

Upon adding a new package, the dependency should be listed in the table file of packages that specifically utilize it. This method prevents the code from breaking for users who only setup specific packages they are utilizing and not the entire ``lsst_apps`` or ``lsst_distrib``. Even when changes are made on a branch, Jenkins builds of that branch will use the new table file and will proceed to pull the new package into the build. Dependencies managed through Conda, rather than EUPS, are assumed and should not be specified in the table file.

Should the need for clarification arise upon the successful addition of a new package and validation of its operational functionality, your firsthand experience would be invaluable in proposing enhancements to this documentation, thereby aiding future developers.

Adding a package to a distributed product
=========================================

RFC process
-----------

New packages intended for distribution to end users should generally be added as a dependency of a "top-level product:" these are the roots of the LSST package hierarchy.
They include ``lsst_apps``, ``lsst_distrib``, ``qserv_distrib`` and ``lsst_sims``.

Before adding a new dependency to one of these top-level distribution products, it must be approved through the :doc:`RFC process </communications/rfc>`.
Consensus must be reached regarding both the name and the suitability of the new package.
Before adopting the RFC, the following steps must be completed:

* Implementation tickets are created to cover package creation.
* The package is migrated to the `LSST organization on GitHub`_, if not already there.
* The package must have a descriptive README file at the root level, describing how it fits into the Science Pipelines infrastructure.
* An audit is done of any dependencies with a focus on identifying implied dependencies.

If the package in the RFC already exists, you must also complete these steps before the RFC can be adopted:

* Demonstrate that the package documentation can build and be linked from a branch of the `Science Pipelines docs`_ (see :ref:`package_and_pipeline_docs` for how to do this)`.

Packages that will not be distributed as part of a release do not require an RFC.

Repository access
-----------------

Access to the repository must be granted by a repository administrator to appropriate teams.
For DM-written code, these include "Data Management" and "Overlords."
For third-party code, either forked or packaged as "TaP" tarball-and-patch, use the "DM Externals" and "Overlords" (but *not* "Data Management") teams.
Note that the "DM Auxilliaries" [sic] team is used to mark packages that are *not* part of the release distribution; it is used to tag them alongside the release as well as to catch accidental inclusions.
The roles assigned to these teams should typically be "Write" for "Data Management", "Admin" for "Overlords", and "Read" for all others, but most permissions are handled at the organization level, so these could even be "Read" for all teams.

.. warning::

  Failing to assign a team will break the daily and weekly builds.
  The automated builds use the team membership to determine the type of tag to be applied.
  Having the code reside in the ``lsst`` or ``lsst-dm`` organization on GitHub is not sufficient.

repos.yaml
----------

The new package must be added to the `etc/repos.yaml file in the lsst/repos repository`_ along with its corresponding GitHub URL.
This file is governed by a "self-merge" policy: upon opening a pull request, it will be checked by GitHub Actions, and developers may merge without further review on success.
This change **must** be merged before the package can be built on Jenkins, and this should be done early in the RFC implementation process.
Refer to :jira:`RFC-75` for background.

.. _package_and_pipeline_docs:

Package and pipelines docs
--------------------------

Documentation for the new package must be built and linked from the main `Science Pipelines docs`_ page.
Before your package is included in the official builds, you need to follow these steps to make that documentation visible to reviewers.
This must be done as part of your RFC proposal (for pre-existing packages), or prior to marking the RFC implemented (for packages that did not exist prior to the RFC being filed):

1. Follow the instructions for :ref:`adding a package to pipelines.lsst.io <add-to-pipelines-lsst-io>` on a ticket branch.
2. :ref:`Build the Science PIpelines docs locally <local-pipelines-lsst-io-build>` on that branch.
3. Copy the ``_build/html`` directory from your pipelines build to a place that's publicly viewable (e.g. your public web path on :doc:`the USDF </usdf/storage>`).
4. Include a link to those built docs in your RFC.

.. note::

   The current Science Pipelines documentation build only builds against tagged versions of packages (e.g. daily or weekly tags) in a release with a Docker image build, like ``lsst_distrib``.
   You can work around this current limitation by building the documentation locally and publishing it with your USDF web hosting, as described above.

Top-level product dependency
----------------------------

The new package then needs to be added to the :file:`ups/*.table` file (and possibly the :file:`ups/*.cfg` file if this is a C++ package) of one or more other packages in the stack where it is used so that the build system can work out the correct dependency tree.
Table files should use ``setupRequired(package_name)`` or ``setupOptional(package_name)`` as necessary; test data packages are usually optional to allow releases to be made without requiring large additional data packages to be included.
Packages that use optional dependencies must be written to ensure that they can pass their unit tests when the package is not available.

.. _github-repository-configuration:

Configuring GitHub Repositories
===============================

.. Note::

  If you created your package via ``@sqrbot-jr`` on the LSST slack, the GitHub repo should be configured correctly.
  These instructions are for the rare cases that cannot be handled by ``@sqrbot-jr``.

All LSST DM repositories on GitHub must be configured by a repository administrator to protect the ``main`` branch and to ensure that the merge button for pull requests can not be pushed without the branch being up to date with ``main``.
There are a number of settings required to ensure this and they are described below with URLs referring to the ``afw`` package.
Replace ``afw`` with the relevant package name to get to the correct page on GitHub.

1. On the main settings page for the repository, https://github.com/lsst/afw/settings, disable squash and rebase merging, and enable automatic deletion of head branches after merging a pull request:

.. image:: /_static/build-ci/github_pull_requests_settings.png

.. note::

  If the Settings tab is not visible at the top of the repo page, an administrator likely needs to grant admin privileges first.

2. Configure the ``main`` branch to enable protections.
For ``afw`` this is located at https://github.com/lsst/afw/settings/branches/ and can also be found from the "Branches" sidebar item on the settings screen.
In the "Branch protection rules" section of that page you will have to click on "Add rule" to create a rule for ``main``.
First, add in ``main`` as the branch name pattern.
Second, enable ``Require a pull request before merging``, but disable ``Require approvals``.
Third, enable status checks, require that branches be up to date before merging, and add the ``call-workflow/lint`` and ``call-workflow/rebase-checker`` GitHub actions to the list of required status checks.
To enable the ``call-workflow/lint`` GitHub action, type ``lint`` into the search box and select the ``call-workflow/lint`` GitHub action and similarly for the other required action.
Finally, check the "Do not allow bypassing the above settings" box, since it's all too easy to make a mistake without realizing you have special override powers.
With checks enabled people will be able to use the GitHub merge button on Pull Requests and know that the :ref:`standard process <workflow-code-review-merge>` is being adhered to.

Once the above settings have been configured correctly, click ``Create`` to save the new rule.
The new rule settings should look something like this:

.. image:: /_static/build-ci/github_branch_protection_rule_settings.png

GitHub requires that at least one check runs before the up-to-date checks are enabled, so a GitHub Action **must** be provided if the GitHub merge button is to be used.
GitHub Actions do not replace normal testing done with a :doc:`Jenkins job <jenkins-stack-os-matrix>`.
For packages that contain Python, it is useful to add a simple GitHub Action by selecting "Actions" from the GitHub repository page, selecting "New Workflow" if necessary, and choosing the "LSST DM Python lint Workflow".
If Python typing is used, it can be checked using ``mypy`` via the "LSST DM Python mypy Workflow".
Similarly, YAML files can be checked via the "LSST DM YAML lint Workflow", and shell scripts can be checked via the "LSST DM shellcheck Workflow".
(All of these checks can be configured, either via an external file such as ``.yamllint.yaml``, or via modifications to the workflow as described in the link in the shellcheck workflow.)
If nothing seems appropriate, the "LSST DM null Workflow" should be enabled to allow GitHub to do the checks it needs.

Pull requests will automatically run GitHub Actions and their results will be visible in the "Checks" tab of the pull request on GitHub.

.. _lfs-repos:

Handling Git LFS-backed repos
=============================

New :doc:`Git LFS-backed </git/git-lfs>` repos (or existing repos being converted to LFS) require additional configuration.
``@sqrbot-jr`` cannot yet create an empty LFS-ready repo.

- The `repos.yaml`_ entry must declare that the repository is LFS backed:

  .. code-block:: yaml

      afwdata:
        url: https://github.com/lsst/afwdata.git
        lfs: true

  See the comment block at the top of `repos.yaml`_ for additional details.

- At present, the EUPS distrib packaging mechanism does not support LFS-backed repos.
  These products **must not** be added to any top-level meta-package or as a mandatory (non-``optional``) recursive dependency of a top-level package.

- *Optional* dependencies must be added to `manifest.remap`_ to prevent the creation of broken EUPS distrib packages.
  Please note that the "self-merge" policy (:jira:`RFC-75`) does not apply to `manifest.remap`_.

  Unlike changes merged into `repos.yaml`_, modifications to `manifest.remap`_ do not take immediate affect.

  We recommend that you attach the modification PR to a DM Jira issue on the ``Continuous Integration`` component.


.. warning::

   LFS-backed repositories must **always** be used as optional dependencies and must always be added to the `manifest.remap`_ file.
   This is required because of constraints imposed by the EUPS publication mechanism.

.. _LSST organization on GitHub: https://github.com/lsst
.. _lsst/templates: https://github.com/lsst/templates/tree/main/project_templates/stack_package
.. _Distributing third-party packages with EUPS: https://confluence.lsstcorp.org/display/LDMDG/Distributing+third-party+packages+with+EUPS
.. _etc/repos.yaml file in the lsst/repos repository: https://github.com/lsst/repos/blob/main/etc/repos.yaml
.. _repos.yaml: https://github.com/lsst/repos/blob/main/etc/repos.yaml
.. _manifest.remap:  https://github.com/lsst/lsstsw/blob/main/etc/manifest.remap
.. _pipe_base: https://github.com/lsst/pipe_base/
.. _Science Pipelines docs: https://pipelines.lsst.io/
