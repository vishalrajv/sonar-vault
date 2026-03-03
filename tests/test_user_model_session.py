from sqlalchemy.orm import Session
from models.user import User
from models.base import Base
from database.db import engine

def test_user_model_has_session_id():
    """Verify that the User model has the current_session_id field."""
    user = User(username="testuser", hashed_password="hashed", role="D&E", current_session_id="test-jti")
    assert hasattr(user, 'current_session_id')
    assert user.current_session_id == "test-jti"

def test_user_model_session_id_nullable():
    """Verify that current_session_id can be null."""
    user = User(username="testuser2", hashed_password="hashed", role="Testing")
    assert user.current_session_id is None
