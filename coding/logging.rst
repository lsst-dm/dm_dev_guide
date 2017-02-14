#######
Logging
#######

This page provides guidance to developers for using logging with :lmod:`lsst.log`  in the Science Pipelines code base.
For reference documentation on the logging framework refer to the `Doxygen page on logging`_.

Developers are encouraged to insert log messages whenever and wherever they might be useful, with appropriate component names and levels.

Whether using :lmod:`lsst.log` or any other logging mechanism, timestamps recorded in logs should use Internet `RFC 3339`_ format, which is sortable and includes the timezone.  See the discussion in `DM-1203`_ for history.

.. _Doxygen page on logging: https://lsst-web.ncsa.illinois.edu/doxygen/x_masterDoxyDoc/log.html
.. _RFC 3339: http://tools.ietf.org/html/rfc3339
.. _DM-1203: https://jira.lsstcorp.org/browse/DM-1203

.. _logger-names:

Logger Names
============

Logger names should generally start with the fully qualified name of the module/file containing the logger, without the leading ``lsst.``.
Some example logger names are ``afw.image.MaskedImage`` and ``meas.algorithms.starSelector``.

If the logger is saved as a variable in a class, it is often appropriate to name the logger after the class.

Logger names use ``.`` as component separators, not ``::``, even in C++.

Basic Usage in Python
=====================

The basic Python interface of :lmod:`lsst.log` is made to be somewhat similar to Python logging.
The simplest way to log is:

.. code-block:: python

   import lsst.log
   lsst.log.info('Some information during normal operation')
   lsst.log.warn('Here is a warning!')

The example logs to the default (root) logger.

A better practice is to use a named logger following our :ref:`name convention <logger-names>` to indicate where the logging messages originate.
For example:

.. code-block:: python

   logger = lsst.log.Log.getLogger("meas.algorithms.starSelector")
   logger.info("This is information about the star selector algorithm execution. %f", 3.14)
   logger.infof("This is information about the star selector algorithm execution. {}", 3.14)

In Python, two string formatting options can be used for log messages.
The standard methods, such as :lmod:`~lsst.log.info` and :lmod:`~lsst.log.warn`, use a ``%``-format string in the message and pass in additional arguments containing variable information, which :lmod:`lsst.log` will internally merge into the message string with ``%`` formatting if the log record is to be printed.
Another set of methods with a trailing ``f``, for example :lmod:`~lsst.log.infof` and :lmod:`~lsst.log.warnf`, can use :meth:`~str.format` string interpolation using curly braces.

To specify the threshold or the lowest-severity log messages a logger handles, :lmeth:`setLevel` can be used:

.. code-block:: python

   logger.setLevel(lsst.log.DEBUG)

Basic Usage in C++
==================

To use :lmod:`lsst.log` in C++, the header file to include is:

.. code-block:: c++

   #include "lsst/log/Log.h"

Typically one of the logging macros should be used.
You can choose either sprintf style formatting (the ``LOGL_`` family) or iostream style formatting (the ``LOGLS_`` family) to log to a logger.
The following shows an example to get a logger object and log using it:

.. code-block:: c++

   LOG_LOGGER _log = LOG_GET("afw.image.ExposureInfo");
   LOGLS_INFO(_log, "Empty WCS extension, using FITS header");
   LOGLS_WARN(_log, "Missing empty chunks info for " << "something");
   LOGL_DEBUG(_log, "St. Dev = %g", sd);


The full list of available macros and more details of the :lmod:`lsst.log` features are described in its `package documentation <https://lsst-web.ncsa.illinois.edu/doxygen/x_masterDoxyDoc/log.html>`_.

Getting a logger object and logging to that is preferred over logging using a string as the logger name, but the latter can also be used.
For example:

.. code-block:: c++

   LOGL_WARN("meas.algorithms.starSelector.psfCandidate", "Failed to make a psfCandidate")

Log Levels
==========

:lmod:`lsst.log` has six levels; in increasing order of severity the are: ``TRACE`` < ``DEBUG`` < ``INFO`` < ``WARN`` < ``ERROR`` < ``FATAL``.
The guideline of using the log levels is as follows:

- FATAL: for severe errors that may prevent further execution of the component.
- ERROR: for errors that may still allow the execution to continue.
- WARN: for conditions that may indicate a problem but that allow continued execution.
- INFO: for information that is of interest during normal execution including production.
- DEBUG: for information that is of interest to developers but not of interest during production.
- TRACE: for detailed information when debugging.

For loggers used at DEBUG and TRACE levels, it is often desirable to add further components to the logger name; these would indicate which specific portion of the code or algorithm that the logged information pertains to.
For example:

.. code-block:: python

   debugLogger = lsst.log.Log.getLogger("meas.algorithms.starSelector.catalogReader")
   debugLogger.debug("Catalog reading took %f seconds", finish - start)
   debugLogger.debugf("Took {} seconds and found {count} sources", elapsed, count=nstars)

The idea here is that the author understands the intent of the log message and can simply name it, without worrying about its relative importance or priority compared with other log messages in the same component.
A person debugging the code would typically be looking at it and so would be able to determine the appropriate name to enable.
The hierarchy allows all components to be easily enabled or disabled together.

