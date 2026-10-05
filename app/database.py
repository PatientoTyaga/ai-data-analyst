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
    
def save_dataset(
    dataset_id: str,
    original_filename: str,
    file_path: str,
    mapping: dict
):
    connection = get_connection()

    connection.execute(
        """
        INSERT OR REPLACE INTO datasets (
            dataset_id,
            original_filename,
            file_path,
            transaction_date,
            revenue,
            region,
            status,
            valid_status,
            cancelled_status
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            dataset_id,
            original_filename,
            file_path,
            mapping["transaction_date"],
            mapping["revenue"],
            mapping["region"],
            mapping["status"],
            mapping["valid_status"],
            mapping["cancelled_status"],
        )
    )

    connection.commit()
    connection.close()
    
def get_dataset(dataset_id: str):
    connection = get_connection()

    row = connection.execute(
        """
        SELECT *
        FROM datasets
        WHERE dataset_id = ?
        """,
        (dataset_id,)
    ).fetchone()

    connection.close()

    if row is None:
        return None

    return {
        "dataset_id": row["dataset_id"],
        "original_filename": row["original_filename"],
        "file_path": row["file_path"],
        "mapping": {
            "transaction_date": row["transaction_date"],
            "revenue": row["revenue"],
            "region": row["region"],
            "status": row["status"],
            "valid_status": row["valid_status"],
            "cancelled_status": row["cancelled_status"],
        }
    }