"""
    config file that declare logging system
     and its handling to Fluend log system.
     Gives logging object as 'l' to call needed log method, ex:
        "Critical, ERROR, WARNING, INFO, DEBUG, NOTSET"
"""

import logging
from fluent import handler

HOST = 'localhost'
PORT = 24224

# format for data that saves into general log file via Fluentd.
CUSTOM_FORMAT = {
    'host': '%(hostname)s',
    'where': '%(module)s.%(funcName)s',
    'type': '%(levelname)s',
    'stack_trace': '%(exc_text)s'
}

# sets level of logging
logging.basicConfig(level=logging.INFO)

# ! ! ! used to Import ! ! !
# gets logger from logging module.
LOG = logging.getLogger('foo')

# gets handler
MY_HANDLER = handler.FluentHandler('app.follow', host=HOST, port=PORT)

# gets formatter with custom format
FORMATTER = handler.FluentRecordFormatter(CUSTOM_FORMAT)

# sets format for Fluend handler
MY_HANDLER.setFormatter(FORMATTER)

# adds handler for logging
LOG.addHandler(MY_HANDLER)
