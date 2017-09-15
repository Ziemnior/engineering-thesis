from database import create_session


def check_existing_uids(record, flash):
    with create_session() as session:
        if not session.query(record).filter_by(is_registered=True, in_use=False).first():
            flash("No cards to assign to user!", "warning")


def check_if_user_exists(form, session, user):
    email = session.query(user).filter_by(email=form.email.data).one_or_none()
    user_id = session.query(user).filter_by(card_id=form.user_id.data.user_id).one_or_none()
    return email or user_id


def if_sensor_registered(data, session, sensor):
    return bool(session.query(sensor).filter_by(sensor_id=data["sensor_id"]).first())


def if_uid_registered(data, session, user):
    return bool(session.query(user).filter_by(card_id=data["user_id"]).one_or_none())


def update_record_status(form, session, record):
    for new_sensor in session.query(record).filter_by(sensor_id=form.sensor_id.data).all():
        new_sensor.is_registered = True
        session.commit()


def update_uid_status(form, session, record):
    for uid in session.query(record).filter_by(user_id=form.user_id.data.user_id).all():
        uid.in_use = True
        session.commit()
