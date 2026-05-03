from models.metadata import FileMetadata


class MetadataStore:
    def __init__(self) -> None:
        self._store: dict[str, FileMetadata] = {}

    def add_metadata(self, metadata: FileMetadata) -> None:
        file_id = metadata.file_id

        self._store[file_id] = metadata

    def get_metadata(self, file_id) -> FileMetadata:
        return self._store[file_id]

    def del_metadata(self, file_id) -> None:
        del self._store[file_id]
