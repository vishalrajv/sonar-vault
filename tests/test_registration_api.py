from fastapi.testclient import TestClient
from app.main import app
import pytest

client = TestClient(app)

def test_register_user_success():
    """Verify that a user can successfully submit registration."""
    import random
    staff_num = f"BEL{random.randint(10000, 99999)}"
    payload = {
        "staff_number": staff_num,
        "password": "securepassword",
        "full_name": "Test User",
        "department": "D&E",
        "role_designation": "Engineer",
        "dob": "1990-01-01",
        "phone_number": "9876543210",
        "personal_email": "test@personal.com",
        "official_email": "test@bel.co.in"
    }
    response = client.post("/api/v1/register", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["staff_number"] == staff_num
    assert data["is_approved"] is False
    assert data["is_active"] is False

def test_register_duplicate_staff_number():
    """Verify that duplicate staff numbers are rejected."""
    payload = {
        "staff_number": "BEL12345",
        "password": "securepassword",
        "full_name": "Test User 2",
        "department": "BSTC",
        "role_designation": "Manager",
        "dob": "1985-05-05",
        "phone_number": "1234567890",
        "personal_email": "test2@personal.com",
        "official_email": "test2@bel.co.in"
    }
    # First one should succeed (if endpoint exists)
    client.post("/api/v1/register", json=payload)
    # Second one should fail
    response = client.post("/api/v1/register", json=payload)
    assert response.status_code == 400
    assert "already registered" in response.json()["detail"]
