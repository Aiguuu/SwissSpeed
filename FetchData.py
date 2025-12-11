import requests

url = "https://api.opentransportdata.swiss/TDP/Soap_Datex2/Pull"

# Defines the request Token and Hash between quotes
headers = {
    "Authorization": "eyJvcmciOiI2NDA2NTFhNTIyZmEwNTAwMDEyOWJiZTEiLCJpZCI6ImQ4ZjdhMGQ0NTg0ZjRmMzliODI4YTNmZDdjNjdiMWI4IiwiaCI6Im11cm11cjEyOCJ9",
    "X-Hash": "60e8abbe9205f993a413708970bad626"
}

# Sends the request and saves feedback in "response"
response = requests.get(url, headers=headers)

# Prints the feedback
print(f"Status Code: {response.status_code}")
print(f"Response: {response.text}")
