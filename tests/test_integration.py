import pytest
from fastapi.testclient import TestClient
from app.main import app
from database.db import get_db, SessionLocal
from models.user import User
from app.auth_utils import hash_password

def test_full_auth_flow(client, test_db):
    # 1. Verify user exists in DB (seeded in conftest)
    user = test_db.query(User).filter(User.username == "admin").first()
    assert user is not None
    
    # 2. Attempt login via API
    response = client.post("/api/v1/login", json={"username": "admin", "password": "adminpass"})
    assert response.status_code == 200
    
    # 3. Verify token content
    data = response.json()
    token = data["access_token"]
    assert token is not None
    
    # Optional: decode token if we had a decode utility (not strictly in plan but good)
    from jose import jwt
    import os
    SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkey")
    ALGORITHM = os.getenv("ALGORITHM", "HS256")
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    assert payload["sub"] == "admin"
    assert payload["role"] == "admin"
