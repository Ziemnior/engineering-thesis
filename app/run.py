from flask import Flask, Response, request
from database import create_session, init_db
from datetime import datetime
from models import Record
from flask_bootstrap import Bootstrap
from models import Record, Sensor, Place
import json
import requests
 
app = Flask(__name__)
#Bootstrap(app)
init_db()
 
app.config['SECRET_KEY'] = 'secretkey'
app.config['TEMPLATES_AUTO_RELOAD'] = True
 
 
@app.route("/api/post-record", methods=["POST"])
def process_record_post():
    data = json.loads(request.data)
    with create_session() as session:
        record = Record(sensor_id=data["sensor_id"],
                        user_id=data["user_id"],
        timestamp=datetime.now())
        session.add(record)
    return Response(status=201)
 
@app.route("/")
def home():
    return "homepage"
 
if __name__ == "__main__":
    with create_session() as session:
        gate = Place(name="Gate")
        sensor1 = Sensor(place_id=1)
        session.add(gate)
        session.add(sensor1)
        print(sensor1)
    app.run()

