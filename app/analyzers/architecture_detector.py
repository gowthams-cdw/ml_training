from pathlib import Path

import networkx as nx

from app.core.logger import app_logger


class ArchitectureDetector:
    """
    Detect high-level architecture patterns.
    """

    def __init__(self) -> None:
        pass

    def detect(
        self,
        repository_path: Path,
        detected_stack: dict,
        dependency_graph: nx.DiGraph,
    ) -> dict:
        """
        Main architecture analysis entrypoint.
        """

        app_logger.info("Starting architecture detection...")

        patterns = []

        patterns.extend(self._detect_layered_architecture(repository_path))

        patterns.extend(
            self._detect_microservice_signals(
                repository_path,
                detected_stack,
            )
        )

        patterns.extend(self._detect_api_patterns(detected_stack))

        result = {
            "patterns": sorted(set(patterns)),
            "node_count": (dependency_graph.number_of_nodes()),
            "edge_count": (dependency_graph.number_of_edges()),
        }

        app_logger.success(f"Architecture patterns detected: {result['patterns']}")

        return result

    # architecture detection utils
    def _detect_layered_architecture(
        self,
        repository_path: Path,
    ) -> list[str]:
        """
        Detect common layered structure.
        """

        patterns = []

        expected_dirs = {
            "controllers",
            "services",
            "repositories",
            "models",
        }

        discovered_dirs = {
            path.name.lower() for path in repository_path.rglob("*") if path.is_dir()
        }

        matches = expected_dirs.intersection(discovered_dirs)

        if len(matches) >= 2:
            patterns.append("Layered Architecture")

        return patterns

    def _detect_microservice_signals(
        self,
        repository_path: Path,
        detected_stack: dict,
    ) -> list[str]:
        """
        Detect microservice indicators.
        """

        patterns = []

        docker_files = list(repository_path.rglob("Dockerfile"))

        compose_files = list(repository_path.rglob("docker-compose.yml"))

        frameworks = detected_stack.get("frameworks", [])

        if docker_files and frameworks:
            patterns.append("Containerized Service")

        if len(compose_files) > 0:
            patterns.append("Microservice Orchestration")

        return patterns

    def _detect_api_patterns(
        self,
        detected_stack: dict,
    ) -> list[str]:
        """
        Detect API-oriented architectures.
        """

        patterns = []

        frameworks = detected_stack.get("frameworks", [])

        api_frameworks = {
            "FastAPI",
            "Flask",
            "Django",
            "Express.js",
            "NestJS",
            "Spring Boot",
        }

        if api_frameworks.intersection(set(frameworks)):
            patterns.append("API Service")

        return patterns
