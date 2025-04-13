
def get_commands(data: dict) -> dict.keys:
    return data.keys()

def get_columns(data: str):
    split_data = data.split("\n")
    return split_data[0], "\n".join(split_data[1:])

def get_names(data: str) -> list[str]:
    """
    This will serve to create the files
    :param data: data structure
    :return: a list of strings, that is the names
    """
    names = []
    for row in data.strip().split("\n"):
        names.append(row.split(",")[0])
    return names

def write_to_directory(path: str, file: str, content: str, header: str):

    with open(f"{path}/{file}.csv", 'w') as fl:
        fl.write(f"{header}\n" + content)
    print("operation completed")

def print_help(command, available_commands):
    print("Available Commands: ")
    print("The first two digits stand for the company.\na: arrival\nd: departure\nn: names\n")
    commands = available_commands[command](available_commands)
    for i, key in enumerate(commands):
        print(f"{i + 1} - {key}")