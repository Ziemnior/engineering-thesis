import jinja2
import calendar
from datetime import timedelta


def int_to_month(input):
    return calendar.month_name[input]


def int_to_hour(input):
    return timedelta(hours=input)
