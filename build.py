from dotenv import load_dotenv

from app.chunking import chunk_documents
from app.loaders import load_documents
from app.retrieval import build_bm25_index
from app.vectordb import index_documents

load_dotenv()


def main() -> None:
    print("\nLoading documents...\n")

    documents = load_documents()

    print(f"Loaded {len(documents)} documents.")

    print("\nChunking documents...\n")

    chunked_documents = chunk_documents(documents)

    print(f"Created {len(chunked_documents)} chunks.")

    print("\nBuilding BM25 index...\n")

    build_bm25_index(chunked_documents)

    print("BM25 index ready.")

    print("\nIndexing documents into ChromaDB...\n")

    index_documents(chunked_documents)

    print("\nBuild completed successfully.\n")


if __name__ == "__main__":
    main()
