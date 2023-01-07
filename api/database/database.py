from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "postgresql://test_user:test_password@concept-db:5432/concept_db"


engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

import typing as t

from sqlalchemy.ext.declarative import as_declarative, declared_attr


class_registry: t.Dict = {}


Base = declarative_base()

def get_db() -> t.Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


import logging

logging.basicConfig()
logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)