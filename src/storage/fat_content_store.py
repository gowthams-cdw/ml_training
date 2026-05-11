from __future__ import annotations

from storage.fat_disk import FATDisk


class FATContentStore:
    """
    Content store backed by a simulated FAT disk.

    _index : dict[content_id → start_cluster]
        Maps the logical content ID (a UUID string) to the first cluster
        of its FAT chain on the virtual disk.

    _disk : FATDisk
        The underlying block device.
    """

    def __init__(self, disk: FATDisk | None = None) -> None:
        self._disk: FATDisk = disk if disk is not None else FATDisk()
        self._index: dict[str, int] = {}

    def read_content(self, content_id: str) -> str:
        """
        Return the string content associated with *content_id*.

        Raises KeyError if the content_id is unknown (same behaviour as
        the original dict-based store so callers need no changes).
        """
        if content_id not in self._index:
            raise KeyError(f"Content ID '{content_id}' not found in FAT store.")
        start_cluster = self._index[content_id]
        return self._disk.read(start_cluster)

    def write_content(self, content_id: str, content: str) -> None:
        """
        Write *content* to the FAT disk under *content_id*.

        If *content_id* already exists, the old chain is freed first
        (in-place update).
        """
        if content_id in self._index:
            self._disk.delete(self._index[content_id])

        start_cluster = self._disk.write(content)
        self._index[content_id] = start_cluster

    def delete_content(self, content_id: str) -> None:
        """
        Free the FAT chain for *content_id* and remove it from the index.

        Raises KeyError if the content_id is unknown.
        """
        if content_id not in self._index:
            raise KeyError(f"Content ID '{content_id}' not found in FAT store.")
        start_cluster = self._index.pop(content_id)
        self._disk.delete(start_cluster)

    def disk_stats(self) -> dict:
        """Return FAT disk usage statistics."""
        return self._disk.disk_stats()

    def to_dict(self) -> dict:
        return {
            "index": self._index,
            "disk": self._disk.to_dict(),
        }

    @classmethod
    def from_dict(cls, data: dict) -> "FATContentStore":
        disk = FATDisk.from_dict(data["disk"])
        store = cls(disk=disk)
        store._index = {k: int(v) for k, v in data["index"].items()}
        return store
