from flask import Flask, Response, request, render_template, flash, redirect, url_for
from database import init_db, create_session
from datetime import datetime
from flask_bootstrap import Bootstrap
from flask_login import LoginManager, login_required, login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash
from models import Record, Record_unreg, Sensor, Place, User
from utils.forms import AddSensorForm, LoginForm, RegisterForm
import json
import requests

app = Flask(__name__)
Bootstrap(app)
init_db()

login_manager = LoginManager()
login_manager.init_app(app)

app.config['SECRET_KEY'] = 'secretkey'
app.config['TEMPLATES_AUTO_RELOAD'] = True


@login_manager.user_loader
def load_user(user_id):
    with create_session() as session:
        return session.query(User).get(user_id)


@app.route("/api/post-record", methods=["POST"])
def process_record_post():
    data = json.loads(request.data)
    with create_session() as session:
        if session.query(Sensor).filter_by(place_id=data["sensor_id"]).first():
            record = Record(sensor_id=data["sensor_id"],
                            user_id=data["user_id"],
                            timestamp=datetime.now())
            session.add(record)
        else:
            record = Record_unreg(sensor_id=data["sensor_id"],
                                  user_id=data["user_id"],
                                  timestamp=datetime.now())
            session.add(record)
    return Response(status=201)


def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (getattr(form, field).label.text, error))


@app.route("/")
def home():
    records = dict()
    with create_session() as session:
        for place in session.query(Place).order_by(Place.name.asc()).all():
            record = (session.query(Record).
                      join(Sensor).
                      filter(Sensor.place_id == place.id))
            if record:
                records[place.id] = record
    return render_template('index.html', records=records)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        with create_session() as session:
            user = session.query(User).filter_by(email=form.email.data).first()
            if user and check_password_hash(user.password, form.password.data):
                login_user(user)
                flash("You're now logged in", "success")
                return redirect(url_for('home'))
            else:
                flash("Invalid email or password", "error")
    return render_template("login.html", form=form)


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        with create_session() as session:
            email = session.query(User).filter_by(email=form.email.data).one_or_none()
            if email is None:
                hashed_password = generate_password_hash(form.password.data)
                user = User(email=form.email.data, password=hashed_password)
                session.add(user)
                flash("You can now log in", "success")
            else:
                flash("Email already exists in database", "error")
    return render_template('register.html', form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have logged out", "info")
    return redirect("/")


@app.route("/addsensor", methods=['GET', 'POST'])
def addsensor():
    form = AddSensorForm()
    if form.validate_on_submit():
        with create_session() as session:
            place = Place(name=form.sensor_place.data)
            sensor = Sensor(place_id=form.sensor_id.data)
            session.add(place)
            session.add(sensor)
    else:
        flash("Please fill out all fields", "warning")
    return render_template("addsensor.html", form=form)


if __name__ == "__main__":
    app.run()
