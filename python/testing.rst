###################
Python Unit Testing
###################

.. note::

   Changes to this document must be approved by the System Architect (`RFC-24 <https://jira.lsstcorp.org/browse/RFC-24>`_).
   To request changes to these policies, please file an :doc:`RFC </communications/rfc>`.

This page provides technical guidance to developers writing unit tests for DM's Python code base.
See :doc:`/coding/unit-test-policy` for an overview of LSST Stack testing.
LSST tests should be written using the :mod:`unittest` framework, with default test discovery, and should support being run using the `pytest`_ test runner as well as from the command line.
If you want to jump straight to a full example of the standard LSST Python testing boilerplate without reading the background, read the :ref:`section on memory testing <py-test-mem>` later in this document.

.. _SQR-012: http://sqr-012.lsst.io
.. _pytest: http://pytest.org

Introduction to ``unittest``
============================

This document will not attempt to explain full details of how to use :mod:`unittest` but instead shows common scenarios encountered in the LSST codebase.

A simple :mod:`unittest` example is shown below:

.. literalinclude:: examples/test_basic_example.py
   :linenos:
   :language: python

The important things to note in this example are:

* Test file names must begin with ``test_`` to allow `pytest`_ to automatically detect them without requiring an explicit test list, which can be hard to maintain and can lead to missed tests.
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

Supporting Pytest
=================

.. note::
  `pytest`_ and its plugins are standard stack EUPS packages and do not have to be installed separately.

All LSST products that are built using :command:`scons` will execute Python tests using `pytest`_ so all tests should be written using it.
`pytest`_ provides a much richer execution and reporting environment for tests and can be used to run multiple test files together.

The `pytest`_ scheme for discovering tests inside Python modules is much more flexible than that provided by :mod:`unittest`, but LSST test files should not take advantage of that flexibility as it can lead to inconsistency in test reports that depend on the specific test runner, and it is required that an individual test file can be executed by running it directly with :command:`python`.
In particular, care must be taken not to have free functions that use a ``test`` prefix or non-\ :class:`~unittest.TestCase` test classes that are named with a ``Test`` prefix in the test files.

.. note::
  When :command:`pytest` is run by :command:`scons` full warnings are reported, including :py:class:`DeprecationWarning`.
  Previously these warnings were hidden in the test output but now they are more obvious, allowing you to fix any problems early.

The tests/SConscript file
-------------------------

The behavior of `pytest`_ when invoked by :command:`scons` is controlled by the :file:`tests/SConscript` file.
At minimum this file should contain the following to enable testing with automated test discovery:

.. code-block:: python

   from lsst.sconsUtils import scripts
   scripts.BasicSConscript.tests(pyList=[])

``pyList`` is used to specify which Python test files to run.
Here the empty list is interpreted as "allow :command:`pytest` to automatically discover tests"
:command:`pytest` will scan the directory tree itself to find tests and will run them all together using the number of subprocesses matching the ``-j`` argument given to :command:`scons`.
For this mode to work, all test files must be named :file:`test_*.py`.

If ``pyList=None`` (the historical default) is used, the :command:`scons` ``tests`` target will be used to locate test files using a glob for ``*.py`` in the :file:`tests` directory.
This list will then be passed explicitly to the :command:`pytest` command, bypassing its automatic test discovery.

Automatic test discovery is preferred as this ensures that there is no difference between running the tests with :command:`scons` and running them with :command:`pytest` without arguments, and it enables the possibility of adjusting :command:`pytest` test discovery to add additional testing of all Python files in the package.

Running tests standalone
------------------------

``pySingles`` is an optional argument to the :lmeth:`~lsst.sconsUtils.scripts.BasicSConscript.tests` method that can be used for the rare cases where a test must be run standalone and not with other test files in a shared process.

.. code-block:: python

   scripts.BasicSConscript.tests(pyList=[], pySingles=["testSingle.py"])

