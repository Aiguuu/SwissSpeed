import xml.etree.ElementTree as ET
from typing import List, Dict
from SoapClient import SoapClient

class DatexParser:

    def __init__(self, xml_text: str):
        self.xml_text = xml_text

    def parse(self):
        records = []

        root = ET.fromstring(self.xml_text)
        ns = {"dx": "http://datex2.eu/schema/2/2_0"}

        for site in root.findall(".//dx:siteMeasurements", ns):

            record = {
                "Location": None,
                "Timestamp": None,
                "LightFlow": None,
                "HeavyFlow": None,
                "LightSpeed": None,
                "HeavySpeed": None,
                "Error": None
            }

            try:
                record["Location"] = site.find(
                    "dx:measurementSiteReference", ns
                ).attrib["id"]

                record["Timestamp"] = site.find(
                    "dx:measurementTimeDefault", ns
                ).text

                seen = set()

                for mv in site.findall("dx:measuredValue", ns):
                    index = mv.attrib.get("index")
                    seen.add(index)

                    basic = mv.find("dx:measuredValue/dx:basicData", ns)
                    if basic is None:
                        continue

                    flow = basic.find(".//dx:vehicleFlowRate", ns)
                    if flow is not None:
                        value = int(float(flow.text))
                        if index == "11":
                            record["LightFlow"] = value
                        elif index == "21":
                            record["HeavyFlow"] = value

                    speed = basic.find(".//dx:speed", ns)
                    if speed is not None:
                        value = int(float(speed.text))
                        if index == "12":
                            record["LightSpeed"] = value
                        elif index == "22":
                            record["HeavySpeed"] = value

                missing = []
                for idx, label in {
                    "11": "LightFlow",
                    "12": "LightSpeed",
                    "21": "HeavyFlow",
                    "22": "HeavySpeed"
                }.items():
                    if record[label] is None and idx not in seen:
                        missing.append(label)

                if missing:
                    record["Error"] = "Missing from API: " + ", ".join(missing)

            except Exception as e:
                record["Error"] = f"Parser error: {e}"

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
        xml_response = soap_client.fetch() 

        ns = {'dx223': 'http://datex2.eu/schema/2/2_0'}
        root = ET.fromstring(xml_response)
        site_measurements = root.findall('.//dx223:siteMeasurements', ns)
        if not site_measurements:
            raise ValueError("SOAP fetch succeeded but no <siteMeasurements> found – check token and URL!")

        print(f"Fetch succeeded and {len(site_measurements)} siteMeasurements found")

    except Exception as e:
        print("SOAP fetch failed:", e)
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

        print(f"Parsing succeeded, {len(data)} records found")
        print("Sample records:", data[:3])
    except Exception as e:
        print("Parsing failed:", e)

