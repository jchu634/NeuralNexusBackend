import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from library import create_app
from library.database import models
from fastapi.testclient import TestClient


@pytest.fixture
def client():
    my_app = create_app(config={
        "ENV_TYPE": "production",
        "IMAGE_DEFAULT_EXPIRY_PERIOD": 5,
        "CACHE_TIMEOUT_PERIOD": 10,
        "AUTH_SECRET_KEY": "570caa4d8df41bd1176dfb267757af96835de1a1381543a680be1f7531fc521c",

        # 'WTF_CSRF_ENABLED': False,                       # test_client will not send a CSRF token, so disable validation.
    }, disable_database=True)

    return TestClient(my_app)


engine = create_engine(
    "sqlite+pysqlite:///:memory:", echo=True, future=True
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
models.Base.metadata.create_all(bind=engine)


@pytest.fixture()
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
