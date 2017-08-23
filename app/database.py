from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager

DATABASE_URI = 'sqlite:///database.db'

Base = declarative_base()
engine = create_engine(DATABASE_URI, echo=True)
Session = sessionmaker(bind=engine)


@contextmanager
def create_session(engine=engine):
    session = Session(bind=engine)
    try:
        yield session
    finally:
        session.commit()


def init_db():
    import models
    models.Base.metadata.bind = engine
    models.Base.metadata.create_all()

