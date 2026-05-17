from pathlib import Path

from app.core.config import (
    BUILD_FILES,
    SUPPORTED_LANGUAGES,
)
from app.core.logger import app_logger


class LanguageDetector:
    """
    Detects repository languages/frameworks.
    """

    def __init__(self) -> None:
        self.extension_map = SUPPORTED_LANGUAGES
        self.build_files = BUILD_FILES

    def detect_repository_stack(
        self,
        repository_path: Path,
        source_files: list[Path],
    ) -> dict:
        """
        Detect repository technologies.
        """

        languages = self._detect_languages(source_files)

        build_systems = self._detect_build_systems(repository_path)

        frameworks = self._detect_frameworks(repository_path)

        result = {
            "languages": languages,
            "build_systems": build_systems,
            "frameworks": frameworks,
        }

        app_logger.success(f"Detected stack: {result}")

        return result

    # langugae detection
    def _detect_languages(
        self,
        source_files: list[Path],
    ) -> dict[str, int]:
        """
        Detect languages by extension frequency.
        """

        counts: dict[str, int] = {}

        for file_path in source_files:
            language = self.extension_map.get(file_path.suffix.lower())

            if not language:
                continue

            counts[language] = counts.get(language, 0) + 1

        return counts

    # detect build system, like cmake
    def _detect_build_systems(
        self,
        repository_path: Path,
    ) -> list[str]:
        """
        Detect build systems/framework ecosystems.
        """

        detected: list[str] = []

        for build_file, ecosystem in self.build_files.items():
            matches = list(repository_path.rglob(build_file))

            if matches:
                detected.append(ecosystem)

        return sorted(set(detected))

    # framework detection
    def _detect_frameworks(
        self,
        repository_path: Path,
    ) -> list[str]:
        """
        Lightweight framework detection.
        """

        frameworks: set[str] = set()

        requirements = repository_path / "requirements.txt"

        package_json = repository_path / "package.json"

        pom_xml = repository_path / "pom.xml"

        # python
        if requirements.exists():
            try:
                content = requirements.read_text(
                    encoding="utf-8",
                    errors="ignore",
                ).lower()

                if "fastapi" in content:
                    frameworks.add("FastAPI")

                if "django" in content:
                    frameworks.add("Django")

                if "flask" in content:
                    frameworks.add("Flask")

            except Exception as exc:
                app_logger.warning(f"Failed reading requirements.txt: {exc}")

        # fastapi
        if package_json.exists():
            try:
                content = package_json.read_text(
                    encoding="utf-8",
                    errors="ignore",
                ).lower()

                if "express" in content:
                    frameworks.add("Express.js")

                if "next" in content:
                    frameworks.add("Next.js")

                if "nestjs" in content:
                    frameworks.add("NestJS")

            except Exception as exc:
                app_logger.warning(f"Failed reading package.json: {exc}")

        # java
        if pom_xml.exists():
            try:
                content = pom_xml.read_text(
                    encoding="utf-8",
                    errors="ignore",
                ).lower()

                if "spring-boot" in content:
                    frameworks.add("Spring Boot")

            except Exception as exc:
                app_logger.warning(f"Failed reading pom.xml: {exc}")

        return sorted(frameworks)
