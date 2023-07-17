######################
Deprecating Interfaces
######################

Deprecation Procedure
=====================

Deprecations are changes to interfaces.
(If they were limited to implementation alone, they wouldn't require deprecation, as no one would notice when the change was made.)
They require approval from the DMCCB by means of an :doc:`RFC </communications/rfc>`.

All internal usage of deprecated interfaces MUST be removed at the point the deprecation is made, not later when the deprecated interfaces are removed; this includes all packages in ``lsst_distrib`` as well as standard CI packages like ``ci_hsc``, ``ci_imsim``, and ``ci_cpp``.
No DM pipeline or test output should ever include deprecation warnings emitted by our own code.
See :ref:`finding-downstream-usage` for how to ensure this.

Release notes
-------------

When a feature, class, or function is deprecated, a description of the deprecation is included in the release notes for the next official release (major or minor or bugfix).
It may be desirable to repeat that description in succeeding release notes until the code is removed.

.. _code_removal:

Code removal
------------

When an interface is deprecated, a ticket should be filed to remove the corresponding deprecated code, usually assigned to the team of the deprecating developer.
Removal of the deprecated code occurs, at the earliest, immediately after the next major release, which will be the first one to include the deprecation in its release notes, or after eight weeks (whichever is longer).
Removal should occur before the major release after the one in which it is first deprecated.
For the purposes of removal, the "release" event is when the first release candidate is tagged, because this is when the release branch may start to diverge from the ``main`` branch.
In other words, if a deprecation is merged to the ``main`` branch between the first release candidate tags for v17 and v18, it may only be removed after the first release candidate tag for v18 (and also only after eight weeks have passed), and should be removed before the first release candidate tag for v19.
The code removal ticket should be blocked by the next major release (v18 in this example), and block the following one (v19).
Scheduling of the code removal should be handled like :doc:`any other backlog story </work/project-planning>`, although with a clear deadline (and a clear "do not merge before" point, unlike most stories).
In particular, the removal could be assigned to a different developer than the one doing the original deprecation, as negotiated by the relevant T/CAM.

This ensures that users of major releases will first see deprecation warnings at the same time the deprecation appears in the release notes, and will then have until the next major release to update their code accordingly.
Users of weekly releases will see only the deprecation warnings and will have eight weeks to update.

Backporting deprecations
------------------------

Deprecations may be backported to release branches, with :doc:`backport requests made and approved </work/backports>` like any other ticket.
After a major release is out, backporting deprecations to a release branch is discouraged and will be permitted only in special circumstances.
Backporting new alternative interfaces without backporting deprecations is preferred when possible.

In all cases, interfaces whose deprecations have been backported onto a release branch are treated the same way as deprecations merged to ``main`` before the first release candidate in terms of when the code should be removed (i.e. after the next major release).
The eight-week counter for removing deprecated code starts when the deprecation is merged to ``main`` and is unaffected by backports.

Continuous integration tests
----------------------------

CI tests are run with deprecation warnings enabled, which should be the default for our warning category and pytest executor.
Triggering such a warning does not cause a test failure.

Python Deprecation
==================

If you need to deprecate a class or function, import the `~deprecated.sphinx.deprecated` decorator::

   from deprecated.sphinx import deprecated

For each class or function to be deprecated, decorate it as follows::

   @deprecated(reason="This method is no longer used for ISR. Will be removed after v14.",
               version="v14.0", category=FutureWarning)
   def _extractAmpId(self, dataId):

Class and static methods should be decorated in the order given here::

    class Foo:
        @classmethod
        @deprecated(reason="This has been replaced with `mm()`. Will be removed after v9.",
	            version="v9.0", category=FutureWarning)
        def cm(cls, x):
            pass

        @staticmethod
        @deprecated(reason="This has been replaced with `mm()`. Will be removed after v9.",
	            version="v9.0", category=FutureWarning)
        def sm(x):
            pass

The reason string should include the replacement API when available or explain why there is no replacement.
The reason string will be automatically added to the docstring for the class or function; there is no need to change that.
The reason string must also specify the version after which the method may be removed, as discussed in :ref:`code_removal`.

The version argument to the decorator specifies the next release, when the deprecation will be in effect but the interface has not yet been removed.
It is not required that developers inserting deprecation decorators know exactly what the next release will be; they may use the next major release in the version argument, even if it is later than the actual first deprecation notice.

Since our end users tend to be developers or at least may call APIs directly from notebooks, we will treat our APIs as end-user features and use ``category=FutureWarning`` instead of the default `DeprecationWarning`, which is primarily for Python developers.
Do not use `PendingDeprecationWarning`.

pybind11 Deprecation
====================

A deprecated pybind11-wrapped function, method or class must be rewrapped in pure Python using the `lsst.utils.deprecate_pybind11` function, which defaults to ``category=FutureWarning``::

   from lsst.utils.deprecated import deprecate_pybind11
   ExposureF.getCalib = deprecate_pybind11(
       ExposureF.getCalib,
       reason="Replaced by getPhotoCalib. Will be removed after v17."
       version="v17.0")

If only one overload of a set is being deprecated, state that in the reason string.
Over-warning is considered better than under-warning in this case.
The reason string must also specify the version after which the function may be removed, as discussed in :ref:`code_removal`.
The version argument specifies the upcoming release, at which time the deprecation will be in effect.


.. note::
	The message printed for deprecated classes will refer to the constructor function but this is how we deprecated the entire class.

C++ Deprecation
===============

Use the C++14 deprecation attribute syntax to deprecate a function, variable, or type::

   class [[deprecated("Replaced by PixelAreaBoundedField. Will be removed after v19.")]]
        PixelScaleBoundedField : public BoundedField {

It should appear on its own line, adjacent to the declaration of the function, variable, or type it applies to.
The reason string should include the replacement API when available or explain why there is no replacement.
The reason string must also specify the version after which the object may be removed, as discussed in :ref:`code_removal`.

When a deprecated C++ interface is used by code that we cannot yet remove (e.g. an also-deprecated pybind11 wrapper for it), we do not want to emit compiler warnings due to the original deprecation.
This can be achieved via preprocessor directives::

    #pragma GCC diagnostic push
    #pragma GCC diagnostic ignored "-Wdeprecated"
    call_deprecated_function();
    #pragma GCC diagnostic pop

Note that this works for ``clang`` as well as ``gcc``, despite the pragma name.

Config Deprecation
==================

To deprecate a `~lsst.pex.config.Field` in a `~lsst.pex.config.Config`, set the ``deprecated`` field in the field's definition::

    someOption = pexConfig.Field(
            dtype=float,
            doc="This is an configurable field that does something important.",
            deprecated="This field is no longer used. Will be removed after v18."
        )


Setting this parameter will append a deprecation message to the `~lsst.pex.config.Field` docstring, and will cause the system to emit a `FutureWarning` when the field is set by a user (for example, in an obs-package override or by a commandline option).
The deprecated string must also specify the version after which the config may be removed, as discussed in :ref:`code_removal`.

.. _package-deprecation:

Package Deprecation
===================

To deprecate an entire package, first have its top-level :file:`__init__.py` (e.g. :file:`python/lsst/example/package/__init__.py`; create it if necessary) issue an appropriate `FutureWarning` when it is imported::

    import warnings

    warnings.warn('lsst.example.package is deprecated; it will be removed from the Rubin Observatory '
                  'Science Pipelines after release 21.0.0', category=FutureWarning)

Add a similar warning to the :file:`index.rst` file documenting this package (e.g. :file:`doc/lsst.example.package/index.rst)`::

    .. py:currentmodule:: lsst.example.package

    .. _lsst.example.package:

    ####################
    lsst.example.package
    ####################

    ``lsst.example.package`` is an example package.

    .. warning:: This package is deprecated, and will be removed from the Rubin Observatory Science Pipelines after release 21.0.0.

Finally, add a note to the top-level :file:`README` file in the package::

    *Warning:* This package is deprecated, and will be removed from the Rubin Observatory Science Pipelines distribution after release 21.0.0.


Package Removal
===============

After deprecating a package as described :ref:`above <package-deprecation>`, there are four steps that need to take place to actually remove the package.

1. Remove the package from all eups table files that contain it.
   This effectively removes the package for all future builds.
   The following steps can then occur whenever reasonable.
2. Rename the package, prefixing the string ``legacy-``, using the "Rename" button at the top of the repository settings page.
   GitHub will redirect references to the old name to the new one.
   The primary reason for this step is to avoid confusing the repo with an active one.
3. Move the package to the ``lsst-dm`` GitHub organization using the "Transfer ownership" button at the bottom of the repository settings page.
   GitHub redirects should still occur.
   This step helps keep the ``lsst`` organization clean, containing only distributed code.
4. Edit the URL in the ``etc/repos.yaml`` file in the ``lsst/repos`` repository to correspond to the new location of the package's GitHub repository.
   This step is to make it easy to find the relocated repository, particularly for historical builds.
   Because of the redirects, this step does not have to occur immediately, but it is simple enough to do right away given the self-merge policy on the ``lsst/repos`` repository.

.. _finding-downstream-usage:

Finding Downstream Usage
========================

For all Python deprecations (including pybind11 and config deprecations), developers should find and fix downstream usage of a deprecated interface by turning the new warnings into errors temporarily, and running Jenkins (or running lsstsw locally).
The easiest approach is to pass ``action="error"`` to the ``@deprecated`` decorator when it is used, or to replace a `warnings.warn` with a ``raise`` statement, on a temporary commit.
Unfortunately this action takes precedence over any warnings filter added later, so code that intentionally calls the deprecated code while silencing the warning (i.e. because it is also a deprecated code path) will also fail.

.. note::

    It is tempting to use the ``PYTHONWARNINGS`` environment variable or the Python interpreter's ``-W`` option to turn warnings into errors instead, since these can be overridden by in-code warnings filters.
    Writing a filter that matches just the desired deprecations is at least difficult, however, and in our testing it seems that matching on ``module`` is surprisingly unreliable and hard-to-debug.
    Since a filter that does not match will cause emitted warnings to be missed in testing, we do not recommend this approach.

Developers may also actually remove deprecated interfaces on temporary ``git`` commits and run Jenkins; this may be more effective for more complicated deprecations, and it can provide a starting point for the removal ticket branch in advance.
This is the recommended approach for all pure C++ deprecations.
