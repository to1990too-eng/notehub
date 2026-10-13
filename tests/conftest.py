import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base, get_db
from app.main import app

SQLALCHEMY_DATABASE_URL = "sqlite://"

@pytest.fixture
def client():
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    TestingSession = sessionmaker(bind=engine, autoflush=False)
    Base.metadata.create_all(bind=engine)

    def override_get_db():
        db = TestingSession()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()

@pytest.fixture
def auth_client(client):
    client.post("/api/v1/auth/register", json={
        "email": "test@example.com",
        "username": "tester",
        "password": "supersecret",
    })
    r = client.post("/api/v1/auth/login", data={
        "username": "test@example.com",
        "password": "supersecret",
    })
    token = r.json()["access_token"]
    client.headers.update({"Authorization": f"Bearer {token}"})
    return client