import sys
import os

# Add root to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from database.db import SessionLocal, engine
from models.base import Base
from models.user import User
from app.auth_utils import hash_password

def seed_admin():
    print("Initializing database...")
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        # Check if admin already exists
        admin = db.query(User).filter(User.username == "admin").first()
        if admin:
            print("Admin user already exists.")
            return

        print("Seeding initial admin user...")
        hashed_pwd = hash_password("admin123")
        admin_user = User(
            username="admin",
            hashed_password=hashed_pwd,
            role="admin",
            is_active=True
        )
        db.add(admin_user)
        db.commit()
        print("Admin user created successfully (username: admin, password: admin123).")
        print("IMPORTANT: Change the password after first login.")
    except Exception as e:
        print(f"Error seeding admin user: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_admin()
