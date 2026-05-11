from typing import OrderedDict


class LRUCache:
    """
    A simple implementation of a Least Recently Used (LRU) cache.
    """
    def __init__(self, capacity: int = 5) -> None:
        self._capacity: int = capacity
        self._cache: OrderedDict[str, str] = OrderedDict()

    def get(self, content_id: str) -> str | None:
        """
        get the content from the cache if it exists, otherwise return None. If the content is found in the cache, it is marked as recently used by moving it to the end of the OrderedDict.

        Args:
            content_id: A string representing the unique identifier of the content to be retrieved from the cache.

        Returns: If the content with the specified content_id exists in the cache, the function returns the corresponding content as a string. If the content does not exist in the cache, the function returns None.

        """
        if content_id not in self._cache:
            return None

        self._cache.move_to_end(content_id)
        return self._cache[content_id]

    def put(self, content_id: str, content: str) -> None:
        """
        add content to the cache with the specified content_id. If the content_id already exists in the cache, it updates the content and marks it as recently used by moving it to the end of the OrderedDict. If adding the new content exceeds the cache's capacity, the least recently used item (the first item in the OrderedDict) is removed from the cache.

        Args:
            content_id: A string representing the unique identifier of the content to be added to the cache.
            content: A string representing the content to be stored in the cache associated with the specified content_id.
        """
        if content_id in self._cache:
            self._cache.move_to_end(content_id)

        self._cache[content_id] = content

        if len(self._cache) > self._capacity:
            self._cache.popitem(last=True)

    def remove(self, content_id: str) -> None:
        """
        remove the content with the specified content_id from the cache if it exists. If the content_id is found in the cache, it is removed from the OrderedDict.

        Args:
            content_id: A string representing the unique identifier of the content to be removed from the cache.
        """
        if content_id in self._cache:
            del self._cache[content_id]
