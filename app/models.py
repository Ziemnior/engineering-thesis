from flask_login import UserMixin
from sqlalchemy import Column, DateTime, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class Record(Base):
    __tablename__ = 'records'
    id = Column(Integer, primary_key=True)
    sensor_id = Column(String, ForeignKey('sensors.id'))
    sensor = relationship("Sensor", back_populates="records")
    user_id = Column(String)
    timestamp = Column(DateTime)

    def __repr__(self):
        return "<Record(sensor_id='%s', user_id='%s')>" % (self.sensor_id, self.user_id)


class RecordUnregistered(Base):
    __tablename__ = 'records_unregistered'
    id = Column(Integer, primary_key=True)
    sensor_id = Column(String)
    user_id = Column(String)
    timestamp = Column(DateTime)

    def __repr__(self):
        return "<Record(sensor_id='%s', user_id='%s')>" % (self.sensor_id, self.user_id)


class Sensor(Base):
    __tablename__ = 'sensors'
    id = Column(Integer, primary_key=True)
    place_id = Column(Integer, ForeignKey('places.id'))
    place = relationship("Place", back_populates="places")
    records = relationship("Record", order_by=Record.id, back_populates="sensor")

    def __repr__(self):
        return "<Sensor(id='%s', at='%s')>" % (self.id, self.place_id)


class Place(Base):
    __tablename__ = 'places'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    places = relationship("Sensor", order_by=Record.id, back_populates="place")

    def __repr__(self):
        return "<Place(id='%s', name='%s')>" % (self.id, self.name)


class User(Base, UserMixin):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True)
    name = Column(String)
    surname = Column(String)
    password = Column(String)
    card_id = Column(String, unique=True)

    def __repr__(self):
        return "<User(email=%s, card_id=%s)>" % (self.email, self.card_id)
