from pathlib import Path

from app.core.config import (
    IGNORE_DIRS,
    IGNORE_FILES,
    MAX_FILE_SIZE_BYTES,
    SUPPORTED_LANGUAGES,
)
from app.core.logger import app_logger


class FileScanner:
    """
    Scans repository files for supported source code.
    """

    def __init__(self) -> None:
        self.supported_extensions = set(SUPPORTED_LANGUAGES.keys())

    def scan_repository(
        self,
        repository_path: Path,
    ) -> list[Path]:
        """
        Scan repository recursively.
        """

        app_logger.info(f"Scanning repository: {repository_path}")

        discovered_files: list[Path] = []

        for file_path in repository_path.rglob("*"):
            if not file_path.is_file():
                continue

            if self._should_ignore(file_path):
                continue

            if not self._is_supported(file_path):
                continue

            if not self._is_valid_size(file_path):
                continue

            discovered_files.append(file_path)

        app_logger.success(f"Discovered {len(discovered_files)} source files")

        return discovered_files

    # filters
    def _should_ignore(
        self,
        file_path: Path,
    ) -> bool:
        """
        Ignore unwanted files/directories.
        """

        # Ignore filenames
        if file_path.name in IGNORE_FILES:
            return True

        # Ignore directories
        for part in file_path.parts:
            if part in IGNORE_DIRS:
                return True

        return False

    def _is_supported(
        self,
        file_path: Path,
    ) -> bool:
        """
        Check supported file extension.
        """

        return file_path.suffix.lower() in self.supported_extensions

    def _is_valid_size(
        self,
        file_path: Path,
    ) -> bool:
        """
        Prevent massive files.
        """

        try:
            return file_path.stat().st_size <= MAX_FILE_SIZE_BYTES
        except OSError:
            return False
