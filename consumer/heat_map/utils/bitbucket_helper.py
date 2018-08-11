"""
A library of helpers of bitbucket_request_sender use
"""

from heat_map.utils.helper import format_date_to_int


def to_timestamp(date_time_str):
    """
    Converts datetime string to timestamp

    :param date_time_str: string - datetime string
    :return: int - timestamp
    """
    return format_date_to_int(date_time_str[0:19], "%Y-%m-%dT%H:%M:%S")


def get_gitname(commit):
    """

    :param commit: dict - commit in response
    :return: string - name
    """

    if 'user' in commit['author']:
        result_name = commit['author']['user']['username']
    else:
        result_name = commit['author']['raw'][:commit['author']['raw'].find('<') - 1]
    return result_name


def get_email(author_raw):
    """
    Extracts author email from author_raw string

    :param author_raw: string
    :return: string
    """
    return author_raw[author_raw.find('<') + 1:-1]
