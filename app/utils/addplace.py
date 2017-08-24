from database import create_sesion


def addsensor():
    with create_session() as session:
        place = Place(name=place_name)
        sensor = Sensor(place_id=place_number)
        session.add(place)
        session.add(sensor)
        
