import sqlite3
from typing import List, Dict

#-------------------------------------------------------------------------------------------------------
# Role: Manages the SQLite database operations.
# Key Functions: Inserts parsed data into the database, updates records, and retrieves data.
#-------------------------------------------------------------------------------------------------------
    
class DBHandler:
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self.create_table()

    def create_table(self):
        """
        Create the SwissSpeed table if it doesn't exist yet.
        """
        self.conn.execute("""
        CREATE TABLE IF NOT EXISTS SwissSpeed (
            Location TEXT NOT NULL,
            Timestamp TEXT NOT NULL,
            LightFlow INTEGER,
            HeavyFlow INTEGER,
            LightSpeed INTEGER,
            HeavySpeed INTEGER,
            Error TEXT,
            UNIQUE(Location, Timestamp)
        )
        """)
        self.conn.commit()
        print(f"Table SwissSpeed ready in DB {self.db_path}")

    def insert_records(self, records: List[Dict]) -> int:
        """
        Insert multiple records into the SwissSpeed table.
        Uses INSERT OR IGNORE to avoid duplicates based on Location+Timestamp.
        Returns the number of newly inserted rows.
        """
        cursor = self.conn.cursor()
        inserted = 0

        for record in records:
            values = (
                record.get("Location"),
                record.get("Timestamp"),
                record.get("LightFlow"),
                record.get("HeavyFlow"),
                record.get("LightSpeed"),
                record.get("HeavySpeed"),
                record.get("Error")
            )
            cursor.execute("""
                INSERT OR IGNORE INTO SwissSpeed
                (Location, Timestamp, LightFlow, HeavyFlow, LightSpeed, HeavySpeed, Error)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, values)

            # Check if the row was actually inserted
            if cursor.rowcount > 0:
                inserted += 1

        self.conn.commit()
        return inserted

    def fetch_all(self):
        """
        Fetch all rows from the SwissSpeed table.
        """
        return self.conn.execute("SELECT * FROM SwissSpeed").fetchall()

    def close(self):
        """
        Close the database connection cleanly.
        """
        self.conn.close()
        print(f"Connection to {self.db_path} closed")

