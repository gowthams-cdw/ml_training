from collections import OrderedDict

from langchain_core.documents import Document
from langsmith import traceable
from rank_bm25 import BM25Okapi

from app.config import (
    BM25_SEARCH_K,
    MIN_RELEVANCE_SCORE,
    VECTOR_SEARCH_K,
)
from app.hyde import generate_hypothetical_document
from app.reranker import rerank_documents
from app.vectordb import get_vectorstore

bm25_documents: list[Document] = []
bm25_index = None


def build_bm25_index(documents: list[Document]) -> None:
    global bm25_documents
    global bm25_index

    bm25_documents = documents

    tokenized_documents = [doc.page_content.split() for doc in documents]

    bm25_index = BM25Okapi(tokenized_documents)


def bm25_search(query: str, k: int) -> list[Document]:
    if bm25_index is None:
        return []

    tokenized_query = query.split()

    results = bm25_index.get_top_n(
        tokenized_query,
        bm25_documents,
        n=k,
    )

    return results


def vector_search(query: str, k: int) -> list[Document]:
    vectorstore = get_vectorstore()

    results = vectorstore.similarity_search_with_relevance_scores(
        query=query,
        k=k,
    )

    filtered_documents = []

    for document, score in results:
        if score >= MIN_RELEVANCE_SCORE:
            filtered_documents.append(document)

    return filtered_documents


def deduplicate_documents(
    documents: list[Document],
) -> list[Document]:
    unique_documents = OrderedDict()

    for doc in documents:
        key = (
            doc.metadata.get("source"),
            doc.metadata.get("chunk_id"),
        )

        unique_documents[key] = doc

    return list(unique_documents.values())


@traceable(name="document_retrieval")
def retrieve_documents(query: str) -> list[Document]:
    hypothetical_document = generate_hypothetical_document(query)

    vector_results = vector_search(
        hypothetical_document,
        VECTOR_SEARCH_K,
    )

    bm25_results = bm25_search(
        query,
        BM25_SEARCH_K,
    )

    merged_documents = vector_results + bm25_results

    unique_documents = deduplicate_documents(merged_documents)

    reranked_documents = rerank_documents(
        query,
        unique_documents,
    )

    return reranked_documents
