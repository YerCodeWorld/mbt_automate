from pypdf import PdfReader, PdfWriter
from src.flights import api as flight_check
from datetime import datetime

# I could use the console purely on white but meh I like this better
def colored_print(message: str, color):
    colors = {
        "red": 31,
        "green": 32,
        "yellow": 33,
        "blue": 34
    }
    print(f"\033[{colors[color]}m{message}\033[0m")

# No idea why if im the only one using this thing but ok
def print_help(command, available_commands):
    print("Available Commands: ")
    print("The first two digits stand for the company.\na: arrival\nd: departure\nn: names\n")
    commands = available_commands[command](available_commands)
    for i, key in enumerate(commands):
        print(f"{i + 1} - {key}")

# USED WHEN HELP COMMAND IS TYPED ON
def get_commands(data: dict) -> dict.keys:
    return data.keys()

# USED WHEN NAMES COMMAND IS TYPED IN
def get_names(data: str) -> list[str]:
    """
    This will serve to create the files
    :param data: data structure
    :return: a list of strings, that is the names
    """
    return [row.split(",")[0] for row in data.strip().split("\n")]

def print_names(names):
    for i, name in enumerate(names):
        print(f"{i+1} - {name}")

# USED WHEN FLIGHT COMMAND IS TYPED IN
def get_flights(data: str):
    return [row.split(",")[2] for row in data.split("\n")]

def print_flights(flights, service_type):

    if service_type[3:] == "departures":
        return colored_print("Departures do not provide flights we need to check on.", "yellow")
    for i, flight in enumerate(flights):
        print(f"{i + 1} - {flight}")

def correct_flights(data, company, service_type):
    def to_12h_format(time_str):
        """Convert a 24h time string (e.g., '16:45') to 12h format with AM/PM."""
        try:
            # Parse the 24h time
            time_obj = datetime.strptime(time_str, "%H:%M")
            # Format as 12h with am/pm (lowercase), or use %I:%M %p for uppercase
            return time_obj.strftime("%-I:%M %p").lower()  # For Unix/Linux/macOS
        except ValueError:
            return "Invalid time format"

    if service_type == "departures":
        return colored_print("Departures do not provide flights we need to check on.", "yellow")

    services = data.strip().split("\n")
    updated_data = []
    current_service = []

    for service in services:
        service = service.split(",")
        service[1] = flight_check(service[2], service_type)
        for col in service:
            if col is not None:
                current_service.append(col)
            else:
                current_service.append("Not found")

        updated_data.append(','.join(current_service))
        current_service = []

    return '\n'.join([row for row in updated_data])

# USED WHEN WRITE COMMAND IS TYPED ON
def write_to_directory(path: str, file: str, content: str, header: str):

    with open(f"{path}/{file}.csv", 'w') as fl:
        fl.write(f"{header}\n" + content)
    colored_print("operation completed", "green")


# EXTRA STEP: create pdfs. USED WHEN PDFS COMMAND IS TYPED ON
def create_pdfs(data, command, split_file: str, path):
    names = get_names(data[command[0]][command[1]])

    try:
        reader = PdfReader(f"{path}/{split_file.upper()}_SPLIT.pdf")  # this is the way I save my files. command + split suffix
    except FileNotFoundError as e:
        return colored_print(f"YO! , {e}", "red")

    if len(reader.pages) > len(names):
        return colored_print(
                "ERROR: Zero correlation between the pdf length and the available names. "
                "are you sure you are using the correct pdf?",
                "red"
            )

    for i in range(len(reader.pages)):
        writer = PdfWriter()
        writer.add_page(reader.pages[i])
        with open(f"{path}/{names[i]} - {command[0]}.pdf", "wb") as output_file:
            writer.write(output_file)
        colored_print("Operation Completed! ", "green")