from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any

from tree_sitter import Parser

from app.core.logger import app_logger


# abstract parser class
# acts as a base for other specific parsers
class BaseParser(ABC):
    """
    Base parser abstraction.
    """

    def __init__(
        self,
        language_name: str,
    ) -> None:

        self.language_name = language_name
        self.parser = Parser()

    def parse_file(
        self,
        file_path: Path,
    ) -> dict[str, Any]:
        """
        Parse source file.
        """

        app_logger.info(f"Parsing file: {file_path}")

        source_code = self._read_file(file_path)

        tree = self._generate_ast(source_code)

        result = {
            "file_path": str(file_path),
            "language": self.language_name,
            "imports": self.extract_imports(
                tree,
                source_code,
            ),
            "functions": self.extract_functions(
                tree,
                source_code,
            ),
            "classes": self.extract_classes(
                tree,
                source_code,
            ),
        }

        return result

    # utils
    def _read_file(
        self,
        file_path: Path,
    ) -> bytes:
        """
        Read source file safely.
        """

        try:
            return file_path.read_bytes()
        except Exception as exc:
            app_logger.error(f"Failed reading file: {file_path} | {exc}")
            return b""

    def _generate_ast(
        self,
        source_code: bytes,
    ):
        """
        Generate syntax tree.
        """

        return self.parser.parse(source_code)

    # abstract methods
    @abstractmethod
    def extract_imports(
        self,
        tree,
        source_code: bytes,
    ) -> list[str]:
        """
        Extract imports/dependencies.
        """

    @abstractmethod
    def extract_functions(
        self,
        tree,
        source_code: bytes,
    ) -> list[dict]:
        """
        Extract functions/methods.
        """

    @abstractmethod
    def extract_classes(
        self,
        tree,
        source_code: bytes,
    ) -> list[dict]:
        """
        Extract classes/types.
        """
