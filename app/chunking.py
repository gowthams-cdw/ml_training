from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.config import CHUNK_OVERLAP, CHUNK_SIZE

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=CHUNK_SIZE,
    chunk_overlap=CHUNK_OVERLAP,
    separators=[
        "\n\n",
        "\n",
        ". ",
        " ",
        "",
    ],
)


def chunk_documents(documents: list[Document]) -> list[Document]:
    chunked_documents = text_splitter.split_documents(documents)

    for index, doc in enumerate(chunked_documents):
        doc.metadata["chunk_id"] = index

    return chunked_documents
