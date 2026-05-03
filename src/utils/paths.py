from models.directory import DirectoryNode


def split_path(path: str) -> list[str]:
    cleaned = path.strip("/")

    # what cleaned becomes empty str
    # case 1: / => ""
    # case 2: " /" => " "
    if not cleaned:
        return []

    return cleaned.split("/")


def resolve_path(root: DirectoryNode, path: str) -> DirectoryNode:
    if path == "/":
        return root

    parts = split_path(path)

    current = root

    for part in parts:
        if part not in current.subdirectories:
            raise Exception("Invalid Directory.")

        current = current.subdirectories[part]

    return current
