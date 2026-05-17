from pathlib import Path

# project root
ROOT_DIR = Path(__file__).resolve().parents[2]

# storage paths
DATA_DIR = ROOT_DIR / "data"

REPOS_DIR = DATA_DIR / "repos"
CACHE_DIR = DATA_DIR / "cache"
VECTOR_DB_DIR = DATA_DIR / "vectordb"

OUTPUTS_DIR = ROOT_DIR / "outputs"

MARKDOWN_OUTPUT_DIR = OUTPUTS_DIR / "markdown"
JSON_OUTPUT_DIR = OUTPUTS_DIR / "json"
DIAGRAM_OUTPUT_DIR = OUTPUTS_DIR / "diagrams"

# supported languages by the tool
SUPPORTED_LANGUAGES = {
    ".py": "python",
    ".js": "javascript",
    ".ts": "typescript",
    ".jsx": "typescriptreact",
    ".tsx": "typescriptreact",
    ".java": "java",
    ".go": "go",
    ".cs": "dotnet",
    ".sh": "bash",
}

# language detection based on build files
BUILD_FILES = {
    "requirements.txt": "python",
    "pyproject.toml": "python",
    "package.json": "nodejs",
    "pom.xml": "java",
    "build.gradle": "java",
    "go.mod": "go",
    "*.csproj": "dotnet",
}

# ignore dirs and files, no useful info from this
# so don't use in the ast or knowledge graph
IGNORE_DIRS = {
    ".git",
    "__pycache__",
    "node_modules",
    "dist",
    "build",
    "target",
    ".venv",
    "venv",
    ".idea",
    ".vscode",
    ".next",
    "coverage",
    "bin",
    "obj",
}

IGNORE_FILES = {
    ".DS_Store",
}

# max file size
# avoid very big files in model graph, like data files
MAX_FILE_SIZE_BYTES = 5 * 1024 * 1024  # 5 MB


# embedding model config
EMBEDDING_MODEL = "BAAI/bge-small-en-v1.5"

CHUNK_SIZE = 1200
CHUNK_OVERLAP = 150

# llm config
DEFAULT_LLM_MODEL = "qwen2.5-coder:14b"

OLLAMA_BASE_URL = "http://localhost:11434"

# graph config
GRAPH_MAX_NODES = 100_000

# cache config
ENABLE_CACHE = True

# supported output config
SUPPORTED_DIAGRAMS = {
    "mermaid",
    "plantuml",
}

# required dir
REQUIRED_DIRS = [
    DATA_DIR,
    REPOS_DIR,
    CACHE_DIR,
    VECTOR_DB_DIR,
    OUTPUTS_DIR,
    MARKDOWN_OUTPUT_DIR,
    JSON_OUTPUT_DIR,
    DIAGRAM_OUTPUT_DIR,
]

# create it
for directory in REQUIRED_DIRS:
    directory.mkdir(parents=True, exist_ok=True)
