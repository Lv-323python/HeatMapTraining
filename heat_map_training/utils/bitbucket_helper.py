"""
A library of helpers of bitbucket_request_sender use
"""

from heat_map_training.utils.helper import format_date_to_int


def to_timestamp(date_time_str):
    """
    Converts datetime string to timestamp

    :param date_time_str: string - datetime string
    :return: int - timestamp
    """
    return format_date_to_int(date_time_str[0:19], "%Y-%m-%dT%H:%M:%S")


def get_gitname(author_raw):
    """
    Extracts author gitname from author_raw string

    :param author_raw: string
    :return: string
    """
    return author_raw[:author_raw.find('<') - 1]


def get_email(author_raw):
    """
    Extracts author email from author_raw string

    :param author_raw: string
    :return: string
    """
    return author_raw[author_raw.find('<') + 1:-1]
