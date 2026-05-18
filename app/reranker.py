from langchain_core.documents import Document
from sentence_transformers import CrossEncoder

from app.config import FINAL_TOP_K, RERANKER_MODEL

reranker_model = CrossEncoder(RERANKER_MODEL)


def rerank_documents(
    query: str,
    documents: list[Document],
) -> list[Document]:
    if not documents:
        return []

    pairs = [(query, doc.page_content) for doc in documents]

    scores = reranker_model.predict(pairs)

    scored_documents = list(zip(documents, scores))

    scored_documents.sort(
        key=lambda item: item[1],
        reverse=True,
    )

    reranked_documents = [doc for doc, _ in scored_documents[:FINAL_TOP_K]]

    return reranked_documents
