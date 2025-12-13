import requests

class SoapClient:
    """
    Simple SOAP client to fetch data from OTD Swiss API.
    """

    def __init__(self, url: str, token: str):
        self.url = "https://api.opentransportdata.swiss/TDP/Soap_Datex2/Pull"
        self.token = "YOUR_TOKEN_HERE"

    def build_envelope(self) -> str:
        return """<?xml version="1.0" encoding="UTF-8"?>
<SOAP-ENV:Envelope xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/" xmlns:tdpplv1="http://datex2.eu/wsdl/TDP/Soap_Datex2/Pull/v1" xmlns:dx223="http://datex2.eu/schema/2/2_0">
    <SOAP-ENV:Body>
        <d2LogicalModel modelBaseVersion="2" xmlns:D2LogicalModel="http://datex2.eu/schema/2/2_0" xmlns="http://datex2.eu/schema/2/2_0">
            <exchange>
                <supplierIdentification>
                    <country>ch</country>
                    <nationalIdentifier>ODMCH_example</nationalIdentifier>
                </supplierIdentification>
            </exchange>
            <payloadPublication xsi:type="GenericPublication" lang="en">
                <publicationTime>2024-08-27T18:18:18</publicationTime>
                <publicationCreator>
                    <country>ch</country>
                    <nationalIdentifier>ODMCH_example</nationalIdentifier>
                </publicationCreator>
                <genericPublicationName>MeasuredDataFilter</genericPublicationName>
                <genericPublicationExtension>
                    <measuredDataFilter>
                        <measurementSiteTableReference targetClass="MeasurementSiteTable" id="OTD:TrafficData" version="0"></measurementSiteTableReference>
                        <siteRequestReference targetClass="MeasurementSiteRecord" id="CH:0003.01" version="0"/>
                        <siteRequestReference targetClass="MeasurementSiteRecord" id="CH:0003/02" version="0"/>
                        <siteRequestReference targetClass="MeasurementSiteRecord" id="CH:0346\.[0-9]*" version="0"/>
                        <siteRequestReference targetClass="MeasurementSiteRecord" id="CH:0347/+" version="0"/>
                        <siteRequestReference targetClass="MeasurementSiteRecord" id="CH:0610/#" version="0"/>
                        <siteRequestReference targetClass="MeasurementSiteRecord" id="CH:067[0-9.]*" version="0"/>
                    </measuredDataFilter>
                </genericPublicationExtension>
            </payloadPublication>
        </d2LogicalModel>
    </SOAP-ENV:Body>
</SOAP-ENV:Envelope>"""

    def fetch(self) -> str:
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "text/xml; charset=utf-8",
            "SoapAction": "http://opentransportdata.swiss/TDP/Soap_Datex2/Pull/v1/pullMeasuredData"
        }

        response = requests.post(self.url, data=self.build_envelope(), headers=headers)

        if response.status_code != 200:
            print("HTTP error:", response.status_code)
            print("Server response:")
            print(response.text)  # <- Affiche le SOAP Fault
        response.raise_for_status()
        return response.text.lstrip("\ufeff").strip()



# ==========================
# MAIN FOR TESTING
# ==========================
if __name__ == "__main__":
    print("=== SoapClient Test ===")

    SOAP_URL = "https://api.opentransportdata.swiss/TDP/Soap_Datex2/Pull"
    TOKEN = "YOUR_TOKEN_HERE" 

    client = SoapClient(SOAP_URL, TOKEN)

    # Test build_envelope
    print("\n--- Testing build_envelope() ---")
    envelope = client.build_envelope()
    if envelope.startswith("<?xml"):
        print("build_envelope() begins correctly /!\ But still may be incorrect /!\ ")
    else:
        print("build_envelope() is not filled correctly")

    # Test fetch
    print("\n--- Testing fetch() ---")
    try:
        xml_response = client.fetch()
        print("✅ fetch() succeeded, received response length:", len(xml_response))
        print("Preview:", xml_response[:400], "...")
    except requests.exceptions.HTTPError as http_err:
        print("❌ HTTP error occurred:", http_err)
    except Exception as err:
        print("❌ Other error occurred:", err)

