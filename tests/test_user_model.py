import pytest
from sqlalchemy import Column, Integer, String, Boolean
from models.base import Base
from models.user import User

def test_user_model_structure():
    user = User(
        username="testadmin",
        hashed_password="hashed_password_here",
        role="admin",
        is_active=True
    )
    assert user.username == "testadmin"
    assert user.role == "admin"
    assert user.is_active is True
    assert hasattr(user, "id")
