from tree_sitter_language_pack import get_language

from app.parsers.base_parser import BaseParser


class PythonParser(BaseParser):
    """
    Python AST parser using Tree-sitter.
    """

    def __init__(self) -> None:
        super().__init__(language_name="python")
        language = get_language("python")
        self.parser.language = language

    # overriding abstract methods from base parser
    def extract_imports(
        self,
        tree,
        source_code: bytes,
    ) -> list[str]:
        """
        Extract Python imports.
        """

        imports: list[str] = []

        root_node = tree.root_node

        stack = [root_node]

        while stack:
            node = stack.pop()

            if node.type in (
                "import_statement",
                "import_from_statement",
            ):
                import_text = source_code[node.start_byte : node.end_byte].decode(
                    "utf-8",
                    errors="ignore",
                )

                imports.append(import_text.strip())

            stack.extend(node.children)

        return imports

    def extract_functions(
        self,
        tree,
        source_code: bytes,
    ) -> list[dict]:
        """
        Extract Python functions.
        """

        functions: list[dict] = []

        root_node = tree.root_node

        stack = [root_node]

        while stack:
            node = stack.pop()

            if node.type == "function_definition":
                function_name = self._extract_function_name(
                    node,
                    source_code,
                )

                functions.append(
                    {
                        "name": function_name,
                        "start_line": node.start_point[0] + 1,
                        "end_line": node.end_point[0] + 1,
                    }
                )

            stack.extend(node.children)

        return functions

    def extract_classes(
        self,
        tree,
        source_code: bytes,
    ) -> list[dict]:
        """
        Extract Python classes.
        """

        classes: list[dict] = []

        root_node = tree.root_node

        stack = [root_node]

        while stack:
            node = stack.pop()

            if node.type == "class_definition":
                class_name = self._extract_class_name(
                    node,
                    source_code,
                )

                classes.append(
                    {
                        "name": class_name,
                        "start_line": node.start_point[0] + 1,
                        "end_line": node.end_point[0] + 1,
                    }
                )

            stack.extend(node.children)

        return classes

    # utils
    def _extract_function_name(
        self,
        node,
        source_code: bytes,
    ) -> str:
        """
        Extract function name.
        """

        for child in node.children:
            if child.type == "identifier":
                return source_code[child.start_byte : child.end_byte].decode(
                    "utf-8",
                    errors="ignore",
                )

        return "unknown_function"

    def _extract_class_name(
        self,
        node,
        source_code: bytes,
    ) -> str:
        """
        Extract class name.
        """

        for child in node.children:
            if child.type == "identifier":
                return source_code[child.start_byte : child.end_byte].decode(
                    "utf-8",
                    errors="ignore",
                )

        return "unknown_class"
