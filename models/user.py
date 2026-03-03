from sqlalchemy import Column, Integer, String, Boolean
from models.base import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, default="user")
    is_active = Column(Boolean, default=True)
    current_session_id = Column(String, nullable=True)

    def __repr__(self):
        return f"<User(username='{self.username}', role='{self.role}')>"
