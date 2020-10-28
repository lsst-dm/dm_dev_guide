######################
Deprecating Interfaces
######################

Deprecation Procedure
=====================

Deprecations are changes to interfaces.
(If they were limited to implementation alone, they wouldn't require deprecation, as no one would notice when the change was made.)
They require approval from the DMCCB by means of an :doc:`RFC </communications/rfc>`.

Release notes
-------------

When a feature, class, or function is deprecated, a description of the deprecation is included in the release notes for the next official release (major or minor or bugfix).
It may be desirable to repeat that description in succeeding release notes until the code is removed.

.. _code_removal:

Code removal
------------

When an interface is deprecated, a ticket should be filed to remove the corresponding deprecated code, usually assigned to the team of the deprecating developer.
Removal of the deprecated code occurs, at the earliest, immediately after the next major release following the release with the first deprecation release note; at the latest, immediately before the major release following.
In other words, if deprecation is first noted in release 17.2.3, the code cannot be removed until after 18.0 is released and must be removed before 19.0 is released.
So the code removal ticket should block the following major release (19.0 in this example).
In general, no deprecation should be removed before two calendar months have elapsed.
Scheduling of the code removal should be handled like :doc:`any other backlog story </work/project-planning>`, although with a clear deadline (and a clear "do not merge before" point, unlike most stories).
In particular, the removal could be assigned to a different developer than the one doing the original deprecation, as negotiated by the relevant T/CAM.

Continuous integration tests
----------------------------

CI tests are run with deprecation warnings enabled, which should be the default for our warning category and pytest executor.
Triggering such a warning does not cause a test failure.

Python Deprecation
==================

If you need to deprecate a class or function, import the `~deprecated.sphinx.deprecated` decorator::

   from deprecated.sphinx import deprecated

For each class or function to be deprecated, decorate it as follows::

   @deprecated(reason="This method is no longer used for ISR. Will be removed after v15.", category=FutureWarning)
   def _extractAmpId(self, dataId):

Class and static methods should be decorated in the order given here::

    class Foo:
        @classmethod
        @deprecated(reason="This has been replaced with `mm()`. Will be removed after v10.",
	            version="v9.0", category=FutureWarning)
        def cm(cls, x):
            pass

        @staticmethod
        @deprecated(reason="This has been replaced with `mm()`. Will be removed after v10.",
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
       reason="Replaced by getPhotoCalib. Will be removed after v18."
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

Package Deprecation
===================

To deprecate an entire package, first have its top-level :file:`__init__.py` (e.g. :file:`python/lsst/example/package/__init__.py`; create it if necessary) issue an appropriate `FutureWarning` when it is imported::

    import warnings

    warnings.warn('lsst.example.package is deprecated; it will be removed from the Rubin Observatory'
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
