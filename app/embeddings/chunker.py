from app.core.config import (
    CHUNK_SIZE,
)
from app.core.logger import app_logger


class Chunker:
    """
    Create semantic chunks for embeddings.
    """

    def __init__(self) -> None:
        self.chunk_size = CHUNK_SIZE

    def create_chunks(
        self,
        parsed_results: list[dict],
    ) -> list[dict]:
        """
        Create semantic embedding chunks.
        """

        app_logger.info("Creating semantic chunks...")

        chunks: list[dict] = []

        for parsed_file in parsed_results:
            file_chunks = self._create_file_chunks(parsed_file)

            chunks.extend(file_chunks)

        app_logger.success(f"Created {len(chunks)} chunks")

        return chunks

    def _create_file_chunks(
        self,
        parsed_file: dict,
    ) -> list[dict]:
        """
        Create chunks from parsed file metadata.
        """

        chunks: list[dict] = []

        file_path = parsed_file.get("file_path", "")

        language = parsed_file.get("language", "")

        imports = parsed_file.get("imports", [])

        functions = parsed_file.get("functions", [])

        classes = parsed_file.get("classes", [])

        if imports:
            chunks.append(
                {
                    "type": "imports",
                    "file_path": file_path,
                    "language": language,
                    "content": "\n".join(imports),
                }
            )

        for function in functions:
            content = (
                f"Function: "
                f"{function['name']}\n"
                f"Lines: "
                f"{function['start_line']}-"
                f"{function['end_line']}"
            )

            chunks.append(
                {
                    "type": "function",
                    "file_path": file_path,
                    "language": language,
                    "content": content,
                }
            )

        for cls in classes:
            content = (
                f"Class: {cls['name']}\nLines: {cls['start_line']}-{cls['end_line']}"
            )

            chunks.append(
                {
                    "type": "class",
                    "file_path": file_path,
                    "language": language,
                    "content": content,
                }
            )

        return chunks
