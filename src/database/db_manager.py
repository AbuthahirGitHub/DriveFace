import sqlite3
from pathlib import Path

class DatabaseManager:
    def __init__(self):
        self.db_path = Path('data/driveface.db')
        self.db_path.parent.mkdir(exist_ok=True)
        self.conn = sqlite3.connect(str(self.db_path))
        self.create_tables()
    
    def create_tables(self):
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS images (
                id INTEGER PRIMARY KEY,
                path TEXT NOT NULL,
                thumbnail_path TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS faces (
                id INTEGER PRIMARY KEY,
                image_id INTEGER,
                name TEXT,
                embedding BLOB,
                FOREIGN KEY (image_id) REFERENCES images (id)
            )
        ''')
        self.conn.commit() 