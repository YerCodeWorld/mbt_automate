
import json
import csv
import os
import datetime
from copy import copy

from src.utils import colored_print
from datetime import timedelta
from pathlib import Path

TOMORROW = str(datetime.date.today() + timedelta(days=1))

def determine_service_type(reservation):
    """
    Determine if a service is an arrival or departure based on pickup/dropoff locations
    and return date if present.
    """
    pickup_location = reservation["pickup_location"]["name"]
    dropoff_location = reservation["drop_of_location"]["name"]
    return_date = reservation["travel"].get("return")

    # Today's date (used to check if return date is today)
    tomorrow = datetime.datetime.strptime(TOMORROW, "%Y-%m-%d").date()

    # If return date exists and is today, it's a departure regardless of locations
    if return_date:
        return_datetime = datetime.datetime.strptime(return_date.split("T")[0], "%Y-%m-%d").date()
        if return_datetime == tomorrow:
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

    # Define CSV headers (Could be loaded from config file too)
    headers = ["Tipo", "Código", "Cliente", "Hora", "Vuelo", "Vehiculo", "Pax", "Desde", "Hacia", "COMP"]

    # Write to CSV
    with open(output_path, 'w', encoding='utf-8', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=headers)
        writer.writeheader()
        total_services = 0

        for reservation in data:

            # Skip records that are not for the target date (tomorrow's)
            flight_arrival = reservation["travel"].get("flight_arrival", "")
            return_date = reservation["travel"].get("return", "")

            if not flight_arrival or not flight_arrival.startswith(TOMORROW):
                if return_date == "null":
                    continue

            # We don't need these services either
            refunded: bool = float(reservation["price"]["refund_amount"]) > 0
            if refunded:
                continue

            service_type = determine_service_type(reservation)
            # Remember to take the spaces
            name = clean_name(reservation["passenger"]["name"]) + " " + clean_name(reservation["passenger"]["surname"])

            pax_indices = ["adult", "children", "infant"]
            pax = sum([int(reservation["travelers"][ct]) for ct in pax_indices])

            pickup_location = reservation["pickup_location"]["name"].split(",")[0]
            drop_off = reservation["drop_of_location"]["name"].split(",")[0]

            if str(return_date).startswith(TOMORROW):
                cp = copy(pickup_location)
                pickup_location = drop_off
                drop_off = cp

            # Prepare row data
            row = {
                "Tipo": service_type,
                "Código": reservation["reservation_no"],
                "Cliente": name,
                "Hora": flight_arrival,
                "Vehiculo": reservation["segment"],
                "Pax": pax,
                "Desde": pickup_location,
                "Hacia": drop_off,
                "COMP": "AT" # Will always be this
            }

            # Handle flight number and time based on service type
            if service_type == "Arrival":
                row["Vuelo"] = reservation["travel"]["flight_number"]
                row["Hora"] = "..."  # For arrivals, time is set to NONE as requested
            else:  # Departure
                row["Vuelo"] = ""  # No flight number for departures
                # For departures, use the arrival time or return time if it's today
                if reservation["travel"].get("return") and TOMORROW in reservation["travel"]["return"]:
                    row["Hora"] = convert_time_format(reservation["travel"]["return"])
                else:
                    row["Hora"] = convert_time_format(reservation["travel"]["flight_arrival"])

            writer.writerow(row)
            total_services += 1

    colored_print(f"CSV file has been created at: {output_path}", "green")
    colored_print(f"We got a total of {total_services} services. Make sure this aligns with the amount shown in AirportTransfer Website", "yellow")


def extract():
    # Paths
    json_file = "ATbookings.json"  # Update this path to your JSON file location
    csv_file = "extracted.csv"

    process_json_to_csv(json_file, csv_file)
