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
        admin = db.query(User).filter(User.staff_number == "ADMIN000").first()
        if admin:
            print("Admin user already exists.")
            return

        print("Seeding initial admin user...")
        hashed_pwd = hash_password("admin123")
        admin_user = User(
            username="ADMIN000",
            staff_number="ADMIN000",
            hashed_password=hashed_pwd,
            role="admin",
            full_name="System Admin",
            department="BSTC",
            is_active=True,
            is_approved=True
        )
        db.add(admin_user)
        db.commit()
        print("Admin user created successfully (Staff Number: ADMIN000, password: admin123).")
        print("IMPORTANT: Change the password after first login.")
    except Exception as e:
        print(f"Error seeding admin user: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_admin()
