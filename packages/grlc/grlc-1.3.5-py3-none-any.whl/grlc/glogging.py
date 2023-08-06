import logging

import grlc.static as static

def getGrlcLogger(name):
    """Construct a logger for grlc with the logging level specified on `config.ini`."""
    glogger = logging.getLogger(name)
    if static.LOG_DEBUG_MODE:
        glogger.setLevel(logging.DEBUG)
    return glogger
