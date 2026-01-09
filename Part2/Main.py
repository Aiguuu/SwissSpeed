from DBHandler import DBHandler
from DashboardServer import DashboardServer
from SoapClient import SoapClient
from DatexParser import DatexParser
from Collector import Collector
import threading

def main():
    SOAP_URL = "https://api.opentransportdata.swiss/TDP/Soap_Datex2/Pull"
    TOKEN = "eyJvcmciOiI2NDA2NTFhNTIyZmEwNTAwMDEyOWJiZTEiLCJpZCI6ImQ4ZjdhMGQ0NTg0ZjRmMzliODI4YTNmZDdjNjdiMWI4IiwiaCI6Im11cm11cjEyOCJ9"

    db_handler = DBHandler("/home/theobias/traffic.db")

    soap_client = SoapClient(SOAP_URL, TOKEN)
    datex_parser = DatexParser 

    collector = Collector(soap_client, datex_parser, db_handler, interval=60)

    collector_thread = threading.Thread(target=collector.run)
    collector_thread.daemon = True  
    collector_thread.start()

    dashboard = DashboardServer(db_handler)
    dashboard.run()

if __name__ == '__main__':
    main()

