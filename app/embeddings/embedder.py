import chromadb
from chromadb.api.types import QueryResult
from sentence_transformers import (
    SentenceTransformer,
)

from app.core.config import (
    EMBEDDING_MODEL,
    VECTOR_DB_DIR,
)
from app.core.logger import app_logger

# batch size
# to have within limit
BATCH_SIZE = 500


class Embedder:
    """
    Generate and store vector embeddings.
    """

    def __init__(self) -> None:
        app_logger.info(f"Loading embedding model: {EMBEDDING_MODEL}")

        self.model = SentenceTransformer(
            EMBEDDING_MODEL,
            device="cpu",
        )

        self.client = chromadb.PersistentClient(path=str(VECTOR_DB_DIR))

        self.collection = self.client.get_or_create_collection(name="repository_chunks")

    def embed_chunks(
        self,
        chunks: list[dict],
    ) -> None:
        """
        Generate embeddings and store.
        """

        app_logger.info("Generating embeddings...")

        documents = []
        metadatas = []
        ids = []

        for index, chunk in enumerate(chunks):
            content = chunk.get("content", "")

            documents.append(content)

            metadatas.append(
                {
                    "type": chunk.get("type"),
                    "file_path": chunk.get("file_path"),
                    "language": chunk.get("language"),
                }
            )

            ids.append(f"chunk_{index}")

        embeddings = self.model.encode(
            documents,
            show_progress_bar=True,
        )

        total = len(documents)

        # batch inserts
        for start in range(
            0,
            total,
            BATCH_SIZE,
        ):
            end = start + BATCH_SIZE

            batch_documents = documents[start:end]

            batch_embeddings = embeddings[start:end]

            batch_metadatas = metadatas[start:end]

            batch_ids = ids[start:end]

            self.collection.add(
                documents=batch_documents,
                embeddings=batch_embeddings.tolist(),
                metadatas=batch_metadatas,
                ids=batch_ids,
            )

            app_logger.info(f"Inserted embedding batch: {start} -> {end}")

        app_logger.success(f"Stored {total} embeddings")

    def search(
        self,
        query: str,
        limit: int = 5,
    ) -> QueryResult:
        """
        Semantic vector search.
        """

        app_logger.info(f"Semantic search: {query}")

        query_embedding = self.model.encode(query)

        results = self.collection.query(
            query_embeddings=[query_embedding.tolist()],
            n_results=limit,
        )

        return results
