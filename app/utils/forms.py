from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, RadioField, IntegerField
from wtforms.validators import InputRequired, Email, Length, EqualTo
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from models import RecordUnregistered
from database import create_session


def get_unregistered_id():
    with create_session() as session:
        return session.query(RecordUnregistered)


class LoginForm(FlaskForm):
    email = StringField('Email Address')
    password = PasswordField('Password')


class RegisterForm(FlaskForm):
    email = StringField('Email Address', validators=[
        InputRequired(), Email(message="Incorrect email")])
    name = StringField('Name', validators=[
        InputRequired()])
    surname = StringField('Surname', validators=[
        InputRequired()])
    password = PasswordField('Password', validators=[
        InputRequired(),
        EqualTo('confirm_password', message="Passwords don't match")])
    confirm_password = PasswordField("Confirm password")
    role = RadioField("Check role:", choices=[('user', "Regular user"), ('admin', "Admin")],
                      validators=[InputRequired()])
    user_id = QuerySelectField('Select user card', query_factory=get_unregistered_id,
                               validators=[InputRequired()])


class AddSensorForm(FlaskForm):
    sensor_place = StringField('Sensor place', validators=[InputRequired()])
    sensor_id = StringField('Sensor ID', validators=[InputRequired()])
