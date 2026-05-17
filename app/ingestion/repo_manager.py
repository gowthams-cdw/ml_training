import shutil
from pathlib import Path
from urllib.parse import urlparse

from git import Repo

from app.core.config import REPOS_DIR
from app.core.logger import app_logger


class RepoManager:
    """
    Handles repository ingestion.
    """

    def __init__(self) -> None:
        self.base_repo_dir = REPOS_DIR

    # check repo
    def prepare_repository(
        self,
        git_url: str | None = None,
        local_dir: Path | None = None,
    ) -> Path:
        """
        Main entry point.

        Returns:
            Path to repository root
        """

        if git_url:
            return self._clone_repository(git_url)

        if local_dir:
            return self._validate_local_directory(local_dir)

        raise ValueError("Either git_url or local_dir required")

    # clone repo
    def _clone_repository(self, git_url: str) -> Path:
        """
        Clone repository locally.
        """

        repo_name = self._extract_repo_name(git_url)

        destination = self.base_repo_dir / repo_name

        if destination.exists():
            app_logger.warning(f"Repository already exists. Removing: {destination}")

            shutil.rmtree(destination)

        app_logger.info(f"Cloning repository: {git_url}")

        Repo.clone_from(
            git_url,
            destination,
            depth=1,
        )

        app_logger.success(f"Repository cloned successfully: {destination}")

        return destination

    def _validate_local_directory(
        self,
        local_dir: Path,
    ) -> Path:
        """
        Validate local repository directory.
        """

        resolved = local_dir.resolve()

        if not resolved.exists():
            raise FileNotFoundError(f"Directory does not exist: {resolved}")

        if not resolved.is_dir():
            raise NotADirectoryError(f"Path is not directory: {resolved}")

        app_logger.success(f"Using local repository: {resolved}")

        return resolved

    # utils
    @staticmethod
    def _extract_repo_name(git_url: str) -> str:
        """
        Extract repository name from URL.
        """

        parsed = urlparse(git_url)

        repo_name = Path(parsed.path).stem

        return repo_name
