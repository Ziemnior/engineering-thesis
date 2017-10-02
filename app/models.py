from flask_login import UserMixin
from sqlalchemy import Column, DateTime, String, Integer, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class Record(Base):
    __tablename__ = 'records'
    id = Column(Integer, primary_key=True)
    sensor_id = Column(String, ForeignKey('sensors.id'))
    sensor = relationship("Sensor", back_populates="records")
    user_id = Column(String)
    timestamp = Column(DateTime)
    is_registered = Column(Boolean)
    in_use = Column(Boolean)

    def __repr__(self):
        return "{} [{}]".format(self.user_id, self.timestamp.__format__('%Y-%m-%d %H:%M:%S'))


class Sensor(Base):
    __tablename__ = 'sensors'
    id = Column(Integer, primary_key=True)
    place_id = Column(String)
    sensor_id = Column(String, unique=True)
    records = relationship("Record", order_by=Record.id, back_populates="sensor")

    def __repr__(self):
        return "<Sensor(id={}, place_id={}, sensor_id={})>".format(self.id, self.place_id, self.sensor_id)


class User(Base, UserMixin):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True)
    name = Column(String)
    surname = Column(String)
    password = Column(String)
    role = Column(String)
    card_id = Column(String, unique=True)
    phone_number = Column(Integer)
    address = Column(String)
    postal_code = Column(Integer)
    city = Column(String)

    def __repr__(self):
        return "<User(email={}, role={}, card_id={})>".format(self.email, self.role, self.card_id)
