from pathlib import Path

from app.core.logger import app_logger


class ServiceDetector:
    """
    Detect logical services/modules.
    """

    def __init__(self) -> None:
        pass

    def detect_services(
        self,
        repository_path: Path,
        source_files: list[Path],
    ) -> list[dict]:
        """
        Detect repository services/modules.
        """

        app_logger.info("Detecting services/modules...")

        services: dict[str, dict] = {}

        for file_path in source_files:
            service_name = self._infer_service_name(
                repository_path,
                file_path,
            )

            if service_name not in services:
                services[service_name] = {
                    "service_name": (service_name),
                    "files": [],
                    "languages": set(),
                }

            services[service_name]["files"].append(str(file_path))

            services[service_name]["languages"].add(file_path.suffix.lower())

        result = []

        for service_data in services.values():
            service_data["languages"] = sorted(list(service_data["languages"]))

            result.append(service_data)

        app_logger.success(f"Detected {len(result)} services/modules")

        return sorted(
            result,
            key=lambda item: item["service_name"],
        )

    # utils
    def _infer_service_name(
        self,
        repository_path: Path,
        file_path: Path,
    ) -> str:
        """
        Infer logical service/module name.
        """

        relative_path = file_path.relative_to(repository_path)

        parts = relative_path.parts

        if len(parts) <= 1:
            return "root"

        return parts[0]
