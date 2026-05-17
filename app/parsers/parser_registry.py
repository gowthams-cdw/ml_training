from pathlib import Path

from app.parsers.bash_parser import (
    BashParser,
)
from app.parsers.dotnet_parser import (
    DotNetParser,
)
from app.parsers.go_parser import (
    GoParser,
)
from app.parsers.java_parser import (
    JavaParser,
)
from app.parsers.js_parser import (
    JSParser,
)
from app.parsers.python_parser import (
    PythonParser,
)


class ParserRegistry:
    """
    Routes files to correct parser.
    """

    def __init__(self) -> None:
        self.parsers = {
            ".py": PythonParser(),
            ".js": JSParser(),
            ".ts": JSParser(),
            ".jsx": JSParser(),
            ".tsx": JSParser(),
            ".java": JavaParser(),
            ".go": GoParser(),
            ".cs": DotNetParser(),
            ".sh": BashParser(),
        }

    def get_parser(
        self,
        file_path: Path,
    ):
        return self.parsers.get(file_path.suffix.lower())
