import xml.etree.ElementTree as ET
from typing import List, Dict
from SoapClient import SoapClient

class DatexParser:
    def __init__(self, xml_text: str):
        self.xml_text = xml_text

    def parse(self) -> List[Dict]:
        """
        Parse the XML and return a list of dictionaries with columns for SwissSpeed.
        """
        records = []
        try:
            root = ET.fromstring(self.xml_text)
        except ET.ParseError as e:
            raise ValueError(f"XML parsing error: {e}")

        ns = {
            'dx223': 'http://datex2.eu/schema/2/2_0'
        }

        for site in root.findall('.//dx223:siteMeasurements', ns):
            record = {}
            try:
                record['Location'] = site.find('dx223:measurementSiteReference', ns).attrib['id']
                record['Timestamp'] = site.find('dx223:measurementTimeDefault', ns).text

                # Default values
                record['LightFlow'] = None
                record['HeavyFlow'] = None
                record['LightSpeed'] = None
                record['HeavySpeed'] = None
                record['Error'] = None

                for mv in site.findall('dx223:measuredValue', ns):
                    index = mv.attrib.get('index')
                    basic = mv.find('dx223:measuredValue/dx223:basicData', ns)
                    if basic is None:
                        continue

                    # TrafficFlow
                    flow = basic.find('dx223:TrafficFlow/dx223:vehicleFlow/dx223:vehicleFlowRate', ns)
                    if flow is not None:
                        val = int(float(flow.text))
                        if index in ['11', '12']:
                            record['LightFlow'] = val
                        elif index in ['21', '22']:
                            record['HeavyFlow'] = val

                    # TrafficSpeed
                    speed = basic.find('dx223:TrafficSpeed/dx223:averageVehicleSpeed/dx223:speed', ns)
                    if speed is not None:
                        val = int(float(speed.text))
                        if index in ['12']:
                            record['LightSpeed'] = val
                        elif index in ['22']:
                            record['HeavySpeed'] = val

            except Exception as e:
                record['Error'] = str(e)

            records.append(record)
        return records

# ==========================
# MAIN FOR TESTING
# ==========================
if __name__ == "__main__":
    print("=== DatexParser Test (with SoapClient) ===")

    url = "https://api.opentransportdata.swiss/TDP/Soap_Datex2/Pull"
    token = "ton_token_ici"

    # --- Fetch XML ---
    try:
        soap_client = SoapClient(url, token)
        print("--- Fetching XML ---")
        xml_response = soap_client.fetch()  # xml_response est défini ici

        # Vérification correcte avec ElementTree
        import xml.etree.ElementTree as ET
        ns = {'dx223': 'http://datex2.eu/schema/2/2_0'}
        root = ET.fromstring(xml_response)
        site_measurements = root.findall('.//dx223:siteMeasurements', ns)
        if not site_measurements:
            raise ValueError("SOAP fetch succeeded but no <siteMeasurements> found – check token and URL!")

        print(f"✅ Fetch succeeded and {len(site_measurements)} siteMeasurements found")

    except Exception as e:
        print("❌ SOAP fetch failed:", e)
        exit(1)

    # --- Parse XML ---
    try:
        parser = DatexParser(xml_response)
        print("--- Parsing XML ---")
        data = parser.parse()
        if not data:
            raise ValueError("Parsed data is empty – token may be missing or invalid")

        # Verify columns on first 3 measurements
        for rec in data[:3]:
            for col in ["Location","Timestamp","LightFlow","HeavyFlow","LightSpeed","HeavySpeed"]:
                if col not in rec:
                    raise ValueError(f"Missing column {col} in record: {rec}")

        print(f"✅ Parsing succeeded, {len(data)} records found")
        print("Sample records:", data[:3])
    except Exception as e:
        print("❌ Parsing failed:", e)

