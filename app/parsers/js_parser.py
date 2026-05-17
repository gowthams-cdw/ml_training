from tree_sitter_language_pack import get_language

from app.parsers.base_parser import BaseParser


class JSParser(BaseParser):
    """
    JavaScript / TypeScript parser.
    """

    def __init__(self) -> None:
        super().__init__(language_name="javascript")
        language = get_language("javascript")
        self.parser.language = language

    # overriding abstract methods from base parser
    def extract_imports(
        self,
        tree,
        source_code: bytes,
    ) -> list[str]:

        imports = []

        stack = [tree.root_node]

        while stack:
            node = stack.pop()

            if node.type in (
                "import_statement",
                "call_expression",
            ):
                text = source_code[node.start_byte : node.end_byte].decode(
                    "utf-8",
                    errors="ignore",
                )

                if "require(" in text or text.startswith("import "):
                    imports.append(text.strip())

            stack.extend(node.children)

        return imports

    def extract_functions(
        self,
        tree,
        source_code: bytes,
    ) -> list[dict]:

        functions = []

        stack = [tree.root_node]

        while stack:
            node = stack.pop()

            if node.type in (
                "function_declaration",
                "method_definition",
            ):
                name = self._extract_name(
                    node,
                    source_code,
                )

                functions.append(
                    {
                        "name": name,
                        "start_line": (node.start_point[0] + 1),
                        "end_line": (node.end_point[0] + 1),
                    }
                )

            stack.extend(node.children)

        return functions

    def extract_classes(
        self,
        tree,
        source_code: bytes,
    ) -> list[dict]:

        classes = []

        stack = [tree.root_node]

        while stack:
            node = stack.pop()

            if node.type == "class_declaration":
                name = self._extract_name(
                    node,
                    source_code,
                )

                classes.append(
                    {
                        "name": name,
                        "start_line": (node.start_point[0] + 1),
                        "end_line": (node.end_point[0] + 1),
                    }
                )

            stack.extend(node.children)

        return classes

    # utils
    def _extract_name(
        self,
        node,
        source_code: bytes,
    ) -> str:

        for child in node.children:
            if child.type == "identifier":
                return source_code[child.start_byte : child.end_byte].decode(
                    "utf-8",
                    errors="ignore",
                )

        return "unknown"