Logging within the Task framework
=================================

Pipeline tasks (subclasses of :lclass:`lsst.pipe.base.Task` or :lclass:`lsst.pipe.base.CmdLineTask`) should use the :lattr:`lsst.pipe.base.Task.log` attribute logger:

.. code-block:: python

   self.log.debugf("Coadding {} exposures", len(calExpRefList))
   self.log.info("Not applying color terms because %s", applyCTReason)
   self.log.warn("Failed to make a psfCandidate from star %d: %s", star.getId(), err)

When running command line tasks, the ``--loglevel`` command line argument can be used to set the threshold for specific components.

Fine-level Verbosity in Tracing
===============================

As an alternative for TRACE loggers where there are different messages at increasing levels of verbosity but no specific component names that would be appropriate, or where increasing verbosity spans a number of levels of the component hierarchy, logger names can be prefixed with "TRACEn", where n=0-5, to indicate increasing verbosity.
For example, in C++:

.. code-block:: c++

   LOG_LOGGER traceLogger = LOG_GET("TRACE2.meas.algorithms.starSelector");
   LOGL_DEBUG(traceLogger, "On %d-th iteration of star selection", iteration);
   LOG_LOGGER innerTraceLogger = LOG_GET("TRACE2.meas.algorithms.starSelector.catalogReader");
   LOGL_DEBUG(innerTraceLogger, "Reading catalog %s", catalogName);
   // Or log to a component directly
   LOGL_DEBUG("TRACE4.meas.algorithms.starSelector.psfCandidate", "Making a psfCandidate from star %d", starId)

and in Python:

.. code-block:: python

   traceLogger = lsst.log.Log.getLogger("TRACE2.meas.algorithms.starSelector")
   traceLogger.debug("On %d-th iteration of star selection", iteration)
   innerTraceLogger = lsst.log.getLogger("TRACE2.meas.algorithms.starSelector.catalogReader")
   innerTraceLogger.debugf("Reading catalog {}", catalogName)
   # Or log to a component directly
   lsst.log.log("TRACE4.meas.algorithms.starSelector.psfCandidate", lsst.log.DEBUG, "Making a psfCandidate from star %d", starId)

Notice that all loggers in the hierarchy under a given component at a given trace level can be enabled easily using, e.g., ``TRACE2.lsst.meas.algorithms.starSelector``.
Besides, a utility function :lfunc:`lsst.log.utils.traceSetAt()` is provided to adjust logging level of a group of loggers so to display messages with trace number <= NUMBER. This is demostrated in the following example:

.. literalinclude:: logging_snippets/tracing.py
   :language: python

The example can be run if :lmod:`lsst.log` is setup:

.. code-block:: shell

   $ python logging_snippets/tracing.py
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

Porting from pex_logging
========================

Logging in the Science Pipelines codes is being migrated from using :lmod:`lsst.pex.logging` to :lmod:`lsst.log`.
Below, some examples are listed that may be used as a starting point for porting:

.. table:: Examples for porting pex_logging to log

   +-------------------------------------+------------------------------------+
   | lsst.pex.logging                    | lsst.log                           |
   +=====================================+====================================+
   | lsst.pex.logging.getDefaultLog()    | lsst.log.Log.getDefaultLogger()    |
   +-------------------------------------+------------------------------------+
   | lsst.pex.logging.Debug(component)   | lsst.log.Log.getLogger(component)  |
   +-------------------------------------+------------------------------------+
   | Log(Log.getDefaultLog(), component) | Log.getLogger(component)           |
   +-------------------------------------+------------------------------------+
   | Trace_setVerbosity(component, num)  | lsst.log.setLevel(component, level)|
   +-------------------------------------+------------------------------------+
   | logger.setThresholdFor()            | lsst.log.setLevel(component, level)|
   +-------------------------------------+------------------------------------+
   | logger.setThreshold()               | logger.setLevel()                  |
   +-------------------------------------+------------------------------------+
   | logger.getThreshold()               | logger.getLevel()                  |
   +-------------------------------------+------------------------------------+
   | logger.logdebug()                   | logger.debug() or logger.trace()   |
   +-------------------------------------+------------------------------------+
   | #include "lsst/pex/logging.h"       | #include "lsst/log/Log.h"          |
   +-------------------------------------+------------------------------------+
   | #include "lsst/pex/logging/Trace.h" | #include "lsst/log/Log.h"          |
   +-------------------------------------+------------------------------------+
   | pex::logging::Log logger()          | LOG_LOGGER logger = LOG_GET()      |
   +-------------------------------------+------------------------------------+
   | pex::logging::Trace::setVerbosity() | LOG_SET_LVL("component", LOG_LVL_X)|
   +-------------------------------------+------------------------------------+

Other common cleanups during the transition:

- Explicit package dependency should be listed in the ups files (.table and .cfg).
- Remove unused header inclusion or imports.
- Use named logger when possible. The nameless default logger was used often and should be replaced if appropriate.
- The old usage ``log.log(log.WARN, "message")`` should be changed to ``log.warn("message")``.
