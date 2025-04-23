"""
The point here is to separate the three slots, that represent the three companies
Then, we would want to separate each slot from arrival and departure type of service, but keeping them in the list
THen, we want to change the data to delete unnecessary information. Arrivals and Departures have a discrepancy in which arrivals need flight code while departures do not
These processes must be done for each company and return all the data in a single text
"""

from src.extended import *
from src.utils import *
from src.airportTransfer import generate_at_bookings
from src.extract import extract
from src.generator import create_slides as slides
from src.flights import api as flight_check
import os

# TODO: Implement getting this info from JSON file
path = os.path.expanduser("~/Desktop")
file = "TODAY.csv"

AVAILABLE_COMMANDS = {
    "atd": ("AT", "AT_departures"),
    "ata": ("AT", "AT_arrivals"),
    "std": ("ST", "ST_departures"),
    "sta": ("ST", "ST_arrivals"),
    "mbtd": ("MBT", "MBT_departures"),
    "mbta": ("MBT", "MBT_arrivals"),
}

DATA = {}

def correct_flight_bridge(c):
    DATA[c[0]][c[1]] = correct_flights(DATA[c[0]][c[1]], c[0], c[1][3:])

ACTIONS = {
    # "pdfs":              lambda a,b,c,d:     create_pdfs(a, b, c, d),
    "create":            lambda c:           slides(DATA[c[0]][c[1]], c[0], c[1]),
    "names":             lambda c:           print_names(get_names(DATA[c[0]][c[1]])),
    "flights":           lambda c:           print_flights(get_flights(DATA[c[0]][c[1]]), c[1]),
    "checkflights":      lambda c:           flight_check(get_flights(DATA[c[0]][c[1]]), c[1]),
    "correctflights":    lambda c:           correct_flight_bridge(c),
    "bookings":          lambda c:           generate_at_bookings(),
    "extract":           lambda c:           extract()
    # "write":             lambda a, b, c, d:  write_to_directory(a, b, c, d),
}

HEADER_TYPE = {
    "a": "name,time,flight,pax,hotel",
    "d": "name,time,pax,hotel"
}

VALID_DATA = {
    "arrival": list[int],
    "departure": list[int],
    "company": int,
    "name": int
}

HEADER = list[str]

# STEP 1: remove the header of the csv file extracted from a google sheets file.
# STEP 1: our files have an empty line to separate companies. we will use that to split the data
def company_split(data: str) -> [[]]:
    global HEADER

    data = data.split("\n")
    HEADER = data[0].split(",")
    sliced_data = "\n".join(data[1:])

    # OUR CURRENT DOCUMENT CONTAINS BLANK LINE SEPARATING COMPANIES, WHICH IS REPRESENTED AS COMMAS (ROWS)
    # If something more solid is needed, we would need to read the "COMP" colum to determine when we find a different company
    return sliced_data.strip().split(',,,,,,,,,,,,')

# STEP 2: now we want to separate the data in arrivals / departures from each data bucket
def organize_by_type(data: [[]], company_index: int, valid_data=None):
    if valid_data is None:
        valid_data = VALID_DATA

    # Huge object
    result = {}
    for i, bucket in enumerate(data):

        services = bucket.strip().split("\n")
        company = services[0].split(",")[company_index]  # Take first data row at index COMP
        arrivals, departures = get_services(services, valid_data)

        result[company] = {
            # Now we will divide departures and arrivals from each company
            f"{company}_arrivals": arrivals,
            f"{company}_departures": departures
        }
    return result

def program():
    global DATA

    while True:
        command = input("\033[34mEnter your command:\033[0m").lower().strip()
        if len(command.split(" ")) > 1:
            command = command.lower().split(" ")

        try:
            if command[0] in ACTIONS.keys():

                cmds = AVAILABLE_COMMANDS[command[1]]
                c = command[0]
                ACTIONS[c](cmds)
                continue

            if command == "process":
                break
            if command == "exit":
                exit(0)
            else:
                company = AVAILABLE_COMMANDS[command]
                print(DATA[company[0]][company[1]])

        except KeyError:
            colored_print("Could not get information for that company", "yellow")

def main():
    while True:

        start = input("Do program? ")
        if start.lower() == "yes":
            global DATA, VALID_DATA

            # STEP 0: OPEN CSV FILE DOWNLOADED FROM ITINERARY
            with open(f"{path}/{file}", "r") as fl:
                data = fl.read()

            # STEP 1: We have data "buckets" which just refer to the different services we get separated by company
            data_buckets = company_split(data)
            # STEP 2: We have a lot of unnecessary information in the current buckets. Based on the header,
            # we get the valid indexes of the data we actually want.
            VALID_DATA = get_valid_indexes(HEADER)

            # STEP 3
            DATA = organize_by_type(data_buckets, VALID_DATA["company"])

            program()

        else:
            print("See ya")
            break

main()