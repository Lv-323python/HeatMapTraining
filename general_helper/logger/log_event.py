"""
    log event
"""

from fluent import sender
from fluent import event
from general_helper.general_utils import get_file_name
from general_helper.logger.log_config import HOST, PORT


def event_log_maker(message='some message'):
    """

    :param message: str - message to forwarding into log center
    :return: None
    """

    try:
        message = str(message)
    except BaseException:
        message = 'some invalid message'

    sender.setup(get_file_name(__file__), host=HOST, port=PORT)
    event.Event('events', {'event': message})
    sender.close()
