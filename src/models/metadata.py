from dataclasses import dataclass, field
from datetime import datetime

from models.file_version import FileVersion
from models.permissions import Permissions


@dataclass
class FileMetadata:
    """
    This class represents the metadata of a file in the file system. It contains information about the file's unique identifier, name, content identifier, size, creation and modification timestamps, permissions, and version history.

    Attributes:
        file_id: A unique identifier for the file, typically generated using a UUID.
        name: The name of the file. This is the human-readable name that users interact with when managing files in the file system.
        content_id: A reference to the content associated with the file. This could be a hash or identifier that points to the actual content stored in the file system, allowing for efficient storage and retrieval of file data.
        size: The size of the file, typically measured in bytes. This information is important for managing storage space in the file system and for tracking changes in file size across different versions.
        created_at: The date and time when the file was created. This is typically stored as a datetime object and can be used for tracking the age of the file and for sorting files based on their creation time.
        modified_at: The date and time when the file was last modified. This is typically stored as a datetime object and can be used for tracking changes to the file and for sorting files based on their modification time.
        permissions: An instance of the Permissions class that defines the access control settings for the file. This includes information about who can read, write, or execute the file, and can be used to enforce security policies in the file system.
        versions: A list of FileVersion instances that represent the version history of the file. Each FileVersion contains information about a specific version of the file, including its content identifier, size, creation timestamp, and any relevant metadata. This allows for tracking changes to the file over time and for retrieving previous versions if needed.
    """

    file_id: str
    name: str
    content_id: str

    size: int

    created_at: datetime
    modified_at: datetime

    permissions: Permissions

    versions: list[FileVersion] = field(default_factory=list)