The tests are still run using :command:`pytest` but executed one at a time without using any multi-process execution.
Use of this should be extremely rare.
In the :lmod:`~lsst.base` package one test file is used to confirm that the LSST import code is working; this can only be tested if we know that it hasn't previously been imported as part of another test.
The other reason, so far, to run a test standalone is for test classes that dynamically generate large amounts of test data during the set up phase.
Until it is possible to pin test classes to a particular process with ``pytest-xdist``, tests such as these interact badly when test methods within the class are allocated to different subprocesses since each subprocess will generate the test files.
This can use significantly more disk and CPU when the test runs, and can even cause Jenkins to fail.
It is important to ensure that any files listed in ``pySingles`` should be named such that they will not be discovered by `pytest`_.
The convention is to name these files :file:`test*.py` without the underscore.

Where does the output go?
-------------------------

When :command:`scons` runs any tests, the output from those tests is written to the :file:`tests/.tests` directory, and a file is created for each test that is executed.
For the usual case where :command:`pytest` is running on multiple test files at once, there is a single file created, :file:`pytest-*.out`, in that directory, along with an XML file containing the test output in JUnit format.
If a test command fails, that output is renamed to have a :file:`.failed` extension and is reported by :command:`scons`.

For convenience the output from the main :command:`pytest` run (as opposed to the rare standalone usages) is also written to standard output so it is visible in the log or in the shell along with other :command:`scons` output.

Common Issues
=============

This section describes some common problems that are encountered when using `pytest`_.

Testing global state
--------------------

`pytest`_ can run tests from more than one file in a single invocation and this can be used to verify that there is no state contaminating later tests.
To run `pytest`_ use the :command:`pytest` executable:

.. code-block:: shell

   $ pytest

to run all files in the ``tests`` directory named ``test_*.py``. To ensure that the order of test execution does not matter it is useful to sometimes run the tests in reverse order by listing the test files manually:

.. code-block:: shell

   $ pytest `ls -r tests/test_*.py`

.. note::

  `pytest`_ plugins are usually all enabled by default.
  In particular, if you install the, otherwise excellent, ``pytest-random-order`` plugin to randomize your tests, this will most likely break your builds as it interacts badly with ``pytest-xdist`` used by :command:`scons` when ``-j`` is used.
  You can install it temporarily for investigative purposes so long as it is uninstalled afterwards.

Test Skipping and Expected Failures
-----------------------------------

When writing tests it is important that tests are skipped using the proper :mod:`unittest` :ref:`skipping framework <python:unittest-skipping>` rather than returning from the test early.
:mod:`unittest` supports skipping of individual tests and entire classes using decorators or skip exceptions.
LSST code sometimes raises skip exceptions in :meth:`~unittest.TestCase.setUp` or :meth:`~unittest.TestCase.setUpClass` class methods.
It is also possible to indicate that a particular test is expected to fail, being reported as an error if the test unexpectedly passes.
Expected failures can be used to write test code that triggers a reported bug before the fix to the bug has been implemented and without causing the continuous integration system to die.
One of the primary advantages of using a modern test runner such as `pytest`_ is that it is very easy to generate machine-readable pass/fail/skip/xfail statistics to see how the system is evolving over time, and it is also easy to enable code coverage.
Jenkins now provides test result information.

.. _testing-flake8:

Enabling additional Pytest options: flake8
==========================================

As described in :ref:`style-guide-py-flake8`, Python modules can be configured using the :file:`setup.cfg` file.
This configuration is supported by `pytest`_ and can be used to enable additional testing or tuning on a per-package basis.
`pytest`_ uses the ``[tool:pytest]`` block in the configuration file.
To enable automatic :command:`flake8` testing as part of the normal test execution the following can be added to the :file:`setup.cfg` file:

.. code-block:: ini

   [tool:pytest]
   addopts = --flake8
   flake8-ignore = E133 E226 E228 N802 N803 N806 N812 N813 N815 N816 W504

