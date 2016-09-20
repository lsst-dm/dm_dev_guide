#######
Logging
#######

This page provides guidance to developers for using logging with :lmod:`lsst.log`  in the science pipeline code base. 

Logger Names
============
Logger names should generally start with the fully qualified name of the module/file containing the logger, without the leading ``lsst.``.
If the logger is saved as a variable in a class, it is often appropriate to name the logger after the class.
Logger names use ``.`` as component separators, not ``::``, even in C++.

Examples

.. code-block:: python

   log = lsst.log.Log.getLogger("meas.algorithms.starSelector")
   log.info("This is information about the star selector algorithm execution. %f", 3.14)

In Python, comma-separated arguments are preferred over the string formatting so it is done only if the log record is to be printed.

Log Levels
==========
Log levels should be used as follows:

- FATAL: for severe errors that may prevent further execution of the component
- ERROR: for errors that may still allow the execution to continue
- WARNING: for conditions that may indicate a problem but that allow continued execution
- INFO: for information that is of interest during normal execution including production
- DEBUG: for information that is of interest to developers but not of interest during production
- TRACE: for detailed information when debugging

For loggers used at DEBUG and TRACE levels, it is often desirable to add further components to the logger name; these would indicate which specific portion of the code or algorithm that the logged information pertains to.

.. code-block:: python

   debugLogger = lsst.log.Log.getLogger("meas.algorithms.starSelector.catalogReader")
   debugLogger.debug("Catalog reading took %f seconds", finish - start)

The idea here is that the author understands the intent of the log message and can simply name it, without worrying about its relative importance or priority compared with other log messages in the same component. A person debugging the code would typically be looking at it and so would be able to determine the appropriate name to enable. The hierarchy allows all components to be easily enabled or disabled together.
As an alternative for TRACE loggers where there are different messages at increasing levels of verbosity but no specific component names that would be appropriate, or where increasing verbosity spans a number of levels of the component hierarchy, logger names can be prefixed with "TRACE1", "TRACE2", "TRACE3", etc. to indicate increasing verbosity.

.. code-block:: python

   traceLogger = lsst.log.Log.getLogger("TRACE2.meas.algorithms.starSelector")
   traceLogger.debug("On %d-th iteration of star selection", iteration)
   innerTraceLogger = lsst.log.getLogger("TRACE2.meas.algorithms.starSelector.catalogReader")
   innerTraceLogger.debug("Reading catalog %s", catalogName)

.. code-block:: c++

   LOG_LOGGER traceLogger = LOG_GET("TRACE2.meas.algorithms.starSelector");
   LOGL_DEBUG(traceLogger, "On %d-th iteration of star selection", iteration);
   LOG_LOGGER innerTraceLogger = LOG_GET("TRACE2.meas.algorithms.starSelector.catalogReader");
   LOGL_DEBUG(innerTraceLogger, "Reading catalog %s", catalogName);

Notice that all loggers in the hierarchy under a given component at a given trace level can be enabled easily using, e.g., "TRACE2.lsst.meas.algorithms.starSelector".
Getting a logger object and logging to that is preferred over logging using a string as the logger name. The latter can be used, for examples:

.. code-block:: python

   lsst.log.log("meas.algorithms.starSelector.psfCandidate", lsst.log.WARN, "Failed to make a psfCandidate")
   lsst.log.log("TRACE4.meas.algorithms.starSelector.psfCandidate", lsst.log.DEBUG, "Making a psfCandidate from star %d=", starId)

.. code-block:: c++

   LOGL_WARN("meas.algorithms.starSelector.psfCandidate", "Failed to make a psfCandidate")
   LOGL_DEBUG("TRACE4.meas.algorithms.starSelector.psfCandidate", "Making a psfCandidate from star %d=", starId)

Developers are encouraged to insert log messages whenever and wherever they might be useful, with appropriate component names and levels.
