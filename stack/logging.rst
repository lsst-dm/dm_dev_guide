#######
Logging
#######

This page provides guidance to developers for using logging in the Science Pipelines code base.
In general, all logging in Python code should be done with the standard :mod:`logging` package.
All logging from C++ code should be done using the :lmod:`lsst.log` package; reference documentation on that logging framework can be found at the `Doxygen page on logging`_.
Application code that uses both Python and C++ logging should include configuration code to forward C++ log messages to the Python :mod:`logging` system.
This is handled automatically when using, for example, the `pipetask`_ command.
For an example of configuring the logging framework in pipeline tasks, see the `pipelines.lsst.io page on logging`_.

Developers are encouraged to insert log messages whenever and wherever they might be useful, with appropriate component names and levels.

Whether using :mod:`logging` or any other logging mechanism, timestamps recorded in logs should use Internet `RFC 3339`_ format, which is sortable and includes the timezone.  See the discussion in :jira:`DM-1203` for history.

.. _Doxygen page on logging: http://doxygen.lsst.codes/stack/doxygen/x_mainDoxyDoc/log.html
.. _pipelines.lsst.io page on logging: https://pipelines.lsst.io/modules/lsst.pipe.base/command-line-task-logging-howto.html
.. _RFC 3339: http://tools.ietf.org/html/rfc3339
.. _pipetask: https://pipelines.lsst.io/modules/lsst.ctrl.mpexec/pipetask.html

.. _logger-names:

Logger Names
============

Logger names should generally start with the fully qualified name of the module/file containing the logger, with the leading ``lsst.``.
Some example logger names are ``lsst.afw.image.MaskedImage`` and ``lsst.meas.algorithms.starSelector``.
A common Python recommendation is to create the logger name from the module hierarchy automatically:

.. code-block:: python

   log = logging.getLogger(__name__)

If the logger is saved as a variable in a class, it is often appropriate to name the logger after the class.
Such a logger can be derived from the module logger using ``log.getChild()``.

Logger names use ``.`` as component separators, not ``::``, even in C++.

Basic Usage in Python
=====================

The simplest way to log is:

.. code-block:: python

   import logging
   logging.info('Some information during normal operation')
   logging.warning('Here is a warning!')

The example logs to the default (root) logger.
By default Python logs warning messages and no other log messages.
This means that the above example code will only write a single log message.
Application code is required to configure the logging state for libraries and this is generally done by calling :func:`logging.basicConfig` to set a default logger level and default log format.
For example, to enable ``INFO`` level output reporting the name of the logger and log message level as well as the message use the following:

.. code-block:: python

   logging.basicConfig(level=logging.INFO, format="{name} {levelname}: {message}", style="{")

Our execution environment and butler commands configure this automatically.

A better naming practice is to use a named logger following our :ref:`name convention <logger-names>` to indicate where the logging messages originate.
For example:

.. code-block:: python

   logger = logging.getLogger("lsst.meas.algorithms.starSelector")
   logger.info("This is information about the star selector algorithm execution. %f", 3.14)

The standard methods, such as :meth:`~logging.Logger.info` and :meth:`~logging.Logger.warning`, use a ``%``-format string in the message and pass in additional arguments containing variable information, which :class:`logging.Logger` will internally merge into the message string with ``%`` formatting if the log record is to be printed.
This deferred string interpolation can be very important if the variable being inserted into the log message is a complex class and converting it to a string is an expensive operation.
For example, do not write:

.. code-block:: python

   log.debug(f"Some message: {myvar}")

since that would do the f-string interpolation even if the logger is only configured to show warning messages.
Instead this code should be written as:

.. code-block:: python

   log.debug("Some message: %s", myvar)

To specify the threshold or the lowest-severity log messages a logger handles, :meth:`~logging.Logger.setLevel` can be used:

.. code-block:: python

   logger.setLevel(logging.DEBUG)

Basic Usage in C++
==================

To use :lmod:`lsst.log` in C++, the header file to include is:

.. code-block:: c++

   #include "lsst/log/Log.h"

Typically one of the logging macros should be used.
You can choose either sprintf style formatting (the ``LOGL_`` family) or iostream style formatting (the ``LOGLS_`` family) to log to a logger.
The following shows an example to get a logger object and log using it:

