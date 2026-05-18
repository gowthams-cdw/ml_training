from pathlib import Path

# directory
BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "data"
CHROMA_DIR = BASE_DIR / "chroma_db"

# chromadb collection
COLLECTION_NAME = "archive_articles"

# models
EMBEDDING_MODEL = "BAAI/bge-small-en-v1.5"
RERANKER_MODEL = "BAAI/bge-reranker-base"
LLM_MODEL = "mistral"

# chunking
CHUNK_SIZE = 700
CHUNK_OVERLAP = 100

# semantic search
VECTOR_SEARCH_K = 15
BM25_SEARCH_K = 10
FINAL_TOP_K = 5

MIN_RELEVANCE_SCORE = 0.45

# files
SUPPORTED_EXTENSIONS = {
    ".pdf",
    ".txt",
    ".json",
}
