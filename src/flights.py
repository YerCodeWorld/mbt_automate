"""
Logic for checking the flight numbers and confirming their actual estimated arrival data
Uses AreoAPI for real-time accurate data..
"""

import requests
import json
from datetime import datetime, timedelta, UTC
import pytz

# Our API key from AreoAPI (FlightAware)
# I gotta use .env files. But not worth the hassle for the moment
api_key = "FTRH5ucRFrmAxSRV4FExcClLLoM0oGKY"
apiUrl = "https://aeroapi.flightaware.com/aeroapi/"

def convert_flight_code(global_code: str):
    # Welp... our api needs this... let's give it to it for it to work.
    global_to_internal = {
        "AA": "AAL",  # American Airlines
        "DL": "DAL",  # Delta Airlines
        "UA": "UAL",  # United Airlines
        "WN": "SWA",  # Southwest Airlines
        "B6": "JBU",  # JetBlue
        "AS": "ASA",  # Alaska Airlines
        "NK": "NKS",  # Spirit Airlines
        "F8": "FLE",
        "F9": "FFT",  # Frontier Airlines
        "AC": "ACA",  # Air Canada
        "WS": "WJA",  # WestJet
        "LA": "LAN",  # LATAM Airlines
        "AV": "AVA",  # Avianca
        "CM": "CMP",  # Copa Airlines
        "AF": "AFR",  # Air France
        "KL": "KLM",  # KLM Royal Dutch Airlines
        "BA": "BAW",  # British Airways
        "LH": "DLH",  # Lufthansa
        "IB": "IBE",  # Iberia
        "EK": "UAE",  # Emirates
        "QR": "QTR",  # Qatar Airways
        "TK": "THY",  # Turkish Airlines
        "ET": "ETH",  # Ethiopian Airlines
        "AZ": "ITY",  # ITA Airways
        "AR": "ARG",  # Aerolineas Argentinas
        "AM": "AMX",  # Aeromexico
        "Y4": "VOI",  # Volaris
        "VB": "VIV",  # VivaAerobus
    }
    try:
        prefix = global_code.split(" ")[0]
    except IndexError:
        return global_code

    if prefix in global_to_internal.keys():  # Is the .keys() necessary?
        internal_code = global_to_internal[prefix]
        return ''.join([internal_code, global_code.split(" ")[1]])
    return global_code.replace(" ", "")

# HELPER FUNCTION TO AUTOMATICALLY CONVERT 24H TO 12H SYSTEM
def convert_time(utc_time):
    utc_time = datetime.strptime(utc_time, "%Y-%m-%dT%H:%M:%SZ")
    # Set as UTC timezone | whatever witchery this does
    utc_time = utc_time.replace(tzinfo=pytz.UTC)
    local_timezone = pytz.timezone("America/Santo_Domingo")
    local_time = utc_time.astimezone(local_timezone)
    # print(f"Local arrival time: {local_time.strftime("%I:%M %p")}")
    # Return converted to 12h time system
    return local_time.strftime("%I:%M %p")

def get_flight_data(flight_code: str, date: str):
    if date == "tomorrow":
        tmr = datetime.now(UTC).date() + timedelta(days=1)
        start = datetime.combine(tmr, datetime.min.time()).isoformat() + 'Z'
        # The datetime.max.time() return a  float for some reason, didnt bother debugging.
        # end_time = datetime.combine(tomorrow, datetime.max.time()).isoformat() + 'Z'
        end = f"{tmr}T23:59:59Z"

        params = {
            'start': start,
            'end': end,
            'max_pages': 2
        }
        auth_header = {
            'x-apikey': api_key
        }
    else:
        params = {'max-pages': 2}
        auth_header = {'x-apikey': api_key}

    response = requests.get(apiUrl + f"flights/{flight_code}", params=params, headers=auth_header)

    if response.status_code == 200:
        data = response.json()
        with open("../puj.today.json", "w", encoding="utf-8") as fl:
            json.dump(data, fl, indent=4)
        return data
    else:
        return "No data retrieved"

# flights =  "B6869 AA2641".split(" ")
flight = "JBU869"
# data = get_flight_data("AV128", "tomorrow")
#with open("puj.today.json", "r", encoding="utf-8") as fl:
#    data = json.load(fl)

def process_flight_data(data, flight):
    """
    Process flight data to find a flight where PUJ is the destination

    Args:
        data: The flight data response from the API
        flight: The flight code/identifier
    """
    if not isinstance(data, dict) or "flights" not in data:
        print("Invalid data format or no flights found")
        return

    # Find the flight where PUJ is the destination
    flight_puj = None
    for flight_info in data["flights"]:
        if flight_info["destination"]["code_iata"] == "PUJ":
            flight_puj = flight_info
            break

    if flight_puj:
        # Found a flight where PUJ is the destination
        estimated_time_utc = flight_puj.get("estimated_in")
        actual_time = convert_time(estimated_time_utc)

        # print(f"Flight to PUJ found! Time: {actual_time}, FLIGHT CODE: {flight}")
        return actual_time
    else:
        # No flight with PUJ as destination was found
        # print(f"No flight to PUJ found for flight code: {flight}")
        return None

def get_flight_time(code: str, date="tomorrow"):
    data = get_flight_data(convert_flight_code(code), date)
    return process_flight_data(data, code)

flights = []
for flight in flights:
    print(f"Got flight {flight}:", get_flight_time(flight))