.. code-block:: c++

   LOG_LOGGER _log = LOG_GET("lsst.afw.image.ExposureInfo");
   LOGLS_INFO(_log, "Empty WCS extension, using FITS header");
   LOGLS_WARN(_log, "Missing empty chunks info for " << "something");
   LOGL_DEBUG(_log, "St. Dev = %g", sd);


The full list of available macros and more details of the :lmod:`lsst.log` features are described in its `package documentation <http://doxygen.lsst.codes/stack/doxygen/x_mainDoxyDoc/x_mainDoxyDoc/log.html>`_.

Getting a logger object and logging to that is preferred over logging using a string as the logger name, but the latter can also be used.
For example:

.. code-block:: c++

   LOGL_WARN("meas.algorithms.starSelector.psfCandidate", "Failed to make a psfCandidate")

.. _logger-levels:

Log Levels
==========

:mod:`logging` has five standard levels; in increasing order of severity the are: ``DEBUG`` < ``INFO`` < ``WARNING`` < ``ERROR`` < ``CRITICAL``.
The guideline of using the log levels is as follows:

- CRITICAL: for severe errors that may prevent further execution of the component (FATAL is also allowed as an alias).
- ERROR: for errors that may still allow the execution to continue.
- WARNING: for conditions that may indicate a problem but that allow continued execution (WARN is also allowed as an alias).
- INFO: for information that is of interest during normal execution including production.
- DEBUG: for information that is of interest to developers but not of interest during production.

In addition there are two additional log levels allowed for specialist pipelines-specific loggers (such as those used for :lclass:`lsst.pipe.base.Task`):

- VERBOSE: for messages of a more detailed nature than would normally be expected to be shown by default but that will not swamp the user in the way that DEBUG messages would if that level of output was enabled.
  The `numeric log level`_ for VERBOSE logs is 15.

- TRACE: for detailed information when debugging, particularly inside loops.
  The TRACE `numeric log level`_ spans a range from 1-5 (e.g. for use with the ``log-cli-level`` argument to ``pytest``).

An alternative approach for TRACE and VERBOSE is to consider using DEBUG messages with a separate logger name that can be enabled when desired, :ref:`as described below <logger-trace-verbosity>`.
Remember though that the default output level for general users is usually INFO and for large-scale pipeline processing it is VERBOSE.
This means that VERBOSE logging will be available by default when analyzing log output for big processing runs in a way that would not happen if specially named loggers were used which had to be explicitly enabled by the person submitting the job.

For loggers used at DEBUG and TRACE levels, it is often desirable to add further components to the logger name; these would indicate which specific portion of the code or algorithm that the logged information pertains to.
For example:

.. code-block:: python

   debugLogger = logging.getLogger(__name__).getChild("catalogReader")
   debugLogger.debug("Catalog reading took %f seconds", finish - start)
   debugLogger.debug("Took %f seconds and found %d sources", elapsed, nstars)

The idea here is that the author understands the intent of the log message and can simply name it, without worrying about its relative importance or priority compared with other log messages in the same component.
A person debugging the code would typically be looking at it and so would be able to determine the appropriate name to enable.
The hierarchy allows all components to be easily enabled or disabled together.

.. _`numeric log level`: <https://docs.python.org/3/library/logging.html#levels>

Logging within the Task framework
=================================

Pipeline tasks (subclasses of :lclass:`lsst.pipe.base.Task` or :lclass:`lsst.pipe.base.CmdLineTask`) should use the :lattr:`lsst.pipe.base.Task.log` attribute logger:

.. code-block:: python

   self.log.verbose("Coadding %d exposures", len(calExpRefList))
   self.log.info("Not applying color terms because %s", applyCTReason)
   self.log.warn("Failed to make a psfCandidate from star %d: %s", star.getId(), err)

When running ``pipetask`` or similar commands, the ``--log-level`` command line argument can be used to set the threshold for specific components.
For example, to make the ``calibrate`` stage of ``processCcd`` less verbose:

.. code-block:: bash

     pipetask --log-level processCcd.calibrate=WARN run [pipeline options]

