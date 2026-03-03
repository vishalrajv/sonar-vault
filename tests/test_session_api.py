import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.db import get_db
from models.base import Base
from app.main import app
from models.user import User
from app.auth_utils import hash_password
from app.token_utils import SECRET_KEY, ALGORITHM
from jose import jwt
import os

# Test Database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_sessions_shared.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    # We will set this per test
    db = getattr(pytest, "_current_db_session", None)
    if db:
        yield db
    else:
        # Fallback if needed
        pass

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture
def db_session(request):
    """Creates a unique database per test."""
    test_name = request.node.name
    db_file = f"./test_{test_name}.db"
    if os.path.exists(db_file):
        os.remove(db_file)
        
    url = f"sqlite:///{db_file}"
    test_engine = create_engine(url, connect_args={"check_same_thread": False})
    TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)
    Base.metadata.create_all(bind=test_engine)
    
    db = TestSessionLocal()
    # Seed user
    hashed_pwd = hash_password("testpass")
    user = User(username="testuser", hashed_password=hashed_pwd, role="D&E")
    db.add(user)
    db.commit()
    
    pytest._current_db_session = db
    pytest._current_db_local = TestSessionLocal
    
    yield db
    
    db.close()
    test_engine.dispose()
    # Cleanup will be handled by the next test or manually if needed
    # but at least they are unique.

client = TestClient(app)

def test_login_updates_session_id(db_session):
    """Verify that login generates a JTI and updates the user's current_session_id."""
    response = client.post("/api/v1/login", json={"username": "testuser", "password": "testpass"})
    assert response.status_code == 200
    data = response.json()
    token = data["access_token"]
    
    # Decode token to get jti
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    jti = payload.get("jti")
    assert jti is not None
    
    # Check database
    user = db_session.query(User).filter(User.username == "testuser").first()
    assert user.current_session_id == jti

def test_concurrency_second_login_invalidates_first(db_session):
    """Verify that a second login generates a NEW JTI and updates the database."""
    # First login
    resp1 = client.post("/api/v1/login", json={"username": "testuser", "password": "testpass"})
    jti1 = jwt.decode(resp1.json()["access_token"], SECRET_KEY, algorithms=[ALGORITHM]).get("jti")
    
    # Second login
    resp2 = client.post("/api/v1/login", json={"username": "testuser", "password": "testpass"})
    jti2 = jwt.decode(resp2.json()["access_token"], SECRET_KEY, algorithms=[ALGORITHM]).get("jti")
    
    assert jti1 != jti2
    
    # Database should have jti2
    user = db_session.query(User).filter(User.username == "testuser").first()
    assert user.current_session_id == jti2
    assert user.current_session_id != jti1
