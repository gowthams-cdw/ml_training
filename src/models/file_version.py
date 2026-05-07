from dataclasses import dataclass
from datetime import datetime


@dataclass
class FileVersion:
    """
    This class represents a version of a file in the file system. It contains information about the version's unique identifier, the content identifier it references, the timestamp of when the version was created, and the size of the file at that version.

    Attributes:
        version_id: A unique identifier for the file version, typically generated using a UUID.
        content_id: A reference to the content associated with this version. This could be a hash or identifier that points to the actual content stored in the file system.
        timestamp: The date and time when this version of the file was created. This is typically stored as a datetime object.
        size: The size of the file at this version, typically measured in bytes. This information can be useful for tracking changes in file size across different versions and for managing storage space in the file system.
    """

    version_id: str
    content_id: str
    timestamp: datetime
    size: int
