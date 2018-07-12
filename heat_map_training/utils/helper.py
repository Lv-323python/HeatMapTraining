"""
A library of helpers of general use
"""
from datetime import datetime


def format_date_to_int(date, format_string):
    """
    Creates an int(timestamp) from a string representing a date and time and a corresponding
    format string

    :param date: string
    :param format_string: string
    :return: int
    """
    try:
        formatted_date = int(datetime.strptime(date, format_string).timestamp())
    except ValueError:
        formatted_date = 0
    return formatted_date
