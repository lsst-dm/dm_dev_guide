import logging
import sys
import lsst.utils.logging

logging.basicConfig(level=logging.INFO, stream=sys.stdout)
root_logger = logging.getLogger()


def writeMessages():
    """Write debugging messages under TRACEn.example.component

    In application code, they may appear either in Python or C++ codebase
    """
    root_logger.info("Writing 6 debug messages")
    for n in range(6):
        logging.getLogger(f"TRACE{n}.example.component").debug("Fine tracing to TRACE%d", n)


# Demonstrate using the utility function trace_set_at to set the levels for a
# group of loggers so it display messages with trace number <= the threshold
for threshold in range(6):
    root_logger.info("Setting trace at %d", threshold)
    lsst.utils.logging.trace_set_at("example.component", threshold)
    writeMessages()
