import sqlite3
import os

def migrate():
    db_path = "sonar_vault.db"
    if not os.path.exists(db_path):
        print(f"Database {db_path} not found. Skipping migration.")
        return

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    new_columns = [
        ("staff_number", "TEXT"),
        ("full_name", "TEXT"),
        ("department", "TEXT"),
        ("role_designation", "TEXT"),
        ("dob", "TEXT"),
        ("phone_number", "TEXT"),
        ("personal_email", "TEXT"),
        ("official_email", "TEXT"),
        ("is_approved", "BOOLEAN DEFAULT 0")
    ]

    for col_name, col_type in new_columns:
        try:
            cursor.execute(f"ALTER TABLE users ADD COLUMN {col_name} {col_type}")
            print(f"Added column {col_name}")
        except sqlite3.OperationalError as e:
            if "duplicate column name" in str(e):
                print(f"Column {col_name} already exists.")
            else:
                raise e

    # For existing users, set staff_number to username if null
    cursor.execute("UPDATE users SET staff_number = username WHERE staff_number IS NULL")
    # For existing users, set is_approved to 1 (True)
    cursor.execute("UPDATE users SET is_approved = 1 WHERE is_approved IS NULL")
    # Also set is_active to True for existing users (since they were active before)
    cursor.execute("UPDATE users SET is_active = 1 WHERE is_active IS NULL")

    # Create index for staff_number
    try:
        cursor.execute("CREATE UNIQUE INDEX IF NOT EXISTS idx_users_staff_number ON users(staff_number)")
        print("Created unique index on staff_number")
    except Exception as e:
        print(f"Error creating index: {e}")

    conn.commit()
    conn.close()
    print("Migration complete.")

if __name__ == "__main__":
    migrate()
