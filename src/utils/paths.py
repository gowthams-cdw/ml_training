from models.directory import DirectoryNode


def split_path(path: str) -> list[str]:
    """
    Utility function to split a file path into its components. It removes leading and trailing slashes and splits the path by the "/" delimiter.

    Args:
        path: A string representing the file path to be split.

    Returns: A list of strings, where each string is a component of the file path.

    """
    cleaned = path.strip("/")

    # what cleaned becomes empty str
    # case 1: / => ""
    # case 2: " /" => " "
    if not cleaned:
        return []

    return cleaned.split("/")


def resolve_path(root: DirectoryNode, path: str) -> DirectoryNode:
    """
    Utility function to resolve a file path to its corresponding DirectoryNode in the file system. It traverses the directory structure starting from the root node and follows the path components to find the target directory.

    Args:
        root: The root DirectoryNode from which to start the path resolution. This is typically the top-level directory of the file system.
        path: A string representing the file path to be resolved. The path should be in the format of "/dir1/dir2/dir3", where each component represents a directory in the file system.

    Returns: The DirectoryNode corresponding to the target directory specified by the path. If the path is valid and exists in the file system, the function will return the DirectoryNode for that directory. If the path is invalid (e.g., if any component of the path does not exist in the directory structure), the function will raise an Exception indicating that the directory is invalid.

    Raises:
        Exception: If the path is invalid (e.g., if any component of the path does not exist in the directory structure), an Exception will be raised with the message "Invalid Directory." This indicates that the specified path cannot be resolved to a valid directory in the file system.
    """
    if path == "/":
        return root

    parts = split_path(path)

    current = root

    for part in parts:
        if part not in current.subdirectories:
            raise Exception("Invalid Directory.")

        current = current.subdirectories[part]

    return current
