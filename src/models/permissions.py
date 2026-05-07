from dataclasses import dataclass


@dataclass
class Permissions:
    """
    This class represents the permissions associated with a file in the file system. It defines the access control settings for the file, specifying who can read, write, or delete the file.

    Attributes:
        read: A boolean value indicating whether the file can be read. If set to True, users with appropriate permissions can view the contents of the file. If set to False, the file cannot be accessed for reading.
        write: A boolean value indicating whether the file can be written to. If set to True, users with appropriate permissions can modify the contents of the file. If set to False, the file cannot be modified.
        delete: A boolean value indicating whether the file can be deleted. If set to True, users with appropriate permissions can remove the file from the file system. If set to False, the file cannot be deleted.
    """

    read: bool = True
    write: bool = True
    delete: bool = True
