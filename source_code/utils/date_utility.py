# define functions to handle date and time
from datetime import datetime, timedelta

import pytz


# function to get current time in PST
def get_current_time_in_pst():
    # Create a timezone object for US/Eastern
    pacific_tz = pytz.timezone('US/Pacific')
    return datetime.now()


# function to add time in minutes to a given time
def add_time_in_minutes(as_of_date_time, minutes: int):
    return as_of_date_time + timedelta(minutes=minutes)


# format date time to string
def format_date_time_to_string(as_of_date_time=datetime.now(), fmt='%Y-%m-%d %H:%M:%S %Z%z'):
    return as_of_date_time.strftime(fmt)


def get_current_date_as_date():
    return datetime.now().date()


def get_current_date(format='%Y-%m-%d'):
    return datetime.now().strftime(format)


def format_date_to_string(in_date, format='%Y-%m-%d'):
    return in_date.strftime(format)


def convert_str_to_date(in_date):
    return datetime.strptime(in_date, '%Y-%m-%d')