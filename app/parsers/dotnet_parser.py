from tree_sitter_language_pack import get_language

from app.parsers.base_parser import BaseParser


class DotNetParser(BaseParser):
    def __init__(self) -> None:
        super().__init__(language_name="dotnet")
        language = get_language("csharp")
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

            if node.type == "using_directive":
                text = source_code[node.start_byte : node.end_byte].decode(
                    "utf-8",
                    errors="ignore",
                )

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

            if node.type == "method_declaration":
                functions.append(
                    {
                        "name": "method",
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
                classes.append(
                    {
                        "name": "class",
                        "start_line": (node.start_point[0] + 1),
                        "end_line": (node.end_point[0] + 1),
                    }
                )

            stack.extend(node.children)

        return classes
