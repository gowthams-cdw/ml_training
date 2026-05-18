from langchain_chroma import Chroma
from langchain_core.documents import Document

from app.config import CHROMA_DIR, COLLECTION_NAME
from app.embeddings import get_embedding_model


def get_vectorstore() -> Chroma:
    return Chroma(
        collection_name=COLLECTION_NAME,
        persist_directory=str(CHROMA_DIR),
        embedding_function=get_embedding_model(),
    )


def index_documents(documents: list[Document]) -> None:
    vectorstore = get_vectorstore()

    vectorstore.add_documents(documents)

    print(f"Indexed {len(documents)} chunks into ChromaDB.")


def similarity_search(query: str, k: int):
    vectorstore = get_vectorstore()

    return vectorstore.similarity_search_with_relevance_scores(
        query=query,
        k=k,
    )
