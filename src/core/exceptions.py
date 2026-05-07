class FileSystemError(Exception):
    """Base class for all file system related errors."""
    pass

class DuplicateDirectoryError(FileSystemError):
    """Raised when a directory with the same name already exists."""
    pass

class DuplicateFileError(FileSystemError):
    """Raised when a file with the same name already exists."""
    pass

class FileNotFoundError(FileSystemError):
    """Raised when a file or directory is not found."""
    pass

class InvalidUsage(FileSystemError):
    """Raised when the CLI command is used incorrectly."""
    pass
