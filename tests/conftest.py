import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.db import get_db
from models.base import Base
from app.main import app
from models.user import User
from app.auth_utils import hash_password

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class SessionManager:
    db = None

@pytest.fixture(scope="module")
def test_db():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    SessionManager.db = db
    try:
        # Seed an admin user
        hashed_pwd = hash_password("adminpass")
        admin = User(
            username="admin", 
            staff_number="ADMIN000", 
            hashed_password=hashed_pwd, 
            role="admin",
            is_active=True,
            is_approved=True
        )
        db.add(admin)
        db.commit()
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="module")
def client(test_db):
    def override_get_db():
        yield SessionManager.db
    
    app.dependency_overrides[get_db] = override_get_db
    from fastapi.testclient import TestClient
    yield TestClient(app)
    del app.dependency_overrides[get_db]
