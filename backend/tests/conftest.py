import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

from app.database import Base
from app.main import app
from app.core.dependencies import get_db


# Use in-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="function")
def db():
    """Create a fresh database for each test."""
    Base.metadata.create_all(bind=engine)
    yield TestingSessionLocal()
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client():
    """Create a test client."""
    return TestClient(app)


@pytest.fixture(scope="function")
def registered_user(client):
    """Register a test user and return user info with token."""
    user_data = {"username": "testuser", "email": "test@example.com", "password": "testpass123"}
    
    # Register user
    response = client.post("/auth/register", json=user_data)
    assert response.status_code == 201
    
    # Login user
    login_data = {"username": user_data["username"], "password": user_data["password"]}
    response = client.post("/auth/login", json=login_data)
    assert response.status_code == 200
    token = response.json()["access_token"]
    
    return {
        "username": user_data["username"],
        "email": user_data["email"],
        "password": user_data["password"],
        "token": token,
    }
