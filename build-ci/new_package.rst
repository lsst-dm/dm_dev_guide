#################################
Adding a new package to the build
#################################

"Top-level products" are the roots of the LSST package hierarchy. They include
``lsst_apps``, ``lsst_distrib``, ``qserv_distrib`` and ``lsst_sims``. Before
adding a new dependency to any top level product, it must be added to the
`LSST organization on GitHub`_ and access must be granted to the appropriate
teams. Both DM-written packages and third-party packages should go through the
RFC process first to confirm their name and the suitability of their contents.

DM-written Science Pipelines packages should follow the template in the
`lsst/templates`_ repository.

Third-party packages should be packaged as described in :doc:`third_party`.

The new package must be added to the `etc/repos.yaml file in the lsstsw
package`_ along with its corresponding GitHub URL. Note that this file is
governed by a "self-merge" policy; see `RFC-75`_ for details.  The new package
then needs to be added to the :file:`ups/*.table` file (and possibly the
:file:`ups/*.cfg` file) of one or more other packages in the stack where it is
used.

.. _LSST organization on GitHub: https://github.com/lsst
.. _lsst/templates: https://github.com/lsst/templates
.. _Distributing third-party packages with EUPS: https://confluence.lsstcorp.org/display/LDMDG/Distributing+third-party+packages+with+EUPS
.. _etc/repos.yaml file in the lsstsw package: https://github.com/lsst/lsstsw/blob/master/etc/repos.yaml
.. _RFC-75: https://jira.lsstcorp.org/browse/RFC-75
