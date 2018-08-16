"""
    module that contains try-except decorator function
"""

import traceback
from functools import wraps

from fluent import sender
from fluent import event

from general_helper.logger.log_config import HOST, PORT
from general_helper.general_utils import get_file_name


def try_except_decor(func):
    """
        Decorator that run function in 'try-except' way,
        returns function result or None with forwarding
        error message to log center.

    :param func: function to decorate
    :return: function object - decorated function
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        """
            Wrapper for decorator.

        :param args:
        :param kwargs:
        :return:
        """
        try:
            return func(*args, **kwargs)
        # except:
        except BaseException:
            # Get current system exception
            error = traceback.format_exc()

            sender.setup(get_file_name(__file__), host=HOST, port=PORT)
            event.Event('error', {'exception': error})
            sender.close()

            return None

    return wrapper
