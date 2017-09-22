from database import create_session
from utils.businesshours import BusinessHours
from datetime import timedelta
from collections import Counter


def get_even_workdays(records):
    if len(records) % 2 == 1:
        records.pop(0)
    return records


def get_workday_boundaries(user):
    return map(list, zip(get_even_workdays(user)[::2], get_even_workdays(user)[1::2]))


def calculate_usual_worktime(user):
    worktime = dict()
    i = 0
    for boundaries in get_workday_boundaries(user):
        business_time = BusinessHours(boundaries[1].timestamp, boundaries[0].timestamp)
        worktime[i] = [timedelta(seconds=(business_time.get_seconds())), boundaries[0].timestamp,
                       boundaries[1].timestamp]
        i += 1
    return worktime


def calculate_real_time(user):
    real_time = dict()
    i = 0
    for boundaries in get_workday_boundaries(user):
        time_in_seconds = (boundaries[0].timestamp - boundaries[1].timestamp).total_seconds()
        real_time[i] = timedelta(seconds=(int(time_in_seconds)))
        i += 1
    return real_time


def calculate_overtime(user):
    real_time = calculate_real_time(user)
    overtime = dict()
    for key, value in calculate_usual_worktime(user).items():
        overtime[key] = real_time[key] - value[0]
    return overtime


def calculate_monthly_salary(user):
    salary = Counter()
    for key, value in calculate_usual_worktime(user).items():
        salary[(value[1].month, value[1].year)] += int(value[0].total_seconds() / 3600)
    return salary