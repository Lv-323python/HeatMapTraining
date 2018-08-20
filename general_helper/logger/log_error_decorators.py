"""
    module that contains try-except decorator function
"""

from functools import wraps

from general_helper.logger.log_config import LOG


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

        except BaseException as exc:
            LOG.error('message from try_except_decor', exc_info=exc)
            return None

    return wrapper
