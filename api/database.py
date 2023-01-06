from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

SQLALCHEMY_DATABASE_URL = f"postgresql://test_user:test_password@db:5432/concept_db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

import typing as t

from sqlalchemy.ext.declarative import as_declarative, declared_attr


class_registry: t.Dict = {}


@as_declarative(class_registry=class_registry)
class Base:
    id: t.Any
    __name__: str

    # Generate __tablename__ automatically
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()