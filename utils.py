from pypdf import PdfReader, PdfWriter

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

# USED WHEN WRITE COMMAND IS TYPED ON
def write_to_directory(path: str, file: str, content: str, header: str):

    with open(f"{path}/{file}.csv", 'w') as fl:
        fl.write(f"{header}\n" + content)
    print("operation completed")


# EXTRA STEP: create pdfs. USED WHEN PDFS COMMAND IS TYPED ON
def create_pdfs(data, command, path):
    names = get_names(data[command[0]][command[1]])
    reader = PdfReader(f"{path}/TO_SPLIT.pdf")

    if len(reader.pages) > len(names):
        return print("ERROR: Zero correlation between the pdf length and the available names. are you sure you are using the correct pdf?")

    for i in range(len(reader.pages)):
        writer = PdfWriter()
        writer.add_page(reader.pages[i])
        with open(f"{path}/{names[i]} - {command[0]}.pdf", "wb") as output_file:
            writer.write(output_file)
        print("Operation completed")