import time

#-------------------------------------------------------------------------------------------
# Role: Responsible for collecting data from the external source (the API).
# Key Functions: Uses SoapClient to fetch data and passes it to DatexParser for parsing.
#-------------------------------------------------------------------------------------------

class Collector:

    def __init__(self, soap, parser_cls, db, interval):
        self.soap = soap
        self.parser_cls = parser_cls
        self.db = db
        self.interval = interval

    def run(self):
        print("Collector running")

        while True:
            try:
                print("\nFetching new data...")
                xml = self.soap.fetch()
                print("Fetch succeeded")

                parser = self.parser_cls(xml)
                records = parser.parse()
                print(f"Parsed {len(records)} records")

                inserted = self.db.insert_records(records)
                print(f"{inserted} new records detected")
                print(f"Inserted {inserted} records !")

                print(f"Waiting {self.interval}s for next update...")
                print(f"Ctrl+C to stop and return to menu")
                time.sleep(self.interval)

            except KeyboardInterrupt:
                print("\nCollector stopped — returning to menu\n")
                break

