###################
Python Unit Testing
###################

This page provides technical guidance to developers writing unit tests for DM's Python code base.
See :doc:`unit_test_policy` for an overview of LSST Stack testing.

Memory Leak Testing
===================

:lmod:`lsst.utils.tests` provides several utilities for writing Python tests
that developers should make use of. In particular,
:lclass:`lsst.utils.tests.MemoryTestCase` is used to detect memory leaks in
C++ objects. :lclass:`~lsst.utils.tests.MemoryTestCase` should be used in
*all* tests, even if C++ code is not explicitly referenced.

This example shows the basic structure of an LSST Python unit test module,
including :lclass:`~lsst.utils.tests.MemoryTestCase`:

.. literalinclude:: unit_test_snippets/unittest_runner_example.py
   :language: python
   :emphasize-lines: 16

Note that :lclass:`~lsst.utils.tests.MemoryTestCase` must always be the
final test suite.

Unicode
=======

It is now commonplace for Unicode to be used in Python code and the LSST test cases should reflect this situation.
In particular file paths, externally supplied strings and strings originating from third party software packages may well include code points outside of US-ASCII.
LSST tests should ensure that these cases are handled by explicitly including strings that include code points outside of this range.
For example,

* file paths should be generated that include spaces as well as international characters,
* accented characters should be included for name strings, and
* unit strings should include the µm if appropriate.
