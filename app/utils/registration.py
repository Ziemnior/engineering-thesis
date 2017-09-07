from database import create_session
from models import RecordUnregistered
from flask import flash


def check_existing_uids():
    with create_session() as session:
        if not session.query(RecordUnregistered).all():
            flash("No cards to assign to user!", "warning")
