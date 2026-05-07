from core.exceptions import InvalidUsage
from core.filesystem import FileSystem


def main():
    """
    Entry point for the file system CLI application.
    Raises:
        InvalidUsage: when the user provides an invalid command or insufficient arguments.
    """
    fs = FileSystem()

    while True:
        command = input("fs> ")

        if command == "exit":
            break

        parts = command.split()

        if not parts:
            continue

        action = parts[0]

        try:
            if action == "mkdir":
                if len(parts) == 1:
                    raise InvalidUsage("Invalid Usage: mkdir <folderpath>")
                path = parts[1]

                fs.create_directory(path)
                print(f"{path} created successfully.")
            elif action == "add":
                if len(parts) == 1:
                    raise InvalidUsage("Invalid Usage: add <filepath>")

                content = input("Enter content: ")
                path = parts[1]

                fs.add_file(path, content)
                print(f"{path} created successfully.")
            elif action == "read":
                if len(parts) == 1:
                    raise InvalidUsage("Invalid Usage: read <filepath>")

                path = parts[1]

                print(fs.read_file(path))
            elif action == "ls":
                if len(parts) == 1:
                    raise InvalidUsage("Invalid Usage: ls <folderpath>")

                path = parts[1]

                print(fs.list_directory(path))
            elif action == "rm":
                if len(parts) == 1:
                    raise InvalidUsage("Invalid Usage: rm <filepath>")

                path = parts[1]

                fs.delete_file(path)
                print(f"{path} removed successfully.")
            elif action == "rmdir":
                if len(parts) == 1:
                    raise InvalidUsage("Invalid Usage: rmdir <folderpath>")

                path = parts[1]

                fs.delete_directory(path)
                print(f"{path} removed successfully.")
            elif action == "search":
                if len(parts) == 1:
                    raise InvalidUsage("Invalid Usage: search <word>")

                word = parts[1]

                print(fs.search_results(word))
            elif action == "save":
                if len(parts) == 1:
                    raise InvalidUsage("Invalid Usage: save <filepath>")

                path = parts[1]

                fs.export_state(path)
                print("data exported successfully.")
            elif action == "load":
                if len(parts) == 1:
                    raise InvalidUsage("Invalid Usage: load <filepath>")

                path = parts[1]

                fs.load_state(path)
                print("data loaded successfully.")
            else:
                print("Unknown Commnad!")
        except Exception as error:
            print(f"Error: {error}")


if __name__ == "__main__":
    main()
