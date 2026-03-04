from fastapi.testclient import TestClient
import pytest
from app.main import app
from models.user import User
from database.db import SessionLocal

def test_login_with_staff_number_success(client, test_db):
    # Setup: Create an approved user
    from app.auth_utils import hash_password
    user = User(
        staff_number="BEL123",
        username="testuser",
        hashed_password=hash_password("testpass"),
        full_name="Test User",
        department="D&E",
        is_approved=True,
        is_active=True
    )
    test_db.add(user)
    test_db.commit()

    response = client.post("/api/v1/login", json={"username": "BEL123", "password": "testpass"})
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_login_unapproved_user_fails(client, test_db):
    # Setup: Create an unapproved user
    from app.auth_utils import hash_password
    user = User(
        staff_number="BEL456",
        username="unapproved",
        hashed_password=hash_password("testpass"),
        full_name="Unapproved User",
        department="BSTC",
        is_approved=False,
        is_active=False
    )
    test_db.add(user)
    test_db.commit()

    response = client.post("/api/v1/login", json={"username": "BEL456", "password": "testpass"})
    assert response.status_code == 401
    assert response.json()["detail"] == "Account pending approval"

def test_login_non_existent_staff_number(client):
    response = client.post("/api/v1/login", json={"username": "NONEXISTENT", "password": "pwd"})
    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect staff number or password"
