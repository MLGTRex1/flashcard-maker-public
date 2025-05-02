"""
Create a users table and update existing tables to track user ownership
Save this as database_user_update.py
"""
import sqlite3
import os

DATABASE_FILE = 'flashcards_log.db'

def update_database_for_users():
    print("Updating database to support multiple users...")
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()

    # Create users table if it doesn't exist
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_code TEXT UNIQUE NOT NULL,
        username TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    print("Users table created.")

    # Check if user_id column exists in generated_cards table
    cursor.execute("PRAGMA table_info(generated_cards)")
    columns = cursor.fetchall()
    column_names = [column[1] for column in columns]

    # Add user_id column to generated_cards if it doesn't exist
    if 'user_id' not in column_names:
        print("Adding user_id column to generated_cards table...")
        cursor.execute('''
        ALTER TABLE generated_cards 
        ADD COLUMN user_id INTEGER DEFAULT NULL
        ''')
        print("Column added successfully!")

    # Check if user_id column exists in processing_history table
    cursor.execute("PRAGMA table_info(processing_history)")
    columns = cursor.fetchall()
    column_names = [column[1] for column in columns]

    # Add user_id column to processing_history if it doesn't exist
    if 'user_id' not in column_names:
        print("Adding user_id column to processing_history table...")
        cursor.execute('''
        ALTER TABLE processing_history 
        ADD COLUMN user_id INTEGER DEFAULT NULL
        ''')
        print("Column added successfully!")

    # Create indexes for performance
    cursor.execute('''
    CREATE INDEX IF NOT EXISTS idx_cards_user_id ON generated_cards(user_id)
    ''')
    cursor.execute('''
    CREATE INDEX IF NOT EXISTS idx_history_user_id ON processing_history(user_id)
    ''')
    
    print("Database indexes created.")

    # Add initial admin user if none exists
    cursor.execute("SELECT COUNT(*) FROM users")
    user_count = cursor.fetchone()[0]
    
    if user_count == 0:
        import uuid
        admin_code = str(uuid.uuid4())[:8]  # Generate a short UUID
        cursor.execute('''
        INSERT INTO users (user_code, username) VALUES (?, ?)
        ''', (admin_code, 'Admin'))
        print(f"Created initial admin user with code: {admin_code}")
        print("IMPORTANT: Save this code! You'll need it to log in as admin.")
    
    conn.commit()
    conn.close()
    print("Database update for users completed!")

if __name__ == "__main__":
    update_database_for_users()