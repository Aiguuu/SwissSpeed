from Collector import Collector
from SoapClient import SoapClient
from DatexParser import DatexParser
from DBHandler import DBHandler
import sys
import os
import re

#---------------------------------------------------------------------------------------------------------------------------------
# Role: Entry point of the application. It initializes and orchestrates the data collection, parsing, and storage process.
# Key Functions: Calls other modules like Collector, DatexParser, and DBHandler to perform the data workflow, with a simple UI.
#---------------------------------------------------------------------------------------------------------------------------------

URL = "https://api.opentransportdata.swiss/TDP/Soap_Datex2/Pull"
TOKEN = "YOUR_TOKEN_HERE"
FETCH_INTERVAL = 60  # in seconds

DB_NAME_REGEX = re.compile(r"^[a-zA-Z0-9_\-]+$")


def list_databases(folder: str = ".") -> list[str]:
    return sorted(
        f for f in os.listdir(folder)
        if f.endswith(".db") and os.path.isfile(os.path.join(folder, f))
    )

def choose_database():
    print("1 - Create new database")
    print("2 - Open existing database")
    print("3 - Close the program.")
    choice = input("Choice: ").strip()

    if choice == "1":
        while True:
            name = input("New database name (no extension): ").strip()
            if not name:
                print("Name cannot be empty")
                continue
            if not DB_NAME_REGEX.match(name):
                print("Only letters, numbers, _ and - allowed")
                continue
            db_path = f"{name}.db"
            if os.path.exists(db_path):
                print("File already exists")
                continue
            return db_path

    elif choice == "2":
        dbs = list_databases(".")

        if not dbs:
            print("No database found in folder")
            return None

        print("\n=== Existing databases ===")
        for i, db in enumerate(dbs, start=1):
            print(f"{i} - {db}")

        while True:
            choice = input("Select the number attached to your file: ").strip()

            if choice.isdigit():
                idx = int(choice)
                if 1 <= idx <= len(dbs):
                    return dbs[idx - 1]

            print("Invalid selection")
            
    elif choice == "3":
        print("See ya !")
        sys.exit(1)
        
    else:
        raise ValueError("Invalid choice")


def main():
    print("=== SwissSpeed Collector ===")

    try:
        db_path = choose_database()
    except Exception as e:
        print("Fatal Error", e)
        sys.exit(1)

    soap_client = SoapClient(URL, TOKEN)
    db_handler = DBHandler(db_path)
    collector = Collector(
        soap=soap_client,
        parser_cls=DatexParser,
        db=db_handler,
        interval=FETCH_INTERVAL
    )

    while True:
        print("\n1 - Start collector")
        print("2 - Exit")
        choice = input("Choice: ").strip()

        if choice == "1":
            print("Collector started. Press Ctrl+C to stop.")
            collector.run()
        elif choice == "2":
            print("=== SwissSpeed Collector ===")
            try:
                db_path = choose_database()
            except Exception as e:
                print("Fatal error.", e)
                sys.exit(1)

            break
        else:
            print("Invalid choice")


if __name__ == "__main__":
    main()

