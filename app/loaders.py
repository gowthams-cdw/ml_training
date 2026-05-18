from pathlib import Path

from langchain_community.document_loaders import (
    JSONLoader,
    PyMuPDFLoader,
    TextLoader,
)
from langchain_core.documents import Document

from app.config import DATA_DIR, SUPPORTED_EXTENSIONS


def load_pdf(file_path: Path) -> list[Document]:
    loader = PyMuPDFLoader(str(file_path))
    documents = loader.load()

    for doc in documents:
        doc.metadata.update(
            {
                "source": file_path.name,
                "file_type": "pdf",
            }
        )

    return documents


def load_txt(file_path: Path) -> list[Document]:
    loader = TextLoader(str(file_path), encoding="utf-8")
    documents = loader.load()

    for doc in documents:
        doc.metadata.update(
            {
                "source": file_path.name,
                "file_type": "txt",
            }
        )

    return documents


def load_json(file_path: Path) -> list[Document]:
    loader = JSONLoader(
        file_path=str(file_path),
        jq_schema=".",
        text_content=False,
    )

    raw_documents = loader.load()

    documents = []

    for doc in raw_documents:
        content = str(doc.page_content)

        documents.append(
            Document(
                page_content=content,
                metadata={
                    "source": file_path.name,
                    "file_type": "json",
                },
            )
        )

    return documents


def load_file(file_path: Path) -> list[Document]:
    suffix = file_path.suffix.lower()

    if suffix == ".pdf":
        return load_pdf(file_path)

    if suffix == ".txt":
        return load_txt(file_path)

    if suffix == ".json":
        return load_json(file_path)

    return []


def load_documents() -> list[Document]:
    documents = []

    for file_path in DATA_DIR.rglob("*"):
        if not file_path.is_file():
            continue

        if file_path.suffix.lower() not in SUPPORTED_EXTENSIONS:
            continue

        loaded_docs = load_file(file_path)
        documents.extend(loaded_docs)

    return documents
