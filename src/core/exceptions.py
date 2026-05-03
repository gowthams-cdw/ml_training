class FileSystemError(Exception):
    pass

class DuplicateDirectoryError(FileSystemError):
    pass

class DuplicateFileError(FileSystemError):
    pass

class FileNotFoundError(FileSystemError):
    pass

class InvalidUsage(FileSystemError):
    pass
