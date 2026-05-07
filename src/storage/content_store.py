class ContentStore:
    """
    A simple in-memory content store that allows reading, writing, and deleting content based on a unique content ID.
    """
    def __init__(self) -> None:
        self._store: dict[str, str] = {}

    def read_content(self, content_id: str) -> str:
        """
        read the content associated with the specified content_id from the content store. If the content_id exists in the store, the function returns the corresponding content as a string. If the content_id does not exist in the store, it raises a KeyError indicating that the content was not found.

        Args:
            content_id: A string representing the unique identifier of the content to be read from the content store.

        Returns: If the content with the specified content_id exists in the content store, the function returns the corresponding content as a string. If the content_id does not exist in the store, it raises a KeyError indicating that the content was not found.

        """
        return self._store[content_id]

    def write_content(self, content_id: str, content: str) -> None:
        """
        write the specified content to the content store with the associated content_id. If the content_id already exists in the store, it will overwrite the existing content with the new content provided. If the content_id does not exist in the store, it will create a new entry in the store with the specified content_id and content.

        Args:
            content_id: A string representing the unique identifier of the content to be written to the content store.
            content: A string representing the content to be stored in the content store associated with the specified content_id.
        """
        self._store[content_id] = content

    def delete_content(self, content_id: str) -> None:
        """
        delete the content associated with the specified content_id from the content store. If the content_id exists in the store, it will remove the corresponding entry from the store. If the content_id does not exist in the store, it raises a KeyError indicating that the content was not found.

        Args:
            content_id: A string representing the unique identifier of the content to be deleted from the content store.
        """
        del self._store[content_id]
