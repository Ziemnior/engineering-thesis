from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, TextAreaField
from wtforms.validators import InputRequired, Email, Length, EqualTo
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from models import User
from database import create_session

class LoginForm(FlaskForm):
    email = StringField('Email Addres')
    password = PasswordField('Password')


class RegisterForm(FlaskForm):
    email = StringField('Email Address', validators=[
        InputRequired(), Email(message="Incorrect email")])
    password=PasswordField('Password', validators=[
        InputRequired(),
        EqualTo('confirm_password', message="Passwords don't match")])
    confirm_password = PasswordField("Confirm password")
    user_id = StringField("Placeholder")


class AddSensorForm(FlaskForm):
    sensor_place = StringField("Sensor place", validators=[InputRequired()])
    sensor_id = StringField("Sensor ID", validators=[InputRequired()])
