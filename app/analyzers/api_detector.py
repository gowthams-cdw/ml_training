from pathlib import Path

from app.core.logger import app_logger


class APIDetector:
    """
    Detect API routes/endpoints.
    """

    def __init__(self) -> None:
        pass

    def detect_apis(
        self,
        source_files: list[Path],
    ) -> list[dict]:
        """
        Detect API routes from source files.
        """

        app_logger.info("Detecting API endpoints...")

        api_routes = []

        for file_path in source_files:
            if file_path.suffix != ".py":
                continue

            routes = self._extract_python_routes(file_path)

            api_routes.extend(routes)

        app_logger.success(f"Detected {len(api_routes)} API routes")

        return api_routes

    def _extract_python_routes(
        self,
        file_path: Path,
    ) -> list[dict]:
        """
        Lightweight FastAPI/Flask route detection.
        """

        routes = []

        try:
            content = file_path.read_text(
                encoding="utf-8",
                errors="ignore",
            )

        except Exception as exc:
            app_logger.warning(f"Failed reading file: {file_path} | {exc}")

            return routes

        lines = content.splitlines()

        http_methods = [
            "get",
            "post",
            "put",
            "delete",
            "patch",
        ]

        for line_number, line in enumerate(
            lines,
            start=1,
        ):
            stripped = line.strip()

            for method in http_methods:
                fastapi_pattern = f"@app.{method}("

                router_pattern = f"@router.{method}("

                if fastapi_pattern in stripped or router_pattern in stripped:
                    route_path = self._extract_route_path(stripped)

                    routes.append(
                        {
                            "file_path": str(file_path),
                            "http_method": (method.upper()),
                            "route": route_path,
                            "line": line_number,
                        }
                    )

        return routes

    # utils
    def _extract_route_path(
        self,
        line: str,
    ) -> str:
        """
        Extract route string from decorator.
        """

        try:
            start = line.index("(") + 1
            end = line.index(")")

            raw = line[start:end]

            return raw.strip().replace('"', "").replace("'", "")
        except Exception:
            return "/unknown"
