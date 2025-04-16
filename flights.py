import requests
import json
from datetime import datetime, timedelta, UTC

api_key = "FTRH5ucRFrmAxSRV4FExcClLLoM0oGKY"
def option_1():

    flight_id = "CMP744"
    url = f"https://aeroapi.flightaware.com/aeroapi/flights/{flight_id}"

    headers = {
        "x-apikey": api_key
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        for flight in data.get("flights", []):
            arrival_time = flight.get("estimated_arrival_time")
            print(f"Estimated Arrival Time: {arrival_time}")
    else:
        print(f"Error: {response.status_code} - {response.text}")

apiUrl = "https://aeroapi.flightaware.com/aeroapi/"

airport = 'PUJ'
tomorrow = datetime.now(UTC).date() + timedelta(days=1)
start_time = datetime.combine(tomorrow, datetime.min.time()).isoformat() + 'Z'
end_time = datetime.combine(tomorrow, datetime.max.time()).isoformat() + 'Z'

params = {
    'start': "2025-04-17T00:00:00Z",
    'end': "2025-04-17T23:59:59Z",
    'max_pages': 2
}
auth_header = {'x-apikey':api_key}

response = requests.get(apiUrl + f"flights/LA2450",
    params=params, headers=auth_header)

if response.status_code == 200:
    data = response.json()
    with open("puj_today.json", "w") as fl:
        json.dump(data, fl, indent=6)
    print(response.json())
else:
    print("Error executing request")