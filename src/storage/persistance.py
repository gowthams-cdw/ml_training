from models.directory import DirectoryNode


def serialize_directory(directory: DirectoryNode) -> dict:
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
