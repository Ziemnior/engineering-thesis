from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, RadioField, IntegerField
from wtforms.validators import InputRequired, Email, Length, EqualTo
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from database import create_session
from models import Record, User


def get_unregistered_id():
    with create_session() as session:
        return session.query(Record).filter_by(is_registered=True, in_use=False).all()


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


class EditForm(FlaskForm):
    email = StringField('Email Address')
    name = StringField('Name')
    surname = StringField('Surname')
    password = PasswordField('Password',
                             validators=[EqualTo('confirm_password', message="Passwords don't match")])
    confirm_password = PasswordField("Confirm password")
    role = RadioField("Check role:", choices=[('user', "Regular user"), ('admin', "Admin")])
    user_id = QuerySelectField('Select user card', query_factory=get_unregistered_id)


class AddSensorForm(FlaskForm):
    sensor_place = StringField('Sensor place', validators=[InputRequired()])
    sensor_id = StringField('Sensor ID', validators=[InputRequired()])


class FilterSensorForm(FlaskForm):
    filter_type = RadioField("Select filter:", choices=[('place', "Place"), ('sensor', "Sensor")])
    sensor_name = StringField('Sensor name')
    place_name = StringField('Place name')
