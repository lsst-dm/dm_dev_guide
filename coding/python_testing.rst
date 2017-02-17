###################
Python Unit Testing
###################

.. note::

   Changes to this document must be approved by the System Architect (`RFC-24 <https://jira.lsstcorp.org/browse/RFC-24>`_).
   To request changes to these policies, please file an :ref:`RFC <decision-making-rfc>`.

This page provides technical guidance to developers writing unit tests for DM's Python code base.
See :doc:`unit_test_policy` for an overview of LSST Stack testing.
If you have legacy DM :mod:`unittest` ``suite``-based code (code that sets up a :class:`unittest.TestSuite` object by listing specific test classes and that uses :lfunc:`lsst.utils.tests.run` rather than :func:`unittest.main`), please refer to tech note `SQR-012`_ for porting instructions.
LSST tests should be written using the :mod:`unittest` framework, with default test discovery, and should support being run using the `pytest`_ test runner.
If you want to jump straight to a full example of the standard LSST Python testing boilerplate without reading the background, read the :ref:`section on memory testing <py-test-mem>` later in this document.

.. _SQR-012: http://sqr-012.lsst.io
.. _pytest: http://pytest.org

Introduction to ``unittest``
============================

This document will not attempt to explain full details of how to use :mod:`unittest` but instead shows common scenarios encountered in the LSST codebase.

A simple :mod:`unittest` example is shown below:

.. literalinclude:: unit_test_snippets/unittest_basic_example.py
   :linenos:
   :language: python

The important things to note in this example are:

* If the test is being executed using :command:`python` from the command line the :py:func:`unittest.main` call performs the test discovery and executes the tests, setting exit status to non-zero if any of the tests fail.
* Test classes are executed in the order in which they appear in the test file.
  In this case the tests in ``DemoTestCase1`` will be executed before those in ``DemoTestCase2``.
* Test classes must, ultimately, inherit from :class:`unittest.TestCase` in order to be discovered, and it is :ref:`recommended <py-utils-tests>` that :lclass:`lsst.utils.tests.TestCase` be used as the base class when :lmod:`~lsst.afw` objects are involved.
  The tests themselves must be methods of the test class with names that begin with ``test``.
  All other methods and classes will be ignored by the test system but can be used by tests.
* Specific test asserts, such as :meth:`~unittest.TestCase.assertGreater`, :meth:`~unittest.TestCase.assertIsNone` or :meth:`~unittest.TestCase.assertIn`, should be used wherever possible.
  It is always better to use a specific assert because the error message will contain more useful detail and the intent is more obvious to someone reading the code.
  Only use :meth:`~unittest.TestCase.assertTrue` or :meth:`~unittest.TestCase.assertFalse` if you are checking a boolean value, or a complex statement that is unsupported by other asserts.
* When testing that an exception is raised always use :meth:`~unittest.TestCase.assertRaises` as a context manager, as shown in line 10 of the above example.
* If a test method completes, the test passes; if it throws an uncaught exception the test has failed.

Using a more advanced test runner
=================================

.. note::
   `pytest`_ is not currently installed as part of a LSST stack installation.
   It can be installed using :command:`conda install pytest` or :command:`pip install pytest`.

All tests should be written such that they are runnable using `pytest`_, a policy adopted in :jira:`RFC-69`.
`pytest`_ provides a much richer execution and reporting environment for tests and can be used to run multiple tests files together.
`pytest`_ test discovery is much more flexible than that provided by :mod:`unittest`, but LSST test files should not take advantage of that flexibility as it can lead to inconsistency in test reports that depend on the specific test runner.
In particular, care must be taken not to have free functions that use a ``test`` prefix or non-\ :class:`~unittest.TestCase` test classes that are named with a ``Test`` prefix in the test files.

.. note::
   The normal way to run tests is to use :command:`scons` or :command:`scons tests`.
   :command:`scons` will then execute each of the tests and report any failures.
   Currently tests are executed one at a time using :command:`python` and checking the command exit status.
   Eventually :lmod:`~lsst.sconsUtils` will be modified to call :command:`py.test` directly with all Python test files (possibly with a different order each invocation).
   It is therefore important that during this transition period developers check that tests run correctly with `pytest`_ by explicitly running :command:`py.test` when creating or updating test files.

