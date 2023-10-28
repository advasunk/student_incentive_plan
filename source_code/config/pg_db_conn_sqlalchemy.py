from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from . import config

DATABASE_HOST = config.get_property('PG_DB_HOST')
DATABASE_PORT = config.get_property('PG_DB_PORT')
DATABASE_NAME = config.get_property('PG_DB_NAME')
DATABASE_USERNAME = config.get_property('PG_DB_USER')
DATABASE_PASSWORD = config.get_property('PG_DB_PASSWORD')

# SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
SQLALCHEMY_DATABASE_URL = f"postgresql://{DATABASE_USERNAME}:{DATABASE_PASSWORD}@{DATABASE_HOST}/{DATABASE_NAME}"

# print(SQLALCHEMY_DATABASE_URL)

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def db_session() -> Generator:
    try:
        db = SessionLocal()
        yield db
        db.commit()
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()
