from models.directory import DirectoryNode


def serialize_directory(directory: DirectoryNode) -> dict:
    """
    serialize a DirectoryNode object into a dictionary format that can be easily stored or transmitted. The function recursively serializes the directory and its subdirectories, creating a nested structure in the resulting dictionary.

    Args:
        directory: A DirectoryNode object representing the directory to be serialized. This object contains information about the directory's ID, name, files, and subdirectories.

    Returns: A dictionary representing the serialized form of the DirectoryNode. The dictionary includes the directory's ID, name, list of files, and a nested dictionary of subdirectories where each key is the name of the subdirectory and the value is the serialized form of that subdirectory.
    """
    serialized_children = {}

    for name, child in directory.subdirectories.items():
        serialized_children[name] = serialize_directory(child)

    return {
        "id": directory.id,
        "name": directory.name,
        "files": directory.files,
        "subdirectories": serialized_children,
    }


def deserialize_directory(
    data: dict, parent: DirectoryNode | None = None
) -> DirectoryNode:
    """
    deserialize a dictionary representation of a directory back into a DirectoryNode object. The function recursively deserializes the directory and its subdirectories, reconstructing the original directory structure.

    Args:
        data: A dictionary representing the serialized form of a DirectoryNode. This dictionary should include the directory's ID, name, list of files, and a nested dictionary of subdirectories where each key is the name of the subdirectory and the value is the serialized form of that subdirectory.
        parent: An optional DirectoryNode object representing the parent directory of the directory being deserialized. This parameter is used to establish the parent-child relationship between directories during the deserialization process. If not provided, it defaults to None, indicating that the deserialized directory is a top-level directory without a parent.

    Returns: A DirectoryNode object representing the deserialized directory. The returned DirectoryNode will have its ID, name, files, and subdirectories populated based on the information provided in the input dictionary. The parent-child relationships between directories will also be established based on the provided parent parameter.
    """
    node = DirectoryNode(
        id=data["id"],
        name=data["name"],
        parent=parent,
        subdirectories={},
        files=data["files"],
    )

    for name, child in data["subdirectories"].items():
        node.subdirectories[name] = deserialize_directory(child, node)

    return node
