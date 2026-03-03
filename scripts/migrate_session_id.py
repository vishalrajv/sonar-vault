import os
from sqlalchemy import text
from database.db import engine

def migrate():
    print("Starting migration: Adding current_session_id to users table...")
    try:
        with engine.connect() as conn:
            # Check if column already exists
            result = conn.execute(text("PRAGMA table_info(users)"))
            columns = [row[1] for row in result]
            
            if 'current_session_id' in columns:
                print("Column 'current_session_id' already exists in table 'users'.")
                return

            print("Adding column 'current_session_id' to table 'users'...")
            conn.execute(text("ALTER TABLE users ADD COLUMN current_session_id TEXT;"))
            conn.commit()
            print("Migration successful.")
    except Exception as e:
        print(f"Error during migration: {e}")

if __name__ == "__main__":
    migrate()
