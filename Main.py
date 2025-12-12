from SoapClient import SoapClient
from DatexParser import DatexParser
from DBHandler import DBHandler

# === CONFIG ===
URL = "https://api.opentransportdata.swiss/TDP/Soap_Datex2/Pull"
TOKEN = "ton_token_ici"
DB_PATH = "SwissSpeed.db"

def run_pipeline(url: str, token: str, db_path: str):
    # --- Step 1: Fetch XML ---
    try:
        print("=== Fetching data from SOAP API ===")
        soap_client = SoapClient(url, token)
        xml_response = soap_client.fetch()
        print("✅ Fetch succeeded")
    except Exception as e:
        print("❌ Fetch failed:", e)
        return

    # --- Step 2: Parse XML ---
    try:
        print("=== Parsing XML ===")
        parser = DatexParser(xml_response)
        records = parser.parse()
        if not records:
            raise ValueError("Parsed data is empty – check token and XML structure")
        print(f"✅ Parsing succeeded, {len(records)} records found")
        print("Sample records:", records[:3])
    except Exception as e:
        print("❌ Parsing failed:", e)
        return

    # --- Step 3: Insert into DB ---
    try:
        print("=== Inserting data into DB ===")
        db = DBHandler(db_path)
        db.insert_records(records)
        print(f"✅ Inserted {len(records)} records into DB '{db_path}'")
    except Exception as e:
        print("❌ DB insertion failed:", e)
    finally:
        db.close()

if __name__ == "__main__":
    run_pipeline(URL, TOKEN, DB_PATH)

