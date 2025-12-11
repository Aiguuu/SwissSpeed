# Inserts data ONLY into the database "SwissSpeed.db" in it's current state, to be found this repository.
# Shows the all th stored data in the terminal afterwards.
# Note: if you want to change the table of the databank, you will have to adapt the function "insert_sample_data".

import sqlite3

# Function to connect to the SQLite Database
def get_db_connection(db_name='SwissSpeed.db'):
    conn = sqlite3.connect(db_name)
    conn.row_factory = sqlite3.Row
    return conn

# Function to write data in the SQLite Database
def insert_sample_data():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO SwissSpeed (id, plate, location, speed)
        VALUES (?, ?, ?, ?)
    """, (1, 2356, 404, 254))
    conn.commit()
    conn.close()

# Function to fetch data from the SQLite Database
def fetch_all_data():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM SwissSpeed")
    data = cursor.fetchall()
    conn.close()
    return data

# Small code to test the functions
if __name__ == "__main__":
    # First, we try to write
    insert_sample_data()
    print("Data successfully written ! Here is what the database contains :")
    # Then, we show what's in the database in the terminal
    for row in fetch_all_data():
        print(dict(row)) 
