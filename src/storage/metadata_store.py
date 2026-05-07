from models.metadata import FileMetadata


class MetadataStore:
    """
    MetadataStore is a simple in-memory store for file metadata. It provides methods to add, retrieve, and delete metadata based on file IDs. The metadata is stored in a dictionary where the keys are file IDs and the values are FileMetadata objects.
    """

    def __init__(self) -> None:
        self._store: dict[str, FileMetadata] = {}

    def add_metadata(self, metadata: FileMetadata) -> None:
        """
        add the provided FileMetadata object to the metadata store. The metadata is stored in a dictionary where the key is the file ID extracted from the FileMetadata object and the value is the FileMetadata object itself. If a metadata entry with the same file ID already exists in the store, it will be overwritten with the new metadata provided.

        Args:
            metadata: A FileMetadata object containing the metadata information to be added to the metadata store. The FileMetadata object should have a file_id attribute that uniquely identifies the file associated with the metadata.
        """
        file_id = metadata.file_id

        self._store[file_id] = metadata

    def get_metadata(self, file_id: str) -> FileMetadata:
        """
        retrieve the FileMetadata object associated with the specified file_id from the metadata store. If a metadata entry with the given file_id exists in the store, it returns the corresponding FileMetadata object. If no metadata entry with the specified file_id is found in the store, it raises a KeyError indicating that the metadata was not found.

        Args:
            file_id: A string representing the unique identifier of the file for which the metadata is to be retrieved. This file_id should correspond to the file_id attribute of a FileMetadata object stored in the metadata store.

        Returns: If a metadata entry with the specified file_id exists in the metadata store, the function returns the corresponding FileMetadata object. If no metadata entry with the specified file_id is found in the store, it raises a KeyError indicating that the metadata was not found.
        """
        return self._store[file_id]

    def del_metadata(self, file_id: str) -> None:
        """
        delete the metadata entry associated with the specified file_id from the metadata store. If a metadata entry with the given file_id exists in the store, it will be removed from the store. If no metadata entry with the specified file_id is found in the store, it raises a KeyError indicating that the metadata was not found.

        Args:
            file_id: A string representing the unique identifier of the file for which the metadata is to be deleted. This file_id should correspond to the file_id attribute of a FileMetadata object stored in the metadata store.
        """
        del self._store[file_id]
