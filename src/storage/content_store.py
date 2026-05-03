class ContentStore:
    def __init__(self) -> None:
        self._store: dict[str, str] = {}

    def read_content(self, content_id) -> str:
        return self._store[content_id]

    def write_content(self, content_id, content) -> None:
        self._store[content_id] = content

    def delete_content(self, content_id) -> None:
        del self._store[content_id]
