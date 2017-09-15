from database import create_session


def check_if_sensor_exists(form, session, sensor):
    return session.query(sensor).filter_by(place_id=form.sensor_place.data, sensor_id=form.sensor_id.data).one_or_none()


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
        if filter_form.filter_type.data == "sensor":
            for sensor in session.query(sensor_).filter_by(sensor_id=filter_form.sensor_name.data).all():
                if sensor:
                    sensors[sensor.id] = sensor
            return sensors
        else:
            for sensor in session.query(sensor_).filter_by(place_id=filter_form.place_name.data).all():
                if sensor:
                    sensors[sensor.id] = sensor
            return sensors
