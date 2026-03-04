import pytest
from app.token_utils import SECRET_KEY, ALGORITHM
from jose import jwt
from models.user import User
from app.auth_utils import hash_password

def test_login_updates_session_id(client, test_db):
    """Verify that login generates a JTI and updates the user's current_session_id."""
    # Seed user
    user = User(
        username="BEL001", 
        staff_number="BEL001",
        hashed_password=hash_password("testpass"), 
        role="user",
        is_approved=True,
        is_active=True
    )
    test_db.add(user)
    test_db.commit()

    response = client.post("/api/v1/login", json={"username": "BEL001", "password": "testpass"})
    assert response.status_code == 200
    data = response.json()
    token = data["access_token"]
    
    # Decode token to get jti
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    jti = payload.get("jti")
    assert jti is not None
    
    # Check database
    test_db.refresh(user)
    assert user.current_session_id == jti

def test_concurrency_second_login_invalidates_first(client, test_db):
    """Verify that a second login generates a NEW JTI and updates the database."""
    # First login
    resp1 = client.post("/api/v1/login", json={"username": "BEL001", "password": "testpass"})
    jti1 = jwt.decode(resp1.json()["access_token"], SECRET_KEY, algorithms=[ALGORITHM]).get("jti")
    
    # Second login
    resp2 = client.post("/api/v1/login", json={"username": "BEL001", "password": "testpass"})
    jti2 = jwt.decode(resp2.json()["access_token"], SECRET_KEY, algorithms=[ALGORITHM]).get("jti")
    
    assert jti1 != jti2
    
    # Database should have jti2
    user = test_db.query(User).filter(User.username == "BEL001").first()
    assert user.current_session_id == jti2
    assert user.current_session_id != jti1

def test_logout_clears_session_id(client, test_db):
    """Verify that logout clears the user's current_session_id."""
    # Login
    resp = client.post("/api/v1/login", json={"username": "BEL001", "password": "testpass"})
    token = resp.json()["access_token"]
    
    # Logout
    logout_resp = client.post("/api/v1/logout", headers={"Authorization": f"Bearer {token}"})
    assert logout_resp.status_code == 200
    
    # Check database
    user = test_db.query(User).filter(User.username == "BEL001").first()
    assert user.current_session_id is None

def test_session_status_valid(client, test_db):
    """Verify that /session/status returns 200 for a valid session."""
    # Login
    resp = client.post("/api/v1/login", json={"username": "BEL001", "password": "testpass"})
    token = resp.json()["access_token"]
    
    # Check status
    status_resp = client.get("/api/v1/session/status", headers={"Authorization": f"Bearer {token}"})
    assert status_resp.status_code == 200
    assert status_resp.json()["username"] == "BEL001"

def test_session_status_invalidated_by_concurrent_login(client, test_db):
    """Verify that an old token is rejected after a new login occurs."""
    # First login
    resp1 = client.post("/api/v1/login", json={"username": "BEL001", "password": "testpass"})
    token1 = resp1.json()["access_token"]
    
    # Second login
    client.post("/api/v1/login", json={"username": "BEL001", "password": "testpass"})
    
    # Check status with first token
    status_resp = client.get("/api/v1/session/status", headers={"Authorization": f"Bearer {token1}"})
    assert status_resp.status_code == 401
    assert "session invalidated" in status_resp.json()["detail"].lower()

def test_login_remember_me_expiration(client, test_db):
    """Verify that login with remember_me=True produces a long-lived token."""
    # Login with remember_me=True
    response = client.post("/api/v1/login", json={"username": "BEL001", "password": "testpass", "remember_me": True})
    assert response.status_code == 200
    token = response.json()["access_token"]
    
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    exp = payload.get("exp")
    
    # Login without remember_me
    response_std = client.post("/api/v1/login", json={"username": "BEL001", "password": "testpass", "remember_me": False})
    token_std = response_std.json()["access_token"]
    payload_std = jwt.decode(token_std, SECRET_KEY, algorithms=[ALGORITHM])
    exp_std = payload_std.get("exp")
    
    # Long-lived should be significantly later than standard
    assert exp > exp_std

def test_dashboard_shell_accessible(client):
    """Verify that /dashboard shell is accessible (auth handled via JS)."""
    resp = client.get("/dashboard")
    assert resp.status_code == 200
