from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


def get_session(config):
    engine = create_engine('mssql+pyodbc://{}:{}@{}/{}?driver={}'.format(config.user, config.password, config.host, config.db, config.driver))
    conn = engine.connect()

    Session = sessionmaker(bind=engine)
    session = Session()

    return session

def get_base():
    return Base