The ``addopts`` parameter adds additional command-line options to the :command:`pytest` command when it is run either from the command-line or from :command:`scons`.
A wrinkle with the configuration of the ``pytest-flake8`` plugin is that it inherits the ``max-line-length`` and ``exclude`` settings from the ``[flake8]`` section of :file:`setup.cfg` but you are required to explicitly list the codes to ignore when running within `pytest`_ by using the ``flake8-ignore`` parameter.
One advantage of this approach is that you can ignore error codes from specific files such that the unit tests will pass, but running :command:`flake8` from the command line will remind you there is an outstanding issue.
This feature should be used sparingly, but can be useful when you wish to enable code linting for the bulk of the project but have some issues preventing full compliance.
For example, at the time of writing this is an extract from the :file:`setup.cfg` file for the :lmod:`lsst.meas.base` package:

.. code-block:: ini

  [flake8]
  max-line-length = 110
  ignore = E133, E226, E228, N802, N803, N806, N812, N813, N815, N816, W504
  exclude = __init__.py, tests/testLib.py

  [tool:pytest]
  addopts = --flake8
  flake8-ignore = E133 E226 E228 N802 N803 N806 N812 N813 N815 N816 W504
      # This will go away for newer flake8 versions
      forcedPhotCoadd.py W503
      # These will not be needed when we use numpydoc
      baseMeasurement.py E266
      forcedMeasurement.py E266

Here one file is triggering a ``W503`` warning erroneously because of a bug in the version of :command:`flake8` currently included in the stack, and two files trigger an error because Doxygen syntax sometimes requires non-compliant comment code.

.. note::
  With this configuration each Python file tested by :command:`pytest` will have :command:`flake8` run on it.
  If :command:`scons` has not been configured to use :command:`pytest` in automatic test discovery mode, you will discover that :command:`flake8` is only being run on the test files themselves rather than all the Python files in the package.


Using a shared base class
=========================

For some tests it is helpful to provide a base class and then share it amongst multiple test classes that are configured with different attributes.
If this is required, be careful to not have helper functions prefixed with ``test``.
Do not have the base class named with a ``Test`` prefix and ensure it does not inherit from :class:`~unittest.TestCase`; if you do, `pytest`_ will attempt to find tests inside it and will issue a warning if none can be found.
Historically LSST code has dealt with this by creating a test suite that only includes the classes to be tested, omitting the base class.
This does not work in a `pytest`_ environment.

Consider the following test code:

.. literalinclude:: examples/test_baseclass.py
   :language: python

which inherits from the helper class and :class:`unittest.TestCase` and runs a single test without attempting to run any tests in ``BaseClass``.

.. code-block:: text

   $ pytest -v python/examples/test_baseclass.py
   ======================================= test session starts ========================================
   platform darwin -- Python 3.4.3, pytest-3.2.1, py-1.4.30, pluggy-0.3.1 -- /usr/local/bin/python3.4
   cachedir: python/examples/.cache
   rootdir: python/examples, inifile:
   collected 1 items

   python/examples/test_baseclass.py::ThisIsTest1::testParam PASSED

   ===================================== 1 passed in 0.02 seconds =====================================


LSST Utility Test Support Classes
=================================

:lmod:`lsst.utils.tests` provides several helpful functions and classes for writing Python tests that developers should make use of.

.. _py-utils-tests:

Special Asserts
---------------

Inheriting from :lclass:`lsst.utils.tests.TestCase` rather than :class:`unittest.TestCase` enables new asserts that are useful for doing element-wise comparison of two floating-point :mod:`numpy`-like arrays or scalars.

`lsst.utils.tests.TestCase.assertFloatsAlmostEqual`_
   Asserts that floating point scalars and/or arrays are equal within the specified tolerance.
   The default tolerance is significantly tighter than the tolerance used by :meth:`unittest.TestCase.assertAlmostEqual` or :func:`numpy.testing.assert_almost_equal`; if you are replacing either of those methods you may have to specify ``rtol`` and/or ``atol`` to prevent failing asserts.
