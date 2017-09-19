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
        InputRequired(message="Enter name")])
    surname = StringField('Surname', validators=[
        InputRequired(message="Enter surname")])
    password = PasswordField('Password', validators=[
        InputRequired(message="Enter password"),
        EqualTo('confirm_password', message="Passwords don't match")])
    confirm_password = PasswordField("Confirm password")
    role = RadioField("Check role:", choices=[('user', "Regular user"), ('admin', "Admin")],
                      validators=[InputRequired(message="Select role")])
    user_id = QuerySelectField('Select user card', query_factory=get_unregistered_id,
                               validators=[InputRequired(message="Select card ID to assign to user")])


class EditForm(FlaskForm):
    email = StringField('Email Address')
    name = StringField('Name')
    surname = StringField('Surname')
    password = PasswordField('Password',
                             validators=[EqualTo('confirm_password', message="Passwords don't match")])
    confirm_password = PasswordField("Confirm password")
    role = RadioField("Check role:", choices=[('user', "Regular user"), ('admin', "Admin")])
    user_id = QuerySelectField('Select user card', query_factory=get_unregistered_id, allow_blank=True)


class AddSensorForm(FlaskForm):
    sensor_place = StringField('Sensor place', validators=[InputRequired(message="Enter sensor place")])
    sensor_id = StringField('Sensor ID', validators=[InputRequired(message="Enter sensor ID")])


class FilterSensorForm(FlaskForm):
    place_name = StringField('Place name')


class FilterSensorStatusForm(FlaskForm):
    filter_status = RadioField("Status", choices=[(1, "Registrered"), (0, "Unregistered")])
