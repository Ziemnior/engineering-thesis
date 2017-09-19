import json
import requests

from flask import Flask, Response, request, render_template, flash, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_login import LoginManager, login_required, login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash

from database import init_db, create_session
from datetime import datetime
from models import Record, Sensor, User
from utils.forms import AddSensorForm, LoginForm, RegisterForm, EditForm, FilterSensorForm, FilterSensorStatusForm
from utils.roles import requires_roles
from utils.create_admin import create_admin_account
from utils.register import check_existing_uids, check_if_user_exists, if_sensor_registered, update_record_status, \
    if_uid_registered, update_uid_status
from utils.users import get_people_on_site, get_user_profile, get_users, get_user_records
from utils.sensors import check_if_sensor_id_exists, display_registered_sensors, filter_sensors, \
    get_sensor_specific_records, filter_records_by_status

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
                        is_registered=if_sensor_registered(data, session, Sensor),
                        in_use=if_uid_registered(data, session, User),
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
    check_existing_uids(Record, flash)
    if form.validate_on_submit():
        with create_session() as session:
            if not check_if_user_exists(form, session, User):
                hashed_password = generate_password_hash(form.password.data)
                user = User(email=form.email.data, name=form.name.data, surname=form.surname.data,
                            password=hashed_password, card_id=form.user_id.data.user_id, role=form.role.data)
                session.add(user)
                update_uid_status(form, session, Record)
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
            if not check_if_sensor_id_exists(form, session, Sensor):
                sensor = Sensor(place_id=form.sensor_place.data, sensor_id=form.sensor_id.data)
                session.add(sensor)
                update_record_status(form, session, Record)
                flash("Sensor added successfully", "success")
            else:
                flash("Sensor ID already registered in database", "error")
        return redirect(url_for('sensors'))
    return render_template("addsensor.html", form=form)


@app.route("/sensor", methods=["GET", "POST"])
@requires_roles('admin')
def sensors():
    return render_template("sensor.html", sensors=display_registered_sensors(Sensor), filter_form=FilterSensorForm())


@app.route("/sensor/filter", methods=["GET", "POST"])
@requires_roles('admin')
def sensor_filter():
    return render_template("sensor.html", sensors=filter_sensors(filter_form, Sensor), filter_form=FilterSensorForm(),
                           flag=1)


@app.route("/sensor/<sensor_id>", methods=["GET", "POST"])
@requires_roles('admin')
def sensor_records(sensor_id):
    return render_template("sensor-records.html", records=get_sensor_specific_records(Record, sensor_id),
                           sensor_id=sensor_id, form=FilterSensorStatusForm())


@app.route("/sensor/<sensor_id>/filter", methods=["GET", "POST"])
@requires_roles('admin')
def sensor_records_filter(sensor_id):
    form = FilterSensorStatusForm()
    return render_template("sensor-records.html", form=form, records=filter_records_by_status(Record, sensor_id, form),
                           sensor_id=sensor_id, flag=1)


@app.route("/onsite")
@requires_roles('admin')
def onsite():
    return render_template("onsite.html", people=get_people_on_site(Record, User))


@app.route('/user')
@requires_roles('admin')
def user():
    return render_template("user.html", users=get_users(User))


@app.route('/user-profile/<id>')
@requires_roles('admin')
def user_profile(id):
    return render_template("user-profile.html", user=get_user_profile(User, id), records=get_user_records(Record, User))


@app.route('/user-profile/<id>/all-records')
@requires_roles('admin')
def user_records(id):
    return render_template("user-records.html", user=get_user_profile(User, id), records=get_user_records(Record, User))


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
