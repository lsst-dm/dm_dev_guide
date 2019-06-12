######################
Deprecating Interfaces
######################

Deprecation Procedure
=====================

Deprecations are changes to interfaces.
(If they were limited to implementation alone, they wouldn't require deprecation, as no one would notice when the change was made.)
As a result they often require or result from :doc:`RFCs </communications/rfc>`.
But our usual policy applies; if no one would object, a deprecation can be made without an RFC.

Release notes
-------------

When a feature, class, or function is deprecated, a description of the deprecation is included in the release notes for the next official release (major or minor or bugfix).
It may be desirable to repeat that description in succeeding release notes until the code is removed.

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

If you need to deprecate a class or function, import the :py:func:`~deprecated.sphinx.deprecated` decorator::

   from deprecated.sphinx import deprecated

For each class or function to be deprecated, decorate it as follows::

   @deprecated(reason="why", category=FutureWarning)

Class and static methods should be decorated in the order given here::

    class Foo:
        @classmethod
        @deprecated(reason="why", category=FutureWarning)
        def cm(cls, x):
            pass

        @staticmethod
        @deprecated(reason="why", category=FutureWarning)
        def sm(x):
            pass

The reason string should include the replacement API when available or explain why there is no replacement.
The reason string will be automatically added to the docstring for the class or function; there is no need to change that.
You do not need to specify the optional version argument to the decorator since deprecation decorators are typically not added in advance of when the deprecation actually begins.
Since our end users tend to be developers or at least may call APIs directly from notebooks, we will treat our APIs as end-user features and use ``category=FutureWarning`` instead of the default :py:class:`DeprecationWarning`, which is primarily for Python developers. Do not use :py:class:`PendingDeprecationWarning`.

pybind11 Deprecation
====================

A deprecated pybind11-wrapped function must be rewrapped in pure Python using the :py:func:`lsst.utils.deprecate_pybind11` function, which defaults to ``category=FutureWarning``::

   from lsst.utils.deprecated import deprecate_pybind11
   ExposureF.getCalib = deprecate_pybind11(ExposureF.getCalib,
           reason="Replaced by getPhotoCalib. (Will be removed in 18.0)")
 
If only one overload of a set is being deprecated, state that in the reason string.
Over-warning is considered better than under-warning in this case.

C++ Deprecation
===============

Use the C++14 deprecation attribute syntax to deprecate a function, variable, or type::

   [[deprecated("why")]]

It should appear on its own line, adjacent to the declaration of the function, variable, or type it applies to.
The reason string should include the replacement API when available or explain why there is no replacement.
