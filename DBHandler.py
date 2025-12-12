import sqlite3
from typing import List, Dict

class DBHandler:
    def __init__(self, db_path: str = "SwissSpeed.db"):
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path)
        self.create_table()

    def create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS SwissSpeed (
            Location TEXT,
            Timestamp TEXT,
            LightFlow INTEGER,
            HeavyFlow INTEGER,
            LightSpeed INTEGER,
            HeavySpeed INTEGER,
            Error TEXT
        );
        """
        self.conn.execute(query)
        self.conn.commit()

    def insert_records(self, records: List[Dict]):
        query = """
        INSERT INTO SwissSpeed 
        (Location, Timestamp, LightFlow, HeavyFlow, LightSpeed, HeavySpeed, Error)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        data_to_insert = [
            (
                rec.get("Location"),
                rec.get("Timestamp"),
                rec.get("LightFlow"),
                rec.get("HeavyFlow"),
                rec.get("LightSpeed"),
                rec.get("HeavySpeed"),
                rec.get("Error")
            )
            for rec in records
        ]
        self.conn.executemany(query, data_to_insert)
        self.conn.commit()

    def fetch_all(self) -> List[Dict]:
        cursor = self.conn.execute("SELECT * FROM SwissSpeed")
        cols = [desc[0] for desc in cursor.description]
        return [dict(zip(cols, row)) for row in cursor.fetchall()]

    def close(self):
        self.conn.close()


# ==========================
# MAIN FOR TESTING
# ==========================
if __name__ == "__main__":
    print("=== DBHandler Test ===")

    try:
        db = DBHandler("test_SwissSpeed.db")
        print("✅ Table created successfully")

        # Insert dummy data
        sample_records = [
            {
                "Location": "CH:0677.01",
                "Timestamp": "2024-09-20T09:59:00Z",
                "LightFlow": 1200,
                "HeavyFlow": 60,
                "LightSpeed": 76,
                "HeavySpeed": 67,
                "Error": None
            }
        ]
        db.insert_records(sample_records)
        print("✅ Sample record inserted")

        all_data = db.fetch_all()
        print(f"✅ Fetched {len(all_data)} records from DB")
        print("Sample from DB:", all_data[:1])

    except Exception as e:
        print("❌ DBHandler test failed:", e)
    finally:
        db.close()

