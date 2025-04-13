"""
import os

path = os.path.expanduser('~/Desktop')
# os.makedirs(path, exist_ok=True)

def mk_dir():
    os.makedirs(f'{path}', exist_ok=True)

def create_file():
    with open(f"{path}/new_text_file.txt", 'w') as file:
        file.write("Hello")

def append_to_file():
    with open(f"{path}/new_text_file.text", 'a') as file:
        file.write("I am so beautiful")

def rename_file():
    os.rename("{BASE_DIR}/new_text_file", f"{path}/old_text_file")

def leave() -> str:
    return "exit"

AVAILABLE_COMMANDS = {
    "mkdir": lambda: mk_dir(),
    "create": lambda: create_file(),
    "append": lambda: append_to_file(),
    "rename": lambda: rename_file(),
    "exit": lambda: leave()
}

def main():
    while True:

        command = input("Enter a command: ")
        if command in AVAILABLE_COMMANDS.keys():
            AVAILABLE_COMMANDS[command]()
        else:
            print("That command is not available")

        if command == "exit":
            break

main()
"""