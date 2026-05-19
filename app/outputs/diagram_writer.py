from pathlib import Path

from app.core.config import OUTPUTS_DIR
from app.core.logger import (
    app_logger,
)


class DiagramWriter:
    """
    Store generated architecture diagrams.
    """

    def __init__(self) -> None:
        self.output_dir = OUTPUTS_DIR / "diagrams"

        self.output_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

    def save_diagram(
        self,
        repository_name: str,
        architecture_diagram: str,
    ) -> Path:
        """
        Save Mermaid diagram markdown.
        """

        file_path = self.output_dir / f"{repository_name}_diagram.md"

        file_path.write_text(
            architecture_diagram,
            encoding="utf-8",
        )

        app_logger.success(f"Architecture diagram saved: {file_path}")

        return file_path
