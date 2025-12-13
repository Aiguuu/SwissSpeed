import sqlite3
from typing import List, Dict

class DBHandler:
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self.create_table()

    def create_table(self):
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

    def insert_records(self, records: List[Dict]) -> int:
        inserted = 0
        cursor = self.conn.cursor()

        for record in records:
            values = (
                record["Location"],
                record["Timestamp"],
                record["LightFlow"],
                record["HeavyFlow"],
                record["LightSpeed"],
                record["HeavySpeed"],
                record["Error"]
            )

            cursor.execute("""
                INSERT OR IGNORE INTO SwissSpeed
                (Location, Timestamp, LightFlow, HeavyFlow, LightSpeed, HeavySpeed, Error)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, values)

        self.conn.commit()
        return inserted

    def fetch_all(self):
        return self.conn.execute("SELECT * FROM SwissSpeed").fetchall()

    def close(self):
        self.conn.close()
