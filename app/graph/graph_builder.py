import networkx as nx

from app.core.logger import app_logger


class GraphBuilder:
    """
    Builds dependency graphs.
    """

    def __init__(self) -> None:
        self.graph = nx.DiGraph()

    def build_dependency_graph(
        self,
        dependency_result: dict,
    ) -> nx.DiGraph:
        """
        Build directed dependency graph.
        """

        app_logger.info("Building dependency graph...")

        dependencies = dependency_result.get("dependencies", [])

        for dependency_entry in dependencies:
            source_file = dependency_entry["source_file"]

            imports = dependency_entry["imports"]

            self.graph.add_node(
                source_file,
                type="source_file",
            )

            for imported_module in imports:
                self.graph.add_node(
                    imported_module,
                    type="import",
                )

                self.graph.add_edge(
                    source_file,
                    imported_module,
                    relationship="imports",
                )

        app_logger.success(
            f"Graph created with "
            f"{self.graph.number_of_nodes()} nodes and "
            f"{self.graph.number_of_edges()} edges"
        )

        return self.graph

    def summarize_graph(
        self,
    ) -> dict:
        """
        Return graph metadata summary.
        """

        return {
            "nodes": self.graph.number_of_nodes(),
            "edges": self.graph.number_of_edges(),
            "density": nx.density(self.graph),
        }
