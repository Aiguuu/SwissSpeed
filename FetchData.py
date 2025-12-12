import requests

url = "https://api.opentransportdata.swiss/TDP/Soap_Datex2/Pull"

soap_body = """<?xml version="1.0" encoding="UTF-8"?>
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/">
  <soapenv:Header/>
  <soapenv:Body>
    <d2LogicalModel xmlns="http://datex2.eu/schema/2/2_0"
                     xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                     modelBaseVersion="2">
      <exchange>
        <supplierIdentification>
          <country>ch</country>
          <nationalIdentifier>MYAPP</nationalIdentifier>
        </supplierIdentification>
      </exchange>
    </d2LogicalModel>
  </soapenv:Body>
</soapenv:Envelope>
"""

headers = {
    "Authorization": f"Bearer eyJvcmciOiI2NDA2NTFhNTIyZmEwNTAwMDEyOWJiZTEiLCJpZCI6ImQ4ZjdhMGQ0NTg0ZjRmMzliODI4YTNmZDdjNjdiMWI4IiwiaCI6Im11cm11cjEyOCJ9",
    "Content-Type": "text/xml; charset=utf-8",
    "SoapAction": "http://opentransportdata.swiss/TDP/Soap_Datex2/Pull/v1/pullMeasuredData"
}

response = requests.post(url, data=soap_body, headers=headers)

print("Status:", response.status_code)
print(response.text[:500]) 
