from dataclasses import dataclass, field


@dataclass
class DirectoryNode:
    """
    This class represents a directory in the file system. It contains information about the directory's name, its parent directory, its subdirectories, and the files it contains.

    Attributes:
        id: A unique identifier for the directory, typically generated using a UUID.
        name: The name of the directory.
        parent: A reference to the parent directory node. This is None
        subdirectories: A dictionary mapping subdirectory names to their corresponding DirectoryNode instances. This allows for easy access to subdirectories within the directory.
        files: A dictionary mapping file names to their content. This allows for easy access to files within the directory and their associated content.
    """

    id: str
    name: str

    parent: "DirectoryNode | None"

    subdirectories: dict[str, "DirectoryNode"] = field(default_factory=dict)

    files: dict[str, str] = field(default_factory=dict)
