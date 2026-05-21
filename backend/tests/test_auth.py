import pytest


def test_register_success(client, db):
    """Test successful user registration."""
    user_data = {"username": "newuser", "email": "new@example.com", "password": "pass123"}
    response = client.post("/auth/register", json=user_data)
    
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == user_data["username"]
    assert data["email"] == user_data["email"]
    assert "id" in data
    assert "created_at" in data


def test_register_duplicate_username(client, db, registered_user):
    """Test registration with duplicate username."""
    user_data = {
        "username": registered_user["username"],
        "email": "different@example.com",
        "password": "pass123",
    }
    response = client.post("/auth/register", json=user_data)
    
    assert response.status_code == 400
    assert "already taken" in response.json()["detail"]


def test_register_duplicate_email(client, db, registered_user):
    """Test registration with duplicate email."""
    user_data = {
        "username": "differentuser",
        "email": registered_user["email"],
        "password": "pass123",
    }
    response = client.post("/auth/register", json=user_data)
    
    assert response.status_code == 400
    assert "already registered" in response.json()["detail"]


def test_login_success(client, db, registered_user):
    """Test successful login."""
    login_data = {"username": registered_user["username"], "password": registered_user["password"]}
    response = client.post("/auth/login", json=login_data)
    
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_wrong_password(client, db, registered_user):
    """Test login with wrong password."""
    login_data = {"username": registered_user["username"], "password": "wrongpassword"}
    response = client.post("/auth/login", json=login_data)
    
    assert response.status_code == 401
    assert "Invalid credentials" in response.json()["detail"]


def test_login_nonexistent_user(client, db):
    """Test login with nonexistent user."""
    login_data = {"username": "nonexistent", "password": "pass123"}
    response = client.post("/auth/login", json=login_data)
    
    assert response.status_code == 401
    assert "Invalid credentials" in response.json()["detail"]
