import sqlite3
import os

def test_db_schema():
    db_path = "sonar_vault.db"
    assert os.path.exists(db_path)

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("PRAGMA table_info(users)")
    columns = {row[1] for row in cursor.fetchall()}
    
    required_columns = {
        "staff_number", "full_name", "department", "role_designation", 
        "dob", "phone_number", "personal_email", "official_email", "is_approved"
    }
    
    for col in required_columns:
        assert col in columns, f"Column {col} missing from users table"
    
    conn.close()
    print("Schema verification passed.")

if __name__ == "__main__":
    test_db_schema()
