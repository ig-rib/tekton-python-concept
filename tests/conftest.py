## Most of the hooks on this file are based on https://www.fastapitutorial.com/blog/unit-testing-in-fastapi/

from typing import Any
from typing import Generator

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import sys
import os


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) 
#this is to include backend dir in sys.path so that we can import from api directory.
from settings import Settings
settings = Settings()
from api.database.database import Base, get_db
from api.database.redis import get_redis_db
from api.routers.healthchecks import healthchecks_router
from api.routers.products import products_router

def start_application():
    app = FastAPI()
    app.include_router(healthchecks_router, prefix="/healthcheck")
    app.include_router(products_router, prefix="/products")
    return app


SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.test_db_user}:{settings.test_db_password}@{settings.test_db_host}:{settings.test_db_port}/{settings.test_db_name}"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionTesting = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def app() -> Generator[FastAPI, Any, None]:
    """
    Create a fresh database on each test case.
    """
    Base.metadata.create_all(engine)  # Create the tables.
    _app = start_application()
    yield _app
    Base.metadata.drop_all(engine)


@pytest.fixture(scope="function")
def db_session(app: FastAPI) -> Generator[SessionTesting, Any, None]:
    connection = engine.connect()
    transaction = connection.begin()
    session = SessionTesting(bind=connection)
    yield session  # use the session in tests.
    session.close()
    transaction.rollback()
    connection.close()

class RedisMockConnection:
    def __init__(self):
        self.dict = {}
    def hmset(self, key, value):
        self.dict[key] = value
    def hmget(self, key, keys):
        if key not in self.dict: return [None]
        return [self.dict[key].get(_k) for _k in keys]
    def expire(self, key, time):
        return None
    def set(self, key, value, ex=None):
        self.dict[key] = value
    def get(self, key):
        return self.dict.get(key, None)

@pytest.fixture(scope="function")
def mock_cache(app: FastAPI) -> Generator[SessionTesting, Any, None]:
    cache = RedisMockConnection()
    yield cache

@pytest.fixture(scope="function")
def client(
    app: FastAPI, db_session: SessionTesting, mock_cache: RedisMockConnection
) -> Generator[TestClient, Any, None]:
    """
    Create a new FastAPI TestClient that uses the `db_session` fixture to override
    the `get_db` dependency that is injected into routes.
    """

    def _get_test_db():
        try:
            yield db_session
        finally:
            pass

    def _get_redis_db():
        try:
            yield mock_cache
        finally:
            pass

    app.dependency_overrides[get_db] = _get_test_db
    app.dependency_overrides[get_redis_db] = _get_redis_db
    with TestClient(app) as client:
        yield client