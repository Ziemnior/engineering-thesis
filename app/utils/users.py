from database import create_session
from sqlalchemy import func


def get_people_on_site(record, user_):
    working_people = []
    with create_session() as session:
        for human in session.query(record.user_id, func.count(record.user_id)).group_by(record.user_id).filter_by(
                is_registered=True):
            if not human[1] % 2 == 0:
                for user in session.query(user_).filter_by(card_id=human[0]).all():
                    working_people.append("{} {}".format(user.name, user.surname))
        return working_people


def get_user_profile(user, id):
    with create_session() as session:
        return session.query(user).filter(user.id == id).first()


def get_users(user):
    with create_session() as session:
        return session.query(user).all()
