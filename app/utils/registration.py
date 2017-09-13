from database import create_session
from models import Record, Sensor, User
from flask import flash


def check_existing_uids():
    with create_session() as session:
        if not session.query(Record).filter_by(is_registered=False).first():
            flash("No cards to assign to user!", "warning")


def check_if_user_exists(form):
    with create_session() as session:
        email = session.query(User).filter_by(email=form.email.data).one_or_none()
        user_id = session.query(User).filter_by(card_id=form.user_id.data.user_id).one_or_none()
    return (email or user_id)


def if_sensor_registered(data):
    with create_session() as session:
        return bool(session.query(Sensor).filter_by(sensor_id=data["sensor_id"]).one_or_none())
