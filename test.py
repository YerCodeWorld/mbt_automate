"""
from datetime import datetime
import pytz

def convert_time(utc_time):
    utc_time = datetime.strptime(utc_time, "%Y-%m-%dT%H:%M:%SZ")
    # Set as UTC timezone | whatever witchery this does
    utc_time = utc_time.replace(tzinfo=pytz.UTC)
    local_timezone = pytz.timezone("America/Santo_Domingo")
    local_time = utc_time.astimezone(local_timezone)

    # Return converted to 12h time system
    return f"Local arrival time: {local_time.strftime("%I:%M %p")}"


# 2025-04-18T15:20:00:00Z
# 2025-04-18T11:30:00.000000Z
# print(convert_time("2025-04-18T11:30:00Z"))
"""

import json
import csv
import os
import datetime
from pathlib import Path


def determine_service_type(reservation):
    """
    Determine if a service is an arrival or departure based on pickup/dropoff locations
    and return date if present.
    """
    pickup_location = reservation["pickup_location"]["name"]
    dropoff_location = reservation["drop_of_location"]["name"]
    return_date = reservation["travel"].get("return")

    # Today's date (used to check if return date is today)
    today = datetime.datetime.strptime("2025-04-18", "%Y-%m-%d").date()

    # If return date exists and is today, it's a departure regardless of locations
    if return_date:
        return_datetime = datetime.datetime.strptime(return_date.split("T")[0], "%Y-%m-%d").date()
        if return_datetime == today:
            return "Departure"

    # Otherwise, determine by locations
    if "Airport" in pickup_location:
        return "Arrival"
    elif "Airport" in dropoff_location:
        return "Departure"
    else:
        # Default case if neither contains "Airport" (shouldn't happen with this data)
        return "Unknown"


def clean_name(name):
    """Clean passenger names by capitalization and handling special characters"""
    if name:
        # Handle specific cases like "del carmen" that should be capitalized
        name = name.title()
    return name


def convert_time_format(time_str):
    """Convert time from ISO format to 12-hour format"""
    if not time_str:
        return "NONE"

    # Extract time from ISO format
    dt = datetime.datetime.strptime(time_str, "%Y-%m-%dT%H:%M:%S.%fZ")

    # Format to 12-hour time
    formatted_time = dt.strftime("%I:%M %p").lower()

    # Remove leading zero in hour if present
    if formatted_time.startswith("0"):
        formatted_time = formatted_time[1:]

    return formatted_time


def process_json_to_csv(json_path, csv_path):
    """Process the JSON data and export to CSV"""
    # Read JSON data
    with open(json_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    # Create desktop path for output
    desktop_path = os.path.join(Path.home(), "Desktop")
    output_path = os.path.join(desktop_path, csv_path)

    # Define CSV headers
    headers = ["Tipo", "Código", "Cliente", "Pickup", "Vuelo", "Vehiculo", "Pax", "Desde", "Hacia", "COMP"]

    # Write to CSV
    with open(output_path, 'w', encoding='utf-8', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=headers)
        writer.writeheader()

        for reservation in data:
            # Skip records that are not for the target date (April 18, 2025)
            flight_arrival = reservation["travel"].get("flight_arrival", "")
            if not flight_arrival or not flight_arrival.startswith("2025-04-18"):
                continue

            service_type = determine_service_type(reservation)

            passenger_name = clean_name(reservation["passenger"]["name"])
            passenger_surname = clean_name(reservation["passenger"]["surname"])
            name = passenger_name + passenger_surname

            adults = reservation["travelers"]["adult"]
            children = reservation["travelers"]["children"]
            infants = reservation["travelers"]["infant"]
            pax = int(adults) + int(children) + int(infants)

            # Prepare row data
            row = {
                "Tipo": service_type,
                "Código": reservation["reservation_no"],
                "Cliente": name,
                "Hora": flight_arrival,
                "Vehiculo": reservation["segment"],
                "Pax": pax,
                "Desde": reservation["pickup_location"]["name"],
                "Hasta": reservation["drop_of_location"]["name"],
                "COMP": "AT"
            }

            # Handle flight number and time based on service type
            if service_type == "Arrival":
                row["flight_number"] = reservation["travel"]["flight_number"]
                row["time"] = "NONE"  # For arrivals, time is set to NONE as requested
            else:  # Departure
                row["flight_number"] = ""  # No flight number for departures
                # For departures, use the arrival time or return time if it's today
                if reservation["travel"].get("return") and "2025-04-18" in reservation["travel"]["return"]:
                    row["time"] = convert_time_format(reservation["travel"]["return"])
                else:
                    row["time"] = convert_time_format(reservation["travel"]["flight_arrival"])

            writer.writerow(row)

    print(f"CSV file has been created at: {output_path}")


if __name__ == "__main__":
    # Paths
    json_file = "ATbookings.json"  # Update this path to your JSON file location
    csv_file = "extracted.csv"

    process_json_to_csv(json_file, csv_file)
