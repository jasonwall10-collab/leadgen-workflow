import sqlite3
import json
from datetime import datetime

def init_db(db_path='data/leads.db'):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Businesses Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS businesses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            location TEXT,
            website_url TEXT,
            status TEXT DEFAULT 'pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Jobs Table (State Machine)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS jobs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            business_id INTEGER,
            stage TEXT NOT NULL, 
            status TEXT DEFAULT 'idle', -- idle, processing, completed, failed, awaiting_approval
            data_json TEXT, -- All structured output for this stage
            last_error TEXT,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (business_id) REFERENCES businesses(id)
        )
    ''')
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    print("Database initialized.")