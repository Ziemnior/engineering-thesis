from database import create_session
from utils.businesshours import BusinessHours


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
        worktime[i] = [business_time.get_hours_minutes(), boundaries[0].timestamp, boundaries[1].timestamp]
        i += 1
    return worktime


def calculate_real_time(user):
    real_time = dict()
    i = 0
    for boundaries in get_workday_boundaries(user):
        real_time[i] = (boundaries[0].timestamp - boundaries[1].timestamp).seconds // 60
        i += 1
    return real_time


def calculate_overtime(user):
    overtime = dict()
    real_time = calculate_real_time(user)
    for key, value in calculate_usual_worktime(user).items():
        overtime[key] = real_time[key] - value[0]
    return overtime
