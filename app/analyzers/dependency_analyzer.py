from collections import defaultdict

from app.core.logger import app_logger


class DependencyAnalyzer:
    """
    Analyze repository dependencies and relationships.
    """

    def __init__(self) -> None:
        self.dependency_graph = defaultdict(set)

    def analyze(
        self,
        parsed_results: list[dict],
    ) -> dict:
        """
        Analyze parsed source metadata.
        """

        app_logger.info("Starting dependency analysis...")

        dependencies = []

        for parsed_file in parsed_results:
            file_path = parsed_file["file_path"]

            imports = parsed_file.get("imports", [])

            cleaned_imports = self._normalize_imports(imports)

            dependency_entry = {
                "source_file": file_path,
                "imports": cleaned_imports,
            }

            dependencies.append(dependency_entry)

            self.dependency_graph[file_path].update(cleaned_imports)

        result = {
            "dependencies": dependencies,
            "graph": dict(self.dependency_graph),
        }

        app_logger.success("Dependency analysis completed")

        return result

    # utils
    def _normalize_imports(
        self,
        imports: list[str],
    ) -> list[str]:
        """
        Normalize import statements.
        """

        normalized: list[str] = []

        for import_stmt in imports:
            cleaned = (
                import_stmt.replace("import ", "")
                .replace("from ", "")
                .replace("\n", " ")
                .strip()
            )

            normalized.append(cleaned)

        return sorted(set(normalized))
