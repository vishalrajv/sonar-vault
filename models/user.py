from sqlalchemy import Column, Integer, String, Boolean
from models.base import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False) # This will be the Staff Number for Login
    staff_number = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    
    full_name = Column(String, nullable=True)
    department = Column(String, nullable=True)
    role_designation = Column(String, nullable=True)
    dob = Column(String, nullable=True)
    phone_number = Column(String, nullable=True)
    personal_email = Column(String, nullable=True)
    official_email = Column(String, nullable=True)
    
    role = Column(String, default="user") # 'user' or 'admin'
    is_active = Column(Boolean, default=False) # Only active after approval
    is_approved = Column(Boolean, default=False)
    current_session_id = Column(String, nullable=True)

    def __repr__(self):
        return f"<User(username='{self.username}', staff_number='{self.staff_number}', role='{self.role}')>"
