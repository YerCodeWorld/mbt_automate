from pypdf import PdfReader, PdfWriter

# I could use the console purely on white but meh I like this better
def colored_print(message: str, color):
    colors = {
        "red": 30,
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

# USED WHEN FLIGHT COMMAND IS TYPED IN
def get_flights(data: str):
    return [row.split(",")[2] for row in data.strip().split("\n")]

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