.. _logger-trace-verbosity:

Fine-level Verbosity in Tracing
===============================

As an alternative for TRACE loggers where there are different messages at increasing levels of verbosity but no specific component names that would be appropriate, or where increasing verbosity spans a number of levels of the component hierarchy, logger names can be prefixed with "TRACEn", where n=0-5, to indicate increasing verbosity.
For example, in C++:

.. code-block:: c++

   LOG_LOGGER traceLogger = LOG_GET("TRACE2.lsst.meas.algorithms.starSelector");
   LOGL_DEBUG(traceLogger, "On %d-th iteration of star selection", iteration);
   LOG_LOGGER innerTraceLogger = LOG_GET("TRACE2.lsst.meas.algorithms.starSelector.catalogReader");
   LOGL_DEBUG(innerTraceLogger, "Reading catalog %s", catalogName);
   // Or log to a component directly
   LOGL_DEBUG("TRACE4.lsst.meas.algorithms.starSelector.psfCandidate", "Making a psfCandidate from star %d", starId)

and in Python:

.. code-block:: python

   traceLogger = logging.getLogger("TRACE2.lsst.meas.algorithms.starSelector")
   traceLogger.debug("On %d-th iteration of star selection", iteration)
   innerTraceLogger = traceLogger.getChild("catalogReader")
   innerTraceLogger.debug("Reading catalog %s", catalogName)
   logging.getLogger("TRACE4.meas.algorithms.starSelector.psfCandidate").log(logging.DEBUG, "Making a psfCandidate from star %d", starId)

Notice that all loggers in the hierarchy under a given component at a given trace level can be enabled easily using, e.g., ``TRACE2.lsst.meas.algorithms.starSelector``.
Besides, a utility function :lfunc:`lsst.utils.logging.trace_set_at` is provided to adjust logging level of a group of loggers so to display messages with trace number <= NUMBER. This is demonstrated in the following example:


.. literalinclude:: examples/tracing.py
   :language: python

The example can be run if :lmod:`lsst.log` is setup:

.. code-block:: shell

   $ python examples/tracing.py
   INFO  root: Setting trace at 0
   INFO  root: Writing 6 debug messages
   DEBUG TRACE0.example.component: Fine tracing to TRACE0
   INFO  root: Setting trace at 1
   INFO  root: Writing 6 debug messages
   DEBUG TRACE0.example.component: Fine tracing to TRACE0
   DEBUG TRACE1.example.component: Fine tracing to TRACE1
   INFO  root: Setting trace at 2
   INFO  root: Writing 6 debug messages
   DEBUG TRACE0.example.component: Fine tracing to TRACE0
   DEBUG TRACE1.example.component: Fine tracing to TRACE1
   DEBUG TRACE2.example.component: Fine tracing to TRACE2
   INFO  root: Setting trace at 3
   INFO  root: Writing 6 debug messages
   DEBUG TRACE0.example.component: Fine tracing to TRACE0
   DEBUG TRACE1.example.component: Fine tracing to TRACE1
   DEBUG TRACE2.example.component: Fine tracing to TRACE2
   DEBUG TRACE3.example.component: Fine tracing to TRACE3
   INFO  root: Setting trace at 4
   INFO  root: Writing 6 debug messages
   DEBUG TRACE0.example.component: Fine tracing to TRACE0
   DEBUG TRACE1.example.component: Fine tracing to TRACE1
   DEBUG TRACE2.example.component: Fine tracing to TRACE2
   DEBUG TRACE3.example.component: Fine tracing to TRACE3
   DEBUG TRACE4.example.component: Fine tracing to TRACE4
   INFO  root: Setting trace at 5
   INFO  root: Writing 6 debug messages
   DEBUG TRACE0.example.component: Fine tracing to TRACE0
   DEBUG TRACE1.example.component: Fine tracing to TRACE1
   DEBUG TRACE2.example.component: Fine tracing to TRACE2
   DEBUG TRACE3.example.component: Fine tracing to TRACE3
   DEBUG TRACE4.example.component: Fine tracing to TRACE4
   DEBUG TRACE5.example.component: Fine tracing to TRACE5
