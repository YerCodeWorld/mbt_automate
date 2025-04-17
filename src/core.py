"""
The point here is to separate the three slots, that represent the three companies
Then, we would want to separate each slot from arrival and departure type of service, but keeping them in the list
THen, we want to change the data to delete unnecessary information. Arrivals and Departures have a discrepancy in which arrivals need flight code while departures do not
These processes must be done for each company and return all the data in a single text
"""

from extended import *
from utils import *
from slide_generator import create_slides as slides
from flights import api as flight_check
import os

# TODO: Implement getting this info from JSON file
path = os.path.expanduser("~/Desktop")
file = "extracted.csv"

# TODO: create these dynamically
AVAILABLE_COMMANDS = {
    "atd": ("AT", "AT_departures"),
    "ata": ("AT", "AT_arrivals"),
    "std": ("ST", "ST_departures"),
    "sta": ("ST", "ST_arrivals"),
    "mbtd": ("MBT", "MBT_departures"),
    "mbta": ("MBT", "MBT_arrivals"),

    "help": ("", ""),
    "exit": ("", ""),
    "flights": ("", ""),
    "checkfl": ("",""),
    "names": ("", ""),
    "pdfs": ("", ""),
    "write": ("", ""),
    "config": ("", "")   # Use this to change the configuration from the JSON file when we implement it
}

ACTIONS = {
    # We could pass the arguments here directly? I don't knoW...
    # Not very optimistic for these approaches.
    "pdfs":     lambda a,b,c,d:     create_pdfs(a, b, c, d),
    "create":   lambda a, b, c:     slides(a, b, c),
    "names":    lambda a:           print(get_names(a)),
    "flights":  lambda a:           print(get_flights(a)),
    "checkfl":  lambda a:           print(flight_check(get_flights(a))),
    "write":    lambda a, b, c, d:  write_to_directory(a, b, c, d),
    "help":     lambda a, b:        print(print_help(a, b))
}

HEADER_TYPE = {
    "a": "name,time,flight,pax,hotel",
    "d": "name,time,pax,hotel"
}

VALID_DATA = {
    "arrival": list[int],
    "departure": list[int],
    "company": int
}

HEADER = list[str]

# STEP 1: remove the header of the csv file extracted from a google sheets file.
# STEP 1: our files have an empty line to separate companies. we will use that to split the data
def company_split(data: str) -> [[]]:
    global HEADER
    # First remove the header and get information from it like the length  to get the amount of columns
    header_data, sliced_data = get_columns(data)
    HEADER = header_data[1]
    # print(len(","*header_data[0]) == len(",,,,,,,,,,,"))
    return sliced_data.strip().split(",,,,,,,,,,,,")

# STEP 2: now we want to separate the data in arrivals / departures from each data bucket
def organize_by_type(data: [[]], company_index: int, valid_data=None):
    if valid_data is None:
        valid_data = VALID_DATA

    result = {}
    for i, bucket in enumerate(data):

        company_name, company_data = get_company(bucket, company_index)
        arrivals, departures = get_services(company_data, valid_data)
        result[company_name] = {
            # Now we will divide departures and arrivals from each company
            f"{company_name}_arrivals": arrivals,
            f"{company_name}_departures": departures
        }
    return result

# TODO: this still needs a better approach
def program(data):

    while True:
        command = input("\033[34mEnter your command:\033[0m").lower().strip()
        if len(command.split(" ")) > 1:
            command = command.lower().split(" ")

        try:
            if command[0] in ACTIONS.keys():

                cmds = AVAILABLE_COMMANDS[command[1]]
                c = command[0]

                # An approach we could take is passing all the possible arguments to a dictionary and pass that
                # dictionary to helper functions, that way reducing the clumsiness of this function.

                if c == "pdfs":
                    ACTIONS[c](data, AVAILABLE_COMMANDS[command[1]], command[1], path)
                elif c == "names":
                    ACTIONS[c](data[cmds[0]][cmds[1]])
                elif c == "create":
                    ACTIONS[c](data[cmds[0]][cmds[1]], cmds[0], command[1][-1])
                elif c == "checkfl":
                    if not command[1][-1] == "d":
                        ACTIONS[c](data[cmds[0]][cmds[1]])
                    else:
                        colored_print("Departures do not provide flights we need to check on.", "yellow")
                elif c == "flights":
                    if not command[1][-1] == "d":
                        ACTIONS[c](data[cmds[0]][cmds[1]])
                    else:
                        colored_print("Departures do not provide flights we need to check on.", "yellow")
                elif c == "write":
                    hd_type = command[1][-1]
                    ACTIONS[c](path, f"{command[1]}", data[cmds[0]][cmds[1]], HEADER_TYPE[hd_type])
                elif c == "help":
                    ACTIONS[c](command[1], AVAILABLE_COMMANDS)
                continue

            if command == "exit":
                break
            else:
                cmp = AVAILABLE_COMMANDS[command]
                print(data[cmp[0]][cmp[1]])

        except KeyError:
            colored_print("Could not get information for that company", "yellow")

def main():
    global VALID_DATA

    # STEP 0
    with open(f"{path}/{file}", "r") as fl:
        data = fl.read()
    # Step 1
    data_buckets = company_split(data)
    # Step 2
    VALID_DATA = get_valid_indexes(HEADER)
    # Step 3
    result = organize_by_type(data_buckets, VALID_DATA["company"])  # work

    program(result)


# TODO: Create starter interface in which we have commands like start, help, and global interest functions in general
# This would allow to reuse the program as many times as we would like to
main()