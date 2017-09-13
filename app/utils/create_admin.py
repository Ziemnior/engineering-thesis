from werkzeug.security import generate_password_hash
from database import create_session
from models import User


def create_admin_account():
    with create_session() as session:
        email = session.query(User).filter_by(email="djpitugta@gmail.com").one_or_none()
        if email is None:
            admin = User(email="djpitugta@gmail.com", name="Jan", surname="Kowalski",
                         password=generate_password_hash("1111"), card_id=None, role="admin")
            session.add(admin)
        else:
            pass


if __name__ == "__main__":
    create_admin_account()
