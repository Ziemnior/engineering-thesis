from database import create_session


def check_if_sensor_id_exists(form, session, sensor):
    return session.query(sensor).filter_by(sensor_id=form.sensor_id.data).one_or_none()


def display_registered_sensors(sensor_):
    sensors = dict()
    with create_session() as session:
        for sensor in session.query(sensor_).order_by(sensor_.place_id.asc()).all():
            if sensor:
                sensors[sensor.id] = sensor
        return sensors


def filter_sensors(filter_form, sensor_):
    sensors = dict()
    with create_session() as session:
        for sensor in session.query(sensor_).filter_by(place_id=filter_form.place_name.data).all():
            if sensor:
                sensors[sensor.id] = sensor
        return sensors


def get_sensor_specific_records(record, sensor_id):
    with create_session() as session:
        return session.query(record).filter_by(sensor_id=sensor_id).order_by(record.timestamp.desc()).all()


def get_sensors_for_specific_gateway(sensor, gateway_id):
    with create_session() as session:
        return session.query(sensor).filter_by(gateway_id=gateway_id).order_by(sensor.place_id.asc()).all()


def get_records_for_specific_gateway(record, gateway_id):
    with create_session() as session:
        return session.query(record).filter_by(gateway_id=gateway_id).order_by(record.timestamp.desc()).all()


def filter_records_by_status(record, sensor_id, filter_form):
    with create_session() as session:
        return session.query(record).filter_by(sensor_id=sensor_id, in_use=filter_form.filter_status.data).order_by(
            record.timestamp.desc()).all()


def delete_sensor(sensor, sensor_id):
    with create_session() as session:
        return session.query(sensor).filter(sensor.sensor_id == sensor_id).delete()


def delete_gateway(sensor, gateway_id):
    with create_session() as session:
        return session.query(sensor).filter(sensor.gateway_id == gateway_id).delete()
