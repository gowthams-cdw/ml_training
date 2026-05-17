from pathlib import Path

import networkx as nx

from app.core.config import (
    DIAGRAM_OUTPUT_DIR,
)
from app.core.logger import app_logger


class MermaidGenerator:
    """
    Generate Mermaid architecture diagrams.
    """

    def __init__(self) -> None:
        pass

    def generate_dependency_diagram(
        self,
        dependency_graph: nx.DiGraph,
        output_name: str = "dependency_graph",
    ) -> Path:
        """
        Generate Mermaid dependency graph.
        """

        app_logger.info("Generating Mermaid diagram...")

        mermaid_lines = ["graph TD"]

        node_mapping: dict[str, str] = {}

        for index, node in enumerate(dependency_graph.nodes()):
            safe_id = f"N{index}"

            node_mapping[node] = safe_id

            label = self._sanitize_label(node)

            mermaid_lines.append(f'    {safe_id}["{label}"]')

        for source, target in dependency_graph.edges():
            source_id = node_mapping[source]
            target_id = node_mapping[target]

            mermaid_lines.append(f"    {source_id} --> {target_id}")

        mermaid_content = "\n".join(mermaid_lines)

        output_path = DIAGRAM_OUTPUT_DIR / f"{output_name}.md"

        output_path.write_text(
            f"```mermaid\n{mermaid_content}\n```\n",
            encoding="utf-8",
        )

        app_logger.success(f"Mermaid diagram generated: {output_path}")

        return output_path

    # utils
    def _sanitize_label(
        self,
        node_name: str,
    ) -> str:
        """
        Clean Mermaid labels.
        """

        cleaned = str(node_name).replace('"', "").replace("\n", " ").replace("\\", "/")

        return cleaned[-60:]
