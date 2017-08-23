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
        return "<Record(type='%s', value='%s', date='%s')>" % (self.data_type, self.value, self.date)


class Sensor(Base):
    __tablename__ = 'sensors'
    id = Column(Integer, primary_key=True)
    place_id = Column(Integer, ForeignKey('places.id'))
    place = relationship("Place", back_populates="places")
    records = relationship("Record", order_by=Record.id, back_populates="sensor")

    def __repr__(self):
        return "<Sensor(id='%s', at='%s')>" % (self.id, self.place)


class Place(Base):
    __tablename__ = 'places'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    places = relationship("Sensor", order_by=Record.id, back_populates="place")

    def __repr__(self):
        return "<Place(id='%s', name='%s')>" % (self.id, self.name)

