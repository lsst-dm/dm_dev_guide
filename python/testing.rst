###################
Python Unit Testing
###################

.. note::

   Changes to this document must be approved by the System Architect (`RFC-24 <https://jira.lsstcorp.org/browse/RFC-24>`_).
   To request changes to these policies, please file an :doc:`RFC </communications/rfc>`.

This page provides technical guidance to developers writing unit tests for DM's Python code base.
See :doc:`/coding/unit-test-policy` for an overview of LSST Stack testing.
LSST tests must support being run using the `pytest`_ test runner and may use its features.
They can be, and traditionally have been, written using the `unittest` framework, with default test discovery.
The use of this framework is described below.
If you want to jump straight to a full example of the standard LSST Python testing boilerplate without reading the background, read the :ref:`section on memory testing <py-test-mem>` later in this document.

.. _SQR-012: http://sqr-012.lsst.io
.. _pytest: http://pytest.org

Introduction to ``unittest``
============================

This document will not attempt to explain full details of how to use `unittest` but instead shows common scenarios encountered in the LSST codebase.

A simple :mod:`unittest` example is shown below:

.. literalinclude:: examples/test_basic_example.py
   :linenos:
   :language: python

The important things to note in this example are:

* Python tests explicitly should not contain a shebang (``#!/usr/bin/env python``) and should not be executable (so cannot be run directly with ``./test_Example.py``).
  This avoids problems encountered running tests on macOS and helps ensure consistency in the way that tests are executed.
* Test file names must begin with ``test_`` to allow `pytest`_ to automatically detect them without requiring an explicit test list, which can be hard to maintain and can lead to missed tests.
* If the test is being executed using :command:`python` from the command line the `unittest.main` call performs the test discovery and executes the tests, setting exit status to non-zero if any of the tests fail.
* Test classes are executed in the order in which they appear in the test file.
  In this case the tests in ``DemoTestCase1`` will be executed before those in ``DemoTestCase2``.
* Test classes must, ultimately, inherit from `unittest.TestCase` in order to be discovered, and it is :ref:`recommended <py-utils-tests>` that `lsst.utils.tests.TestCase` be used as the base class when :lmod:`~lsst.afw` objects are involved.
  The tests themselves must be methods of the test class with names that begin with ``test``.
  All other methods and classes will be ignored by the test system but can be used by tests.
* Specific test asserts, such as `~unittest.TestCase.assertGreater`, `~unittest.TestCase.assertIsNone` or `~unittest.TestCase.assertIn`, should be used wherever possible.
  It is always better to use a specific assert because the error message will contain more useful detail and the intent is more obvious to someone reading the code.
  Only use `~unittest.TestCase.assertTrue` or `~unittest.TestCase.assertFalse` if you are checking a boolean value, or a complex statement that is unsupported by other asserts.
* When testing that an exception is raised always use `~unittest.TestCase.assertRaises` as a context manager, as shown in line 10 of the above example.
* If a test method completes, the test passes; if it throws an uncaught exception the test has failed.

We write test files to allow them to be run by `pytest`_ rather than simply :command:`python`, as the former provides more flexibility and enhanced reporting when running tests (such as specifying that only certain tests run).

Supporting Pytest
=================

.. note::
  `pytest`_ and its plugins are standard stack EUPS packages and do not have to be installed separately.

All LSST products that are built using :command:`scons` will execute Python tests using `pytest`_ so all tests should be written using it.
`pytest`_ provides a much richer execution and reporting environment for tests and can be used to run multiple test files together.

The `pytest`_ scheme for discovering tests inside Python modules is much more flexible than that provided by :mod:`unittest`.
In particular, care must be taken not to have free functions that use a ``test`` prefix or non-\ `~unittest.TestCase` test classes that are named with a ``Test`` prefix in the test files.

.. note::
  When :command:`pytest` is run by :command:`scons` full warnings are reported, including `DeprecationWarning`.
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

If there is pybind wrapper code in ``tests/`` that must be compiled for the python tests to run (for example, a test C++ library that must be loaded by the python tests), there must be a ``BasicSConscript.pybind11()`` entry *before* the ``BasicSConscript.tests()`` entry in the :file:`tests/SConscript`.
Having the ``pybind11`` come first ensures the necessary code will be compiled before any tests are loaded and run.

Running tests standalone
------------------------

``pySingles`` is an optional argument to the `~lsst.sconsUtils.scripts.BasicSConscript.tests` method that can be used for the rare cases where a test must be run standalone and not with other test files in a shared process.

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

When writing tests it is important that tests are skipped using the `pytest skipping framework`_ or the :mod:`unittest` :ref:`skipping framework <python:unittest-skipping>` rather than returning from the test early.
Both `pytest`_ and :mod:`unittest` support skipping of individual tests and entire classes using decorators or skip exceptions.
LSST code sometimes raises skip exceptions in `~unittest.TestCase.setUp` or `~unittest.TestCase.setUpClass` class methods.
It is also possible to indicate that a particular test is expected to fail, being reported as an error if the test unexpectedly passes.
Expected failures can be used to write test code that triggers a reported bug before the fix to the bug has been implemented and without causing the continuous integration system to die.
One of the primary advantages of using a modern test runner such as `pytest`_ is that it is very easy to generate machine-readable pass/fail/skip/xfail statistics to see how the system is evolving over time, and it is also easy to enable code coverage.
Jenkins now provides test result information.

.. _pytest skipping framework: https://docs.pytest.org/en/6.2.x/skipping.html

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
   flake8-ignore = E133 E226 E228 N802 N803 N806 N812 N813 N815 N816 W503

The ``addopts`` parameter adds additional command-line options to the :command:`pytest` command when it is run either from the command-line or from :command:`scons`.
A wrinkle with the configuration of the ``pytest-flake8`` plugin is that it inherits the ``max-line-length`` and ``exclude`` settings from the ``[flake8]`` section of :file:`setup.cfg` but you are required to explicitly list the codes to ignore when running within `pytest`_ by using the ``flake8-ignore`` parameter.
One advantage of this approach is that you can ignore error codes from specific files such that the unit tests will pass, but running :command:`flake8` from the command line will remind you there is an outstanding issue.
This feature should be used sparingly, but can be useful when you wish to enable code linting for the bulk of the project but have some issues preventing full compliance.
For example, at the time of writing this is an extract from the :file:`setup.cfg` file for the :lmod:`lsst.meas.base` package:

.. code-block:: ini

  [flake8]
  max-line-length = 110
  max-doc-length = 79
  ignore = E133, E226, E228, N802, N803, N806, N812, N813, N815, N816, W503
  exclude = __init__.py, tests/testLib.py

  [tool:pytest]
  addopts = --flake8
  flake8-ignore = E133 E226 E228 N802 N803 N806 N812 N813 N815 N816 W503
      # These will not be needed when we use numpydoc
      baseMeasurement.py E266
      forcedMeasurement.py E266

Here two files trigger an error because Doxygen syntax sometimes requires non-compliant comment code.

.. note::
  With this configuration each Python file tested by :command:`pytest` will have :command:`flake8` run on it.
  If :command:`scons` has not been configured to use :command:`pytest` in automatic test discovery mode, you will discover that :command:`flake8` is only being run on the test files themselves rather than all the Python files in the package.


Using a shared base class
=========================

For some tests it is helpful to provide a base class and then share it amongst multiple test classes that are configured with different attributes.
If this is required, be careful to not have helper functions prefixed with ``test``.
Do not have the base class named with a ``Test`` prefix and ensure it does not inherit from `~unittest.TestCase`; if you do, `pytest`_ will attempt to find tests inside it and will issue a warning if none can be found.
Historically LSST code has dealt with this by creating a test suite that only includes the classes to be tested, omitting the base class.
This does not work in a `pytest`_ environment.

Consider the following test code:

.. literalinclude:: examples/test_baseclass.py
   :language: python

which inherits from the helper class and `unittest.TestCase` and runs a single test without attempting to run any tests in ``BaseClass``.

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

`lsst.utils.tests`__ provides several helpful functions and classes for writing Python tests that developers should make use of.

.. __: https://pipelines.lsst.io/v/weekly/modules/lsst.utils/index.html#lsst-utils-tests-module

.. _py-utils-tests:

Special Asserts
---------------

Inheriting from `lsst.utils.tests.TestCase` rather than `unittest.TestCase` enables new asserts that are useful for doing element-wise comparison of two floating-point `numpy`-like arrays or scalars.

`lsst.utils.tests.TestCase.assertFloatsAlmostEqual`
   Asserts that floating point scalars and/or arrays are equal within the specified tolerance.
   The default tolerance is significantly tighter than the tolerance used by `unittest.TestCase.assertAlmostEqual` or `numpy.testing.assert_almost_equal`; if you are replacing either of those methods you may have to specify ``rtol`` and/or ``atol`` to prevent failing asserts.
`lsst.utils.tests.TestCase.assertFloatsEqual`
   Asserts that floating point scalars and/or arrays are identically equal.
`lsst.utils.tests.TestCase.assertFloatsNotEqual`
   Asserts that floating point scalars and/or arrays are not equal.

Additionally, :ref:`lsst.geom <pipelines:lsst.geom>`, :ref:`lsst.afw.geom <pipelines:lsst.afw.geom>`, and :ref:`lsst.afw.image <pipelines:lsst.afw.image>` provide additional asserts that get loaded into `lsst.utils.tests.TestCase` when the associated module is loaded.
These include methods for `Geom (SpherePoints, Angles, Pairs, Boxes)`_, and `Images`_, such as:

:lmeth:`~lsst.geom.testUtils.assertSpherePointsAlmostEqual`
   Assert that two sphere points (:lclass:`~lsst.geom.SpherePoint`) are nearly equal (provided by :lmod:`lsst.geom.testUtils`).
:lmeth:`~lsst.geom.testUtils.assertAnglesAlmostEqual`
   Assert that two angles (:lclass:`~lsst.geom.Angle`) are nearly equal, ignoring wrap differences by default (provided by :lmod:`lsst.geom.testUtils`).
:lmeth:`~lsst.geom.testUtils.assertPairsAlmostEqual`
   Assert that two planar pairs (e.g. :lclass:`~lsst.geom.Point2D` or :lclass:`~lsst.geom.Extent2D`) are nearly equal (provided by :lmod:`lsst.geom.testUtils`).
:lmeth:`~lsst.geom.testUtils.assertBoxesAlmostEqual`
   Assert that two boxes (:lclass:`~lsst.geom.Box2D` or :lclass:`~lsst.geom.Box2I`) are nearly equal (provided by :lmod:`lsst.geom.testUtils`).
:lmeth:`~lsst.afw.geom.utils.assertWcsAlmostEqualOverBBox`
   Compare :lmeth:`~lsst.afw.image.imageLib.Wcs.pixelToSky` and :lmeth:`~lsst.afw.image.imageLib.Wcs.skyToPixel` for two WCS over a rectangular grid of pixel positions (provided by :lmod:`lsst.afw.geom.utils`).
:lmeth:`~lsst.afw.image.testUtils.assertImagesAlmostEqual`
   Assert that two images are nearly equal, including non-finite values (provided by :lmod:`lsst.afw.image.testUtils`).
:lmeth:`~lsst.afw.image.testUtils.assertMasksEqual`
   Assert that two masks are equal (provided by :lmod:`lsst.afw.image.testUtils`).
:lmeth:`~lsst.afw.image.testUtils.assertMaskedImagesAlmostEqual`
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
The call to `~lsst.utils.tests.ExecutablesTestCase.create_executable_tests` initiates executable discovery and creates a test for each executable that is found.

In some cases an explicit test has to be written either because some precondition has to be met before the test will stand a chance of running or because some arguments have to be passed to the executable.
To support this the `~lsst.utils.tests.ExecutablesTestCase.assertExecutable` method is available:

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


File descriptor leak testing
----------------------------

.. _py-test-mem:

`lsst.utils.tests.MemoryTestCase` is used to detect leaks in file descriptors.
`~lsst.utils.tests.MemoryTestCase` should be used in *all* test files where :lmod:`~lsst.utils` is in the dependency chain.

This example shows the basic structure of an LSST Python unit test module,
including `~lsst.utils.tests.MemoryTestCase` (the highlighted lines indicate the leak testing modifications):

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


   =========================== 2 passed in 0.28 seconds ===========================

Note that `~lsst.utils.tests.MemoryTestCase` must always be the
final test suite.
For the file descriptor test to function properly the `lsst.utils.tests.init` function must be invoked before any of the tests in the class are executed.
Since LSST test scripts are required to run properly when called from within `pytest`_, the `~lsst.utils.tests.init` function has to be in the :ref:`setup_module <pytest:xunitsetup>` function that is called by `pytest`_ whenever a test module is loaded.
It is no longer required that this function also be present just before the call to `unittest.main` to handle being called with :command:`python`.
If you see strange failures in the file descriptor leak check when tests are run in parallel, make sure that `lsst.utils.tests.init` is being called properly.


Decorators for iteration
------------------------

It can be useful to parametrize a class or test function to execute with different combinations of variables.
`pytest`_ has `parametrizing decorators`_ to enable this.

.. _parametrizing decorators: https://docs.pytest.org/en/6.2.x/parametrize.html

In addition, we have custom decorators that have been used to provide similar functionality but should generally be avoided in new code.
``lsst.utils.tests.classParameters`` is a class decorator for generating classes with different combinations of class variables.
This is useful for when the ``setUp`` method generates the object being tested:
placing the decorator on the class allows generating that object with different values.
The decorator takes multiple lists of named parameters (which must have the same length) and iterates over the combinations.
For example:

.. code-block:: python

    @classParameters(foo=[1, 2], bar=[3, 4])
    class MyTestCase(unittest.TestCase):
        ...

will generate two classes, as if you wrote:

.. code-block:: python

    class MyTestCase_1_3(unittest.TestCase):
        foo = 1
        bar = 3
        ...

    class MyTestCase_2_4(unittest.TestCase):
        foo = 2
        bar = 4
        ...

Note that the values are embedded in the class name, which allows identification of the particular class in the event of a test failure.

``lsst.utils.tests.methodParameters`` is a method decorator for running a test method with different value combinations.
This is useful for when you want an individual test to iterate over multiple values.
As for ``classParameters``, the decorator takes multiple lists of named parameters (which must have the same length) and iterates over the combinations.
For example:

.. code-block:: python

    class MyTestCase(unittest.TestCase):
        @methodParameters(foo=[1, 2], bar=[3, 4])
        def testSomething(self, foo, bar):
            ...

will run tests:

.. code-block:: python

        testSomething(foo=1, bar=3)
        testSomething(foo=2, bar=4)

Note that the method being decorated must be within a subclass of ``unittest.TestCase``, since it relies on the existence of the ``subTest`` method for identifying the individual iterations.
This use of ``subTest`` also means that all iterations will be executed, not stopping at the first failure.

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

If you have legacy DM `unittest` ``suite``-based code (code that sets up a `unittest.TestSuite` object by listing specific test classes and that uses ``lsst.utils.tests.run`` rather than `unittest.main`), please refer to tech note `SQR-012`_ for porting instructions.


.. _`Coords`: http://doxygen.lsst.codes/stack/doxygen/x_masterDoxyDoc/x_masterDoxyDoc/namespacelsst_1_1afw_1_1coord_1_1utils.html
.. _`Geom (SpherePoints, Angles, Pairs, Boxes)`: http://doxygen.lsst.codes/stack/doxygen/x_masterDoxyDoc/namespacelsst_1_1afw_1_1geom_1_1utils.html
.. _`Images`: http://doxygen.lsst.codes/stack/doxygen/x_masterDoxyDoc/x_masterDoxyDoc/namespacelsst_1_1afw_1_1image_1_1test_utils.html
