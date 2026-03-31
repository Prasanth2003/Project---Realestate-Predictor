import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'real_estate.db')

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            price REAL,
            location TEXT,
            size REAL,
            income REAL,
            amenities TEXT,
            likelihood TEXT,
            probability REAL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def save_prediction(price, location, size, income, amenities, likelihood, probability):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO predictions (price, location, size, income, amenities, likelihood, probability)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (price, location, size, income, amenities, likelihood, probability))
    conn.commit()
    conn.close()

def get_history():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM predictions ORDER BY created_at DESC')
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]
