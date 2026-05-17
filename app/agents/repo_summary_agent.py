import json

import requests

from app.core.config import (
    DEFAULT_LLM_MODEL,
    OLLAMA_BASE_URL,
)
from app.core.logger import app_logger


class RepoSummaryAgent:
    """
    AI repository summarization agent.
    """

    def __init__(self) -> None:

        self.model = DEFAULT_LLM_MODEL
        self.base_url = OLLAMA_BASE_URL

    def generate_summary(
        self,
        detected_stack: dict,
        architecture_result: dict,
        graph_summary: dict,
    ) -> str:
        """
        Generate repository architecture summary.
        """

        app_logger.info("Generating AI repository summary...")

        prompt = self._build_prompt(
            detected_stack=detected_stack,
            architecture_result=architecture_result,
            graph_summary=graph_summary,
        )

        response = self._call_llm(prompt)

        app_logger.success("AI summary generated")

        return response

    def _build_prompt(
        self,
        detected_stack: dict,
        architecture_result: dict,
        graph_summary: dict,
    ) -> str:
        """
        Build optimized structured prompt.
        """

        structured_context = {
            "detected_stack": detected_stack,
            "architecture": architecture_result,
            "graph_summary": graph_summary,
        }

        return f"""
You are a senior software architect.

Analyze this repository metadata and generate:

1. High-level architecture summary
2. Main technologies used
3. Likely architectural style
4. System observations

Repository Metadata:
{json.dumps(structured_context, indent=2)}

Keep response concise and technical.
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

            return "LLM summary generation failed."
