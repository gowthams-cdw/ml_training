import hashlib
from pathlib import Path
from typing import Any

from diskcache import Cache

from app.core.config import (
    CACHE_DIR,
)
from app.core.logger import app_logger


class CacheManager:
    """
    Persistent cache manager.
    """

    def __init__(self) -> None:
        self.cache = Cache(
            str(CACHE_DIR)
        )

    def generate_file_hash(
        self,
        file_path: Path,
    ) -> str:
        """
        Generate deterministic file hash.
        """

        sha256 = hashlib.sha256()

        try:
            with open(
                file_path,
                "rb",
            ) as file:
                while chunk := file.read(8192):
                    sha256.update(chunk)

            return sha256.hexdigest()

        except Exception as exc:
            app_logger.error(
                f"Hash generation failed: "
                f"{file_path} | {exc}"
            )

            return ""

    # utils
    def get(
        self,
        key: str,
    ) -> Any:
        """
        Retrieve cached value.
        """

        return self.cache.get(key)

    def set(
        self,
        key: str,
        value: Any,
    ) -> None:
        """
        Store cache value.
        """

        self.cache.set(
            key,
            value,
        )

    def exists(
        self,
        key: str,
    ) -> bool:
        """
        Check cache existence.
        """

        return key in self.cache

    # parser cache
    def get_parsed_result(
        self,
        file_hash: str,
    ) -> dict | None:
        """
        Get cached parsed AST result.
        """

        return self.get(
            f"parsed::{file_hash}"
        )

    def store_parsed_result(
        self,
        file_hash: str,
        parsed_result: dict,
    ) -> None:
        """
        Store parsed AST result.
        """

        self.set(
            f"parsed::{file_hash}",
            parsed_result,
        )
