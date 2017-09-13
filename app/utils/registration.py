from database import create_session
from models import RecordUnregistered
from flask import flash


def check_existing_uids():
    with create_session() as session:
        if not session.query(RecordUnregistered).all():
            flash("No cards to assign to user!", "warning")


def return_uid(form):
    if form.role.data == 'admin':
        return None
    else:
        with create_session() as session:
            session.query(RecordUnregistered).filter_by(user_id=form.user_id.data.user_id).delete()
        return form.user_id.data.user_id

