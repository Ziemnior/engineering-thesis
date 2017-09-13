from flask import Flask, Response, request, render_template, flash, redirect, url_for
from database import init_db, create_session
from datetime import datetime
from flask_bootstrap import Bootstrap
from flask_login import LoginManager, login_required, login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash
from models import Record, Sensor, User
from utils.forms import AddSensorForm, LoginForm, RegisterForm, EditForm
from utils.roles import requires_roles
from utils.create_admin import create_admin_account
from utils.registration import check_existing_uids, check_if_user_exists, if_sensor_registered
import json
import requests
from sqlalchemy import func

app = Flask(__name__)
Bootstrap(app)

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
        record = Record(sensor_id=data["sensor_id"],
                        user_id=data["user_id"],
                        is_registered=if_sensor_registered(data),
                        timestamp=datetime.now())
        session.add(record)
    return Response(status=201)


@app.route("/")
def home():
    return render_template('index.html')


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
@requires_roles('admin')
def register():
    form = RegisterForm()
    check_existing_uids()
    if form.validate_on_submit():
        with create_session() as session:
            if not check_if_user_exists(form):
                hashed_password = generate_password_hash(form.password.data)
                user = User(email=form.email.data, name=form.name.data, surname=form.surname.data,
                            password=hashed_password, card_id=form.user_id.data.user_id, role=form.role.data)
                session.add(user)
                session.query(Record).filter_by(user_id=form.user_id.data.user_id).update({Record.is_registered: True})
                session.commit()
                flash("You can now log in", "success")
                return redirect(url_for('home'))
            else:
                flash("Email or card already registered in the database", "error")
    return render_template('register.html', form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have logged out", "info")
    return redirect("/")


@app.route("/addsensor", methods=["GET", "POST"])
@requires_roles('admin')
def addsensor():
    form = AddSensorForm()
    if form.validate_on_submit():
        with create_session() as session:
            sensor = Sensor(place_id=form.sensor_place.data, sensor_id=form.sensor_id.data)
            session.add(sensor)
            flash("Sensor added successfully", "success")
        return redirect(url_for('addsensor'))

    sensors = dict()
    with create_session() as session:
        for sensor in session.query(Sensor).order_by(Sensor.place_id.asc()).all():
            if sensor:
                sensors[sensor.id] = sensor
    return render_template("addsensor.html", form=form, sensors=sensors)


@app.route("/onsite")
@requires_roles('admin')
def onsite():
    return render_template("onsite.html", people=people)


@app.route('/user')
@requires_roles('admin')
def user():
    with create_session() as session:
        users = session.query(User).all()
    return render_template("user.html", users=users)


@app.route('/user-profile/<id>')
@requires_roles('admin')
def user_profile(id):
    with create_session() as session:
        user = session.query(User).filter(User.id == id).first()
    return render_template("user-profile.html", user=user)


@app.route('/user-profile/<id>/edit', methods=["GET", "POST"])
def edit_profile(id):
    with create_session() as session:
        user = session.query(User).filter(User.id == id).first()
        form = EditForm(obj=user)
        form.email.render_kw = {'readonly': True}
        if form.validate_on_submit():
            form.populate_obj(user)
            session.commit()
            flash("Profile updated successfully", "success")
            return redirect(url_for('user_profile', id=id))
    return render_template("edit.html", id=id, form=form, user=user)


if __name__ == "__main__":
    init_db()

    create_admin_account()
    app.run()
