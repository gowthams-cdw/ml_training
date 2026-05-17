import json

import requests

from app.core.config import (
    DEFAULT_LLM_MODEL,
    OLLAMA_BASE_URL,
)
from app.core.logger import app_logger
from app.embeddings.embedder import (
    Embedder,
)


class RepositoryQAAgent:
    """
    Repository question-answering agent.
    """

    def __init__(self, embedder: Embedder) -> None:
        self.embedder = embedder
        self.model = DEFAULT_LLM_MODEL
        self.base_url = OLLAMA_BASE_URL

    def ask(
        self,
        question: str,
        limit: int = 5,
    ) -> str:
        """
        Ask repository-aware questions.
        """

        app_logger.info(f"Repository QA question: {question}")

        retrieval_results = self.embedder.search(
            question,
            limit=limit,
        )

        context = self._build_context(retrieval_results)

        prompt = self._build_prompt(
            question,
            context,
        )

        response = self._call_llm(prompt)

        return response

    def _build_context(
        self,
        retrieval_results,
    ) -> str:
        """
        Convert vector search into LLM context.
        """

        documents = retrieval_results.get(
            "documents",
            [[]],
        )[0]

        metadatas = retrieval_results.get(
            "metadatas",
            [[]],
        )[0]

        context_blocks = []

        for document, metadata in zip(
            documents,
            metadatas,
        ):
            block = {
                "file_path": metadata.get("file_path"),
                "type": metadata.get("type"),
                "language": metadata.get("language"),
                "content": document,
            }

            context_blocks.append(block)

        return json.dumps(
            context_blocks,
            indent=2,
        )

    def _build_prompt(
        self,
        question: str,
        context: str,
    ) -> str:
        """
        Create optimized RAG prompt.
        """

        return f"""
You are a senior software architect.

Answer the repository question using ONLY
the retrieved repository context below.

If the answer is unknown, say so clearly.

Repository Context:
{context}

Question:
{question}

Provide:
1. Direct answer
2. Technical explanation
3. Relevant repository observations
"""

    def _call_llm(
        self,
        prompt: str,
    ) -> str:
        """
        Call local Ollama model.
        """

        url = f"{self.base_url}/api/generate"

        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
        }

        try:
            response = requests.post(
                url,
                json=payload,
                timeout=120,
            )

            response.raise_for_status()

            result = response.json()

            return result.get(
                "response",
                "No response generated.",
            )

        except Exception as exc:
            app_logger.error(f"LLM call failed: {exc}")

            return "Repository QA failed."
