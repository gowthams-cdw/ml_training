from typing import OrderedDict


class LRUCache:
    def __init__(self, capacity: int = 5) -> None:
        self._capacity: int = capacity
        self._cache: OrderedDict[str, str] = OrderedDict()

    def get(self, content_id: str) -> str | None:
        if content_id not in self._cache:
            return None

        self._cache.move_to_end(content_id)
        return self._cache[content_id]

    def put(self, content_id: str, content: str) -> None:
        if content_id in self._cache:
            self._cache.move_to_end(content_id)

        self._cache[content_id] = content

        if len(self._cache) > self._capacity:
            self._cache.popitem(last=True)

    def remove(self, content_id: str) -> None:
        del self._cache[content_id]
