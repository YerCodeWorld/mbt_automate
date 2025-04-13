"""
The point here is to separate the three slots, that represent the three companies
Then, we would want to separate each slot from arrival and departure type of service, but keeping them in the list
THen, we want to change the data to delete unnecessary information. Arrivals and Departures have a discrepancy in which arrivals need flight code while departures do not
These processes must be done for each company and return all the data in a single text
"""

from utils import *
import os

path = os.path.expanduser("~/Desktop")
with open(f"{path}/TODAY.csv", "r") as file:
    DATA = file.read()

# TODO: create these dynamically
AVAILABLE_COMMANDS = {
    "atd": ("AT", "AT_departures"),
    "ata": ("AT", "AT_arrivals"),
    "atdn": ("AT", "AT_departures"),
    "atan": ("AT", "AT_arrivals"),

    "std": ("ST", "ST_departures"),
    "sta": ("ST", "ST_arrivals"),
    "stdn": ("ST", "ST_departures"),
    "stan": ("ST", "ST_arrivals"),

    "mbtd": ("MBT", "MBT_departures"),
    "mbta": ("MBT", "MBT_arrivals"),
    "mbtdn": ("MBT", "MBT_departures"),
    "mbtan": ("MBT", "MBT_arrivals"),

    "help": get_commands
}
UNWANTED_ARRIVALS_INDEXES = [0, 1, 5, 7, 9, 10, 11, 12]
UNWANTED_DEPARTURES_INDEXES =  [0, 1, 5, 8, 9, 10, 11, 12]
HEADER = []
ARRIVALS_HEADER = "name,time,flight,pax,hotel"
DEPARTURES_HEADER = "name,time,pax,hotel"

HEADER_TYPE = {
    "a": ARRIVALS_HEADER,
    "d": DEPARTURES_HEADER
}
IGNORE_MODE_TYPE = {
    "arrival": UNWANTED_ARRIVALS_INDEXES,
    "departure": UNWANTED_DEPARTURES_INDEXES
}

def split_by_company(data: str) -> [[]]:
    global HEADER
    # This is the regular amount of commas from the csv
    header, removed_header = get_columns(data)
    HEADER = header
    return removed_header.strip().split(",,,,,,,,,,,")

def determine_company(data: []) -> (str, [str]):
    # take one string row - to check for the company (SINCE THAT SPECIFIC INDEX TELLS US THE TYPE OF SERVICE)
    get_company_type: str = data.strip().split("\n")[0]
    get_company_data: str = data.strip().split("\n")

    # THE INFORMATION IS AT INDEX 9, THE COLUM WHICH CONTAINS THE COMPANY
    return get_company_type.split(",")[9], get_company_data  # I made sure this was the correct index

def separate_by_type_of_service(data, mode: IGNORE_MODE_TYPE) -> ([], []):

    formatted_list = []
    for index, l in enumerate(data):
        if index not in mode:
            formatted_list.append(l)
    return formatted_list

def format_data(data: {}):

    formatted_arrivals = []
    formatted_departures = []
    # for string row in data from the company
    for dt in data:

        t = dt[0]  # type
        d = dt.split(",")  # split string row

        if t == "D":
            formatted_departures.append(",".join(separate_by_type_of_service(d, IGNORE_MODE_TYPE["departure"])))
        if t == "A":
            formatted_arrivals.append(",".join(separate_by_type_of_service(d, IGNORE_MODE_TYPE["arrival"])))

    return "\n".join(formatted_arrivals), "\n".join(formatted_departures)

def split_by_type(data: [[]]):

    tree = {}  # We will return this object

    # The company is a list of lists, so we take out each one and then work on them individually
    for i, company in enumerate(data):
        # We would need to know what company we are working for. The information is in each row so
        # we are just sending the data to check one of them and get the index which has the information
        # returning the company we get as well as the whole list of rows
        cmp, cmp_data = determine_company(company)
        a, d = format_data(cmp_data)   # Arrivals, departures
        tree[cmp] = {
            # Now we will divide departures and arrivals from each company
            f"{cmp}_arrivals": a,
            f"{cmp}_departures": d
        }

    return tree

# TODO: PLEASE REFACTOR
def program(result):

    while True:
        command = input("Enter your command: ").lower().strip()
        if "write" in command:

            try:
                data_to_write = command.split(" ")
                if len(data_to_write) > 1:
                    cmp = AVAILABLE_COMMANDS[data_to_write[1]]
                    hd_type = command[-1]
                    write_to_directory(path, f"{data_to_write[1]}", result[cmp[0]][cmp[1]], HEADER_TYPE[hd_type])
                else:
                    print("write what? ")
            except Exception as err:
                print("Here: ", err)

            continue
        try:
            if command == "exit":
                break

            elif command == "help":
                print_help(command, AVAILABLE_COMMANDS)

            elif command[len(command)-1] == "n":
                cmd = AVAILABLE_COMMANDS[command]
                print(get_names(result[cmd[0]][cmd[1]]))
            else:
                cmp = AVAILABLE_COMMANDS[command]
                # print(cmp[0]) leaving here for example
                print(result[cmp[0]][cmp[1]])

        # Nice solution
        except KeyError:
            print("Could not get information for that company")

def main():
    # We have to split the data in a list, in order to separate it by company
    data_after_split = split_by_company(DATA)  # works
    # Then we will simply create an object with all the companies as keys, and a dictionary (arrivals | departures)
    # as the values. This lists will also go through a refactoring process to remove unnecessary information
    # according to its type
    result = split_by_type(data_after_split)  # work
    program(result)

main()