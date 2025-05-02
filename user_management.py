"""
user_management.py - User authentication and management functions

This module contains functions for managing users in the flashcard application.
It handles user creation, authentication, and retrieval.
"""
import sqlite3
import uuid
import os

# Use the same database file as the main application
DATABASE_FILE = 'flashcards_log.db'

def check_admin_user_exists():
    """Check if admin user exists and print status information"""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # Check users table
        cursor.execute("SELECT COUNT(*) FROM users")
        user_count = cursor.fetchone()[0]
        
        # Check for user with ID 1
        cursor.execute("SELECT * FROM users WHERE id = 1")
        admin_user = cursor.fetchone()
        
        if admin_user:
            admin_data = dict(admin_user)
            print(f"Admin user found: ID={admin_data.get('id')}, Username={admin_data.get('username')}, Code={admin_data.get('user_code')}")
            return True
        else:
            print(f"No admin user found with ID 1. Total users in database: {user_count}")
            
            # If there are users but none with ID 1, print the first user
            if user_count > 0:
                cursor.execute("SELECT * FROM users LIMIT 1")
                first_user = cursor.fetchone()
                if first_user:
                    first_user_data = dict(first_user)
                    print(f"First user in database: ID={first_user_data.get('id')}, Username={first_user_data.get('username')}")
            
            return False
    except sqlite3.Error as e:
        print(f"Database error checking admin user: {e}")
        return False
    finally:
        conn.close()

def create_admin_user():
    """Create or reset the admin user"""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # Generate admin code
        admin_code = generate_user_code()
        
        # Check if admin user exists
        cursor.execute("SELECT id FROM users WHERE id = 1")
        admin_exists = cursor.fetchone()
        
        if admin_exists:
            # Update existing admin
            cursor.execute('UPDATE users SET user_code = ?, username = ? WHERE id = 1',
                         (admin_code, 'Admin'))
            print(f"Admin user updated with new code: {admin_code}")
        else:
            # Create new admin, forcing ID to be 1
            cursor.execute('INSERT INTO users (id, user_code, username) VALUES (1, ?, ?)',
                         (admin_code, 'Admin'))
            print(f"New admin user created with code: {admin_code}")
        
        conn.commit()
        return admin_code
    except sqlite3.Error as e:
        print(f"Database error creating admin user: {e}")
        conn.rollback()
        return None
    finally:
        conn.close()

def get_db_connection():
    """Get a connection to the SQLite database with row factory"""
    conn = sqlite3.connect(DATABASE_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def create_user(user_code, username):
    """Create a new user with the given code and username"""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('INSERT INTO users (user_code, username) VALUES (?, ?)',
                      (user_code, username))
        conn.commit()
        user_id = cursor.lastrowid
        print(f"Created new user: {username} (ID: {user_id}, Code: {user_code})")
        return user_id
    except sqlite3.IntegrityError:
        print(f"User code '{user_code}' already exists")
        return None
    except sqlite3.Error as e:
        print(f"Database error creating user: {e}")
        conn.rollback()
        return None
    finally:
        conn.close()

def get_user_by_code(user_code):
    """Get user information by their access code"""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('SELECT id, user_code, username FROM users WHERE user_code = ?', 
                      (user_code,))
        user = cursor.fetchone()
        return dict(user) if user else None
    except sqlite3.Error as e:
        print(f"Database error retrieving user: {e}")
        return None
    finally:
        conn.close()

def get_user_by_id(user_id):
    """Get user information by their ID"""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('SELECT id, user_code, username FROM users WHERE id = ?', 
                      (user_id,))
        user = cursor.fetchone()
        return dict(user) if user else None
    except sqlite3.Error as e:
        print(f"Database error retrieving user: {e}")
        return None
    finally:
        conn.close()

def list_users():
    """Get a list of all users"""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('SELECT id, user_code, username FROM users ORDER BY username')
        users = [dict(row) for row in cursor.fetchall()]
        return users
    except sqlite3.Error as e:
        print(f"Database error listing users: {e}")
        return []
    finally:
        conn.close()

def generate_user_code():
    """Generate a unique user code"""
    return str(uuid.uuid4())[:8].upper()  # 8-character uppercase code

def update_database_for_users():
    """Update the database schema to support multiple users"""
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
        admin_code = generate_user_code()
        cursor.execute('''
        INSERT INTO users (user_code, username) VALUES (?, ?)
        ''', (admin_code, 'Admin'))
        print(f"Created initial admin user with code: {admin_code}")
        print("IMPORTANT: Save this code! You'll need it to log in as admin.")
    
    conn.commit()
    conn.close()
    print("Database update for users completed!")

# Run the database update if this script is executed directly
if __name__ == "__main__":
    update_database_for_users()