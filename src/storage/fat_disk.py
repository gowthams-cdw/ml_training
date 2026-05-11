from __future__ import annotations

# FAT sentinel values
FAT_FREE: int = 0x00000000
FAT_EOF: int = 0x0FFFFFFF

# Disk geometry
CLUSTER_SIZE: int = 512
TOTAL_CLUSTERS: int = 4096


class DiskFullError(Exception):
    """Raised when the FAT disk has no free clusters left."""

    pass


class FATDisk:
    """
    In-memory FAT disk.

    Attributes:
    _data : bytearray
        The flat "disk surface" — TOTAL_CLUSTERS × CLUSTER_SIZE bytes.
    _fat  : list[int]
        The File Allocation Table — one 32-bit entry per cluster.
        Values are FAT_FREE, FAT_EOF, or the index of the next cluster.
    """

    def __init__(
        self,
        cluster_size: int = CLUSTER_SIZE,
        total_clusters: int = TOTAL_CLUSTERS,
    ) -> None:
        self.cluster_size = cluster_size
        self.total_clusters = total_clusters
        self._data = bytearray(cluster_size * total_clusters)
        self._fat: list[int] = [FAT_FREE] * total_clusters

    def _cluster_offset(self, index: int) -> int:
        """Return the byte offset of cluster index in _data."""
        return index * self.cluster_size

    def _read_cluster(self, index: int) -> bytes:
        """Read the raw bytes of cluster index."""
        off = self._cluster_offset(index)
        return bytes(self._data[off : off + self.cluster_size])

    def _write_cluster(self, index: int, data: bytes) -> None:
        """Write data into cluster index, zero-padding if shorter."""
        off = self._cluster_offset(index)
        padded = data.ljust(self.cluster_size, b"\x00")
        self._data[off : off + self.cluster_size] = padded[: self.cluster_size]

    # 0 media type byte
    # 1 error/dirty flag byte
    RESERVED_CLUSTERS: int = 2

    def _find_free_cluster(self) -> int:
        """Return the index of the first free cluster, or raise DiskFullError."""
        for i in range(self.RESERVED_CLUSTERS, len(self._fat)):
            if self._fat[i] == FAT_FREE:
                return i
        raise DiskFullError(
            f"FAT disk is full ({self.total_clusters} clusters, "
            f"{self.total_clusters * self.cluster_size} bytes total)."
        )

    def _allocate_chain(self, n_clusters: int) -> int:
        """
        Allocate a chain of n_clusters free clusters.

        Returns the index of the first cluster in the chain.
        The FAT is updated so each cluster points to the next,
        and the last cluster is marked FAT_EOF.
        """
        if n_clusters == 0:
            raise ValueError("Must allocate at least 1 cluster.")

        # Gather free cluster indices up-front to avoid partial allocation
        free: list[int] = []
        for i in range(self.RESERVED_CLUSTERS, len(self._fat)):
            if self._fat[i] == FAT_FREE:
                free.append(i)
            if len(free) == n_clusters:
                break

        if len(free) < n_clusters:
            raise DiskFullError(
                f"Not enough free clusters: need {n_clusters}, have {len(free)}."
            )

        # Link the chain
        for k in range(len(free) - 1):
            self._fat[free[k]] = free[k + 1]
        self._fat[free[-1]] = FAT_EOF

        return free[0]

    def _free_chain(self, start: int) -> None:
        """Mark every cluster in the chain starting at start as FAT_FREE."""
        current = start
        while current not in (FAT_FREE, FAT_EOF):
            nxt = self._fat[current]
            self._fat[current] = FAT_FREE
            self._write_cluster(current, b"") # zero out the cluster clear
            current = nxt

    def _follow_chain(self, start: int) -> list[int]:
        """Return the ordered list of cluster indices in the chain."""
        chain: list[int] = []
        current = start
        while current not in (FAT_FREE, FAT_EOF):
            chain.append(current)
            current = self._fat[current]
        return chain

    def write(self, content: str) -> int:
        """
        Write *content* to disk and return the start-cluster index.

        The number of clusters consumed is ceil(len(bytes) / cluster_size),
        with a minimum of 1 cluster (so even empty files claim a slot).
        """
        raw = content.encode("utf-8")
        n_clusters = max(1, -(-len(raw) // self.cluster_size))

        start = self._allocate_chain(n_clusters)
        chain = self._follow_chain(start)

        for k, cluster_idx in enumerate(chain):
            chunk = raw[k * self.cluster_size : (k + 1) * self.cluster_size]
            self._write_cluster(cluster_idx, chunk)

        return start

    def read(self, start: int) -> str:
        """
        Read and return the content stored in the chain beginning at *start*.
        """
        chain = self._follow_chain(start)
        raw = b"".join(self._read_cluster(idx) for idx in chain)
        return raw.rstrip(b"\x00").decode("utf-8")

    def delete(self, start: int) -> None:
        """Free all clusters in the chain beginning at *start*."""
        self._free_chain(start)

    def free_clusters(self) -> int:
        """Return the number of unallocated clusters."""
        return sum(1 for e in self._fat if e == FAT_FREE)

    def used_clusters(self) -> int:
        """Return the number of allocated clusters."""
        return self.total_clusters - self.free_clusters()

    def free_bytes(self) -> int:
        return self.free_clusters() * self.cluster_size

    def used_bytes(self) -> int:
        return self.used_clusters() * self.cluster_size

    def capacity_bytes(self) -> int:
        return self.total_clusters * self.cluster_size

    def disk_stats(self) -> dict:
        """Return a human-readable dict of disk usage statistics."""
        return {
            "total_clusters": self.total_clusters,
            "cluster_size_b": self.cluster_size,
            "capacity_b": self.capacity_bytes(),
            "used_clusters": self.used_clusters(),
            "free_clusters": self.free_clusters(),
            "used_b": self.used_bytes(),
            "free_b": self.free_bytes(),
            "utilization_pct": round(
                100 * self.used_clusters() / self.total_clusters, 2
            ),
        }

    def to_dict(self) -> dict:
        """Serialize the disk to a JSON-safe dict."""
        return {
            "cluster_size": self.cluster_size,
            "total_clusters": self.total_clusters,
            # Store only non-free FAT entries to save space
            "fat": {str(i): v for i, v in enumerate(self._fat) if v != FAT_FREE},
            # Store only non-zero clusters to save space
            "clusters": {
                str(i): self._read_cluster(i).hex()
                for i in range(self.total_clusters)
                if any(
                    self._data[
                        self._cluster_offset(i) : self._cluster_offset(i)
                        + self.cluster_size
                    ]
                )
            },
        }

    @classmethod
    def from_dict(cls, data: dict) -> "FATDisk":
        """Deserialize a disk previously saved with to_dict()."""
        disk = cls(
            cluster_size=data["cluster_size"],
            total_clusters=data["total_clusters"],
        )
        for idx_str, val in data["fat"].items():
            disk._fat[int(idx_str)] = val
        for idx_str, hex_data in data["clusters"].items():
            raw = bytes.fromhex(hex_data)
            off = disk._cluster_offset(int(idx_str))
            disk._data[off : off + disk.cluster_size] = raw
        return disk
