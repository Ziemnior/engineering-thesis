from database import create_session
from utils.businesshours import BusinessHours
from datetime import timedelta, datetime
from collections import Counter
import json
import requests


def process_record(record, user, sensor, request, response, if_sensor_registered, if_uid_registered):
    data = json.loads(request.data)
    with create_session() as session:
        record = record(sensor_id=data["sensor_id"],
                        user_id=data["user_id"],
                        is_registered=if_sensor_registered(data, session, sensor),
                        in_use=if_uid_registered(data, session, user),
                        timestamp=datetime.now())
        session.add(record)
    return response(status=201)


def delete_record(record, id):
    with create_session() as session:
        return session.query(record).filter(record.id == id).delete()


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
        real_time[i] = [timedelta(seconds=(int(time_in_seconds))), boundaries[0].timestamp, boundaries[1].timestamp]
        i += 1
    return real_time


def calculate_overtime(user):
    real_time = calculate_real_time(user)
    overtime = dict()
    for key, value in calculate_usual_worktime(user).items():
        overtime[key] = [real_time[key][0] - value[0], value[1], value[2]]

    return overtime


def calculate_basic_salary(user):
    salary = Counter()
    for key, value in calculate_usual_worktime(user).items():
        salary[(value[1].month, value[1].year)] += value[0].total_seconds() / 3600
    return salary


def calculate_extended_salary(user):
    extended_salary = Counter()
    for key, value in calculate_overtime(user).items():
        extended_salary[(value[1].month, value[1].year)] += value[0].total_seconds() / 3600
    return extended_salary
