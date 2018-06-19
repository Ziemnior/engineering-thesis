from flask import flash, redirect, url_for
from flask_login import current_user
from functools import wraps
from models import User
from database import create_session


def requires_roles(*roles):
    def wrapper(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            if get_current_user_role() not in roles:
                return error_response()
            return f(*args, **kwargs)
        return wrapped
    return wrapper


def get_current_user_role():
    with create_session() as session:
        try:
            get_role = session.query(User.role).filter_by(email=current_user.email).first()
            return "".join(get_role)
        except AttributeError:
            return None


def error_response():
    flash('Authentication error, please check your details and try again', "error")
    return redirect(url_for('home'))