`pytest`_ can run tests from more than one file in a single invocation and this can be used to verify that there is no state contaminating later tests.
To run `pytest`_ use the :command:`py.test` executable:

.. code-block:: shell

   $ py.test tests/*.py

and to ensure that the order of test execution does not matter it is useful to sometimes run the tests in reverse order:

.. code-block:: shell

   $ py.test `ls -r tests/*.py`

When writing tests it is important that tests are skipped using the proper :mod:`unittest` :ref:`skipping framework <python:unittest-skipping>` rather than returning from the test early.
:mod:`unittest` supports skipping of individual tests and entire classes using decorators or skip exceptions.
LSST code sometimes raises skip exceptions in :meth:`~unittest.TestCase.setUp` or :meth:`~unittest.TestCase.setUpClass` class methods.
It is also possible to indicate that a particular test is expected to fail, being reported as an error if the test unexpectedly passes.
Expected failures can be used to write test code that triggers a reported bug before the fix to the bug has been implemented and without causing the continuous integration system to die.
One of the primary advantages of using a modern test runner such as `pytest`_ is that it is very easy to generate machine-readable pass/fail/skip/xfail statistics to see how the system is evolving over time.

Using a shared base class
=========================

For some tests it is helpful to provide a base class and then share it amongst multiple test classes that are configured with different attributes.
If this is required, be careful to not have helper functions prefixed with ``test``.
Do not have the base class named with a ``Test`` prefix and ensure it does not inherit from :class:`~unittest.TestCase`; if you do, `pytest`_ will attempt to find tests inside it and will issue a warning if none can be found.
Historically LSST code has dealt with this by creating a test suite that only includes the classes to be tested, omitting the base class.
This does not work in a `pytest`_ environment.

Consider the following test code:

.. literalinclude:: unit_test_snippets/unittest_baseclass.py
   :language: python

which inherits from the helper class and :class:`unittest.TestCase` and runs a single test without attempting to run any tests in ``BaseClass``.

.. code-block:: shell

   $ py.test -v coding/unit_test_snippets/unittest_baseclass.py
   ======================================= test session starts ========================================
   platform darwin -- Python 3.4.3, pytest-2.9.1, py-1.4.30, pluggy-0.3.1 -- /usr/local/bin/python3.4
   cachedir: coding/unit_test_snippets/.cache
   rootdir: coding/unit_test_snippets, inifile:
   collected 1 items

   coding/unit_test_snippets/unittest_baseclass.py::ThisIsTest1::testParam PASSED

   ===================================== 1 passed in 0.02 seconds =====================================


LSST Utility Test Support Classes
=================================

:lmod:`lsst.utils.tests` provides several helpful functions and classes for writing Python tests that developers should make use of.

.. _py-utils-tests:

Special Asserts
---------------

Inheriting from :lclass:`lsst.utils.tests.TestCase` rather than :class:`unittest.TestCase` enables new asserts that are useful for doing element-wise comparison of two floating-point :mod:`numpy`-like arrays or scalars.

`lsst.utils.tests.TestCase.assertFloatsAlmostEqual <https://lsst-web.ncsa.illinois.edu/doxygen/x_masterDoxyDoc/namespacelsst_1_1utils_1_1tests.html#a09ee2482a2e8d71e8612c0378f4286fc>`_
   Asserts that floating point scalars and/or arrays are equal within the specified tolerance.
   The default tolerance is significantly tighter than the tolerance used by :meth:`unittest.TestCase.assertAlmostEqual` or :func:`numpy.testing.assert_almost_equal`; if you are replacing either of those methods you may have to specify ``rtol`` and/or ``atol`` to prevent failing asserts.
`lsst.utils.tests.TestCase.assertFloatsEqual <https://lsst-web.ncsa.illinois.edu/doxygen/x_masterDoxyDoc/namespacelsst_1_1utils_1_1tests.html#a0e354bcea6ba8c11238882ede5058c03>`_
   Asserts that floating point scalars and/or arrays are identically equal.
`lsst.utils.tests.TestCase.assertFloatsNotEqual <https://lsst-web.ncsa.illinois.edu/doxygen/x_masterDoxyDoc/namespacelsst_1_1utils_1_1tests.html#a4fc68518d134e3656499898653a3bce3>`_
   Asserts that floating point scalars and/or arrays are not equal.

Note that :lmeth:`~lsst.utils.tests.TestCase.assertClose` and :lmeth:`~lsst.utils.tests.TestCase.assertNotClose` methods have been deprecated by the above methods.

Additionally, :lmod:`~lsst.afw` provides additional asserts that get loaded into :lclass:`lsst.utils.tests.TestCase` when the associated module is loaded.
These include methods for `Coords <https://lsst-web.ncsa.illinois.edu/doxygen/x_masterDoxyDoc/namespacelsst_1_1afw_1_1coord_1_1utils.html>`_, `Geom (Angles, Pairs, Boxes) <https://lsst-web.ncsa.illinois.edu/doxygen/x_masterDoxyDoc/namespacelsst_1_1afw_1_1geom_1_1utils.html>`_, and `Images <https://lsst-web.ncsa.illinois.edu/doxygen/x_masterDoxyDoc/namespacelsst_1_1afw_1_1image_1_1test_utils.html>`_, such as:

:lmeth:`~lsst.afw.coord.utils.assertCoordsNearlyEqual`
   Assert that two coords represent nearly the same point on the sky (provided by :lmod:`lsst.afw.coord.utils`).
:lmeth:`~lsst.afw.geom.utils.assertAnglesNearlyEqual`
   Assert that two angles are nearly equal, ignoring wrap differences by default (provided by :lmod:`lsst.afw.geom.utils`).
:lmeth:`~lsst.afw.geom.utils.assertPairsNearlyEqual`
   Assert that two planar pairs (e.g. :lclass:`~lsst.afw.geom.Point2D` or :lclass:`~lsst.afw.geom.Extent2D`) are nearly equal (provided by :lmod:`lsst.afw.geom.utils`).
:lmeth:`~lsst.afw.geom.utils.assertBoxesNearlyEqual`
   Assert that two boxes (:lclass:`~lsst.afw.geom.Box2D` or :lclass:`~lsst.afw.geom.Box2I`) are nearly equal (provided by :lmod:`lsst.afw.geom.utils`).
:lmeth:`~lsst.afw.image.basicUtils.assertWcsNearlyEqualOverBBox`
   Compare :lmeth:`~lsst.afw.image.imageLib.Wcs.pixelToSky` and :lmeth:`~lsst.afw.image.imageLib.Wcs.skyToPixel` for two WCS over a rectangular grid of pixel positions (provided by :lmod:`lsst.afw.image.basicUtils`).
:lmeth:`~lsst.afw.image.testUtils.assertImagesNearlyEqual`
   Assert that two images are nearly equal, including non-finite values (provided by :lmod:`lsst.afw.image.testUtils`).
:lmeth:`~lsst.afw.image.testUtils.assertMasksEqual`
   Assert that two masks are equal (provided by :lmod:`lsst.afw.image.testUtils`).
:lmeth:`~lsst.afw.image.testUtils.assertMaskedImagesNearlyEqual`
   Assert that two masked images are nearly equal, including non-finite values (provided by :lmod:`lsst.afw.image.testUtils`).

Testing Executables
-------------------

In some cases the test to be executed is a shell script or a compiled binary executable.
In order for the test running environment to be aware of these tests, a Python test file must be present that can be run by `pytest`_.
If none of the tests require special arguments and all the files with the executable bit set are to be run, this can be achieved by copying the file :file:`$UTILS_DIR/tests/testExecutables.py` to the relevant :file:`tests` directory.
The file is reproduced here:

.. literalinclude:: unit_test_snippets/testExecutables.py
   :linenos:
   :language: python
   :emphasize-lines: 8-9

The ``EXECUTABLES`` variable can be a tuple containing the names of the executables to be run (relative to the directory containing the test file).
``None`` indicates that the test script should discover the executables in the same directory as that containing the test file.
The call to :lmeth:`~lsst.utils.tests.ExecutablesTestCase.create_executable_tests` initiates executable discovery and creates a test for each executable that is found.

In some cases an explicit test has to be written either because some precondition has to be met before the test will stand a chance of running or because some arguments have to be passed to the executable.
To support this the :lmeth:`~lsst.utils.tests.ExecutableTestCase.assertExecutable` method is available:

.. code-block:: python

   def testBinary(self):
       self.assertExecutable("binary1", args=None,
                             root_dir=os.path.dirname(__file__))

where ``binary1`` is the name of the executable relative to the root directory specified in the ``root_dir`` optional argument.
Arguments can be provided to the ``args`` keyword parameter in the form of a sequence of arguments in a list or tuple.

.. note::
   The LSST codebase is currently in transition such that :lmod:`~lsst.sconsUtils` will run executables
   itself as well as running Python test scripts that run executables.
   Do not worry about this duplication of test running.
   When the codebase has migrated to consistently use the testing scheme described in this section :lmod:`~lsst.sconsUtils` will be modified to disable the duplicate testing.


Memory and file descriptor leak testing
---------------------------------------

.. _py-test-mem:

:lclass:`lsst.utils.tests.MemoryTestCase` is used to detect memory leaks in C++ objects and leaks in file descriptors.
:lclass:`~lsst.utils.tests.MemoryTestCase` should be used in *all* test files where :lmod:`~lsst.utils` is in the dependency chain, even if C++ code is not explicitly referenced.

This example shows the basic structure of an LSST Python unit test module,
including :lclass:`~lsst.utils.tests.MemoryTestCase` (the highlighted lines indicate the memory testing modifications):

.. literalinclude:: unit_test_snippets/unittest_runner_example.py
   :linenos:
   :language: python
   :emphasize-lines: 12, 17, 21


which ends up running the single specified test plus the two running as part of the leak test:

.. code-block:: shell

   $ py.test -v unittest_runner_example.py
   ============================= test session starts ==============================
   platform darwin -- Python 2.7.11, pytest-2.8.5, py-1.4.31, pluggy-0.3.1 -- ~/lsstsw/miniconda/bin/python
   cachedir: .cache
   rootdir: .../coding/unit_test_snippets, inifile:
   collected 3 items

   unittest_runner_example.py::DemoTestCase::testDemo PASSED
   unittest_runner_example.py::MemoryTester::testFileDescriptorLeaks <- .../lsstsw/stack/DarwinX86/utils/12.0.rc1+f79d1f7db4/python/lsst/utils/tests.py PASSED
   unittest_runner_example.py::MemoryTester::testLeaks <- .../lsstsw/stack/DarwinX86/utils/12.0.rc1+f79d1f7db4/python/lsst/utils/tests.py PASSED

   =========================== 3 passed in 0.28 seconds ===========================

Note that :lclass:`~lsst.utils.tests.MemoryTestCase` must always be the
final test suite.
For the memory test to function properly the :lfunc:`lsst.utils.tests.init()` function must be invoked before any of the tests in the class are executed.
Since LSST test scripts are required to run properly from the command-line and when called from within `pytest`_, the :lfunc:`~lsst.utils.tests.init()` function has to be in the file twice: once in the :ref:`setup_module <pytest:xunitsetup>` function that is called by `pytest`_ whenever a test module is loaded (`pytest`_ will not use the ``__main__`` code path), and also just before the call to :func:`unittest.main()` call to handle being called with :command:`python`.

Unicode
=======

It is now commonplace for Unicode to be used in Python code and the LSST test cases should reflect this situation.
In particular file paths, externally supplied strings and strings originating from third party software packages may well include code points outside of US-ASCII.
LSST tests should ensure that these cases are handled by explicitly including strings that include code points outside of this range.
For example,

* file paths should be generated that include spaces as well as international characters,
* accented characters should be included for name strings, and
* unit strings should include the µm if appropriate.
