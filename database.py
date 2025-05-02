# database.py
import sqlite3

DATABASE_FILE = 'flashcards_log.db'

def get_db_connection():
    """Get a connection to the SQLite database with row factory"""
    conn = sqlite3.connect(DATABASE_FILE)
    conn.row_factory = sqlite3.Row
    return conn