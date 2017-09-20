from database import create_session
from utils.businesshours import BusinessHours


def get_even_workdays(records):
    if len(records) % 2 == 1:
        records.pop(0)
    return records


def get_workday_boundaries(user):
    return [list(x) for x in zip(get_even_workdays(user)[::2], get_even_workdays(user)[1::2])]


def calculate_worktime(user):
    worktime = dict()
    i = 0
    for boundaries in get_workday_boundaries(user):
        business_time = BusinessHours(boundaries[1].timestamp, boundaries[0].timestamp)
        worktime[i] = [business_time.get_minutes(), boundaries[0], boundaries[1]]
        i += 1
    return worktime