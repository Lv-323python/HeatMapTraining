"""
    A library of helpers of gitlab_request_senders use
"""

from heat_map_training.utils.helper import format_date_to_int


def get_time_utc(time):
    """
    return time from helper's function
    :param time: string
    :return: int
    """
    if time[-1] == 'Z':
        return format_date_to_int(time + '+0000', "%Y-%m-%dT%H:%M:%S.%fZ%z")

    return format_date_to_int(time[:26] + time[27:29], "%Y-%m-%dT%H:%M:%S.%f%z")