`lsst.utils.tests.TestCase.assertFloatsEqual`_
   Asserts that floating point scalars and/or arrays are identically equal.
`lsst.utils.tests.TestCase.assertFloatsNotEqual`_
   Asserts that floating point scalars and/or arrays are not equal.

Note that :lmeth:`~lsst.utils.tests.TestCase.assertClose` and :lmeth:`~lsst.utils.tests.TestCase.assertNotClose` methods have been deprecated by the above methods.

Additionally, :lmod:`~lsst.afw` provides additional asserts that get loaded into :lclass:`lsst.utils.tests.TestCase` when the associated module is loaded.
These include methods for `Coords`_, `Geom (Angles, Pairs, Boxes)`_, and `Images`_, such as:

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
If none of the tests require special arguments and all the files with the executable bit set are to be run, this can be achieved by copying the file :file:`$UTILS_DIR/tests/test_executables.py` to the relevant :file:`tests` directory.
The file is reproduced here:

.. literalinclude:: examples/test_executables.py
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

.. literalinclude:: examples/test_runner_example.py
   :linenos:
   :language: python
   :emphasize-lines: 12, 17, 21


which ends up running the single specified test plus the two running as part of the leak test:

.. code-block:: shell

   $ pytest -v test_runner_example.py
   ============================= test session starts ==============================
   platform darwin -- Python 3.6.2, pytest-3.2.1, py-1.4.31, pluggy-0.3.1 -- ~/lsstsw/miniconda/bin/python
   cachedir: .cache
   rootdir: .../python/examples, inifile:
   collected 3 items

   test_runner_example.py::DemoTestCase::testDemo PASSED
   test_runner_example.py::MemoryTester::testFileDescriptorLeaks <- .../lsstsw/stack/DarwinX86/utils/12.0.rc1+f79d1f7db4/python/lsst/utils/tests.py PASSED
   test_runner_example.py::MemoryTester::testLeaks <- .../lsstsw/stack/DarwinX86/utils/12.0.rc1+f79d1f7db4/python/lsst/utils/tests.py PASSED

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

Legacy Test Code
================

If you have legacy DM :mod:`unittest` ``suite``-based code (code that sets up a :class:`unittest.TestSuite` object by listing specific test classes and that uses :lfunc:`lsst.utils.tests.run` rather than :func:`unittest.main`), please refer to tech note `SQR-012`_ for porting instructions.


.. _`lsst.utils.tests.TestCase.assertFloatsAlmostEqual`: http://doxygen.lsst.codes/stack/doxygen/x_masterDoxyDoc/namespacelsst_1_1utils_1_1tests.html#a09ee2482a2e8d71e8612c0378f4286fc
.. _`lsst.utils.tests.TestCase.assertFloatsEqual`: http://doxygen.lsst.codes/stack/doxygen/x_masterDoxyDoc/namespacelsst_1_1utils_1_1tests.html#a0e354bcea6ba8c11238882ede5058c03
.. _`lsst.utils.tests.TestCase.assertFloatsNotEqual`: http://doxygen.lsst.codes/stack/doxygen/x_masterDoxyDoc/x_masterDoxyDoc/namespacelsst_1_1utils_1_1tests.html#a4fc68518d134e3656499898653a3bce3
.. _`Coords`: http://doxygen.lsst.codes/stack/doxygen/x_masterDoxyDoc/x_masterDoxyDoc/namespacelsst_1_1afw_1_1coord_1_1utils.html
.. _`Geom (Angles, Pairs, Boxes)`: http://doxygen.lsst.codes/stack/doxygen/x_masterDoxyDoc/namespacelsst_1_1afw_1_1geom_1_1utils.html
.. _`Images`: http://doxygen.lsst.codes/stack/doxygen/x_masterDoxyDoc/x_masterDoxyDoc/namespacelsst_1_1afw_1_1image_1_1test_utils.html
