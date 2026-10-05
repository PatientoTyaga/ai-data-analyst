import sqlite3
from pathlib import Path


DATABASE_PATH = Path("data/app.db")


def get_connection():
    DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row

    return connection

def initialize_database():
    connection = get_connection()

    connection.execute("""
        CREATE TABLE IF NOT EXISTS datasets (
            dataset_id TEXT PRIMARY KEY,
            original_filename TEXT NOT NULL,
            file_path TEXT NOT NULL,
            transaction_date TEXT NOT NULL,
            revenue TEXT NOT NULL,
            region TEXT NOT NULL,
            status TEXT NOT NULL,
            valid_status TEXT NOT NULL,
            cancelled_status TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    connection.commit()
    connection.close()