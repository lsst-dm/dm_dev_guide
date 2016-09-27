import lsst.log.utils


def writeMessages():
    """Write debugging messages under TRACEn.example.component

    In application code, they may appear either in Python or C++ codebase
    """
    lsst.log.info("Writing 6 debug messages")
    for n in range(6):
        lsst.log.log("TRACE%d.example.component" % n, lsst.log.DEBUG, "Fine tracing to TRACE%d" % n)


# Demonstrate using the utility function traceSetAt to set the levels for a
# group of loggers so it display messages with trace number <= the threshold
for threshold in range(6):
    lsst.log.info("Setting trace at %d", threshold)
    lsst.log.utils.traceSetAt("example.component", threshold)
    writeMessages()
