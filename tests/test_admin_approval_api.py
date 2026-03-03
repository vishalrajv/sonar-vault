from fastapi.testclient import TestClient
from app.main import app
import pytest
from models.user import User
from app.auth_utils import hash_password

client = TestClient(app)

@pytest.fixture
def admin_token(client, test_db):
    # Ensure an admin user exists
    admin = test_db.query(User).filter(User.username == "admin_test").first()
    if not admin:
        admin = User(
            username="admin_test",
            staff_number="ADMIN001",
            hashed_password=hash_password("adminpass"),
            role="admin",
            is_active=True,
            is_approved=True
        )
        test_db.add(admin)
        test_db.commit()
    
    response = client.post(
        "/api/v1/login",
        json={"username": "admin_test", "password": "adminpass"}
    )
    return response.json()["access_token"]

@pytest.fixture
def user_token(client, test_db):
    # Ensure a regular user exists
    user = test_db.query(User).filter(User.username == "user_test").first()
    if not user:
        user = User(
            username="user_test",
            staff_number="USER001",
            hashed_password=hash_password("userpass"),
            role="user",
            is_active=True,
            is_approved=True
        )
        test_db.add(user)
        test_db.commit()
    
    response = client.post(
        "/api/v1/login",
        json={"username": "user_test", "password": "userpass"}
    )
    return response.json()["access_token"]

def test_get_pending_users_admin_only(admin_token, user_token):
    # Admin should succeed
    response = client.get(
        "/api/v1/admin/pending-users",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200
    
    # Regular user should fail
    response = client.get(
        "/api/v1/admin/pending-users",
        headers={"Authorization": f"Bearer {user_token}"}
    )
    assert response.status_code == 403

def test_approve_user_workflow(admin_token, test_db):
    # 1. Register a new user
    payload = {
        "staff_number": "PENDING001",
        "password": "password",
        "full_name": "Pending User",
        "department": "D&E",
        "role_designation": "Engineer",
        "dob": "1990-01-01",
        "phone_number": "000",
        "personal_email": "p@p.com",
        "official_email": "p@bel.co.in"
    }
    client.post("/api/v1/register", json=payload)
    
    user = test_db.query(User).filter(User.staff_number == "PENDING001").first()
    assert user.is_approved is False
    
    # 2. Approve the user
    response = client.post(
        f"/api/v1/admin/approve-user/{user.id}",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200
    
    # 3. Verify status
    test_db.refresh(user)
    assert user.is_approved is True
    assert user.is_active is True
