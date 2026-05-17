import json

import requests

from app.core.config import (
    DEFAULT_LLM_MODEL,
    OLLAMA_BASE_URL,
)
from app.core.logger import app_logger


class ArchitectureReviewAgent:
    """
    AI architecture review agent.
    """

    def __init__(self) -> None:
        self.model = DEFAULT_LLM_MODEL
        self.base_url = OLLAMA_BASE_URL

    def review_architecture(
        self,
        detected_stack: dict,
        architecture_result: dict,
        graph_summary: dict,
        api_routes: list[dict],
        services: list[dict],
    ) -> str:
        """
        Perform architecture review.
        """

        app_logger.info("Running architecture review...")

        prompt = self._build_prompt(
            detected_stack=detected_stack,
            architecture_result=architecture_result,
            graph_summary=graph_summary,
            api_routes=api_routes,
            services=services,
        )

        response = self._call_llm(prompt)

        app_logger.success("Architecture review completed")

        return response

    def _build_prompt(
        self,
        detected_stack: dict,
        architecture_result: dict,
        graph_summary: dict,
        api_routes: list[dict],
        services: list[dict],
    ) -> str:
        """
        Build architecture review prompt.
        """

        structured_context = {
            "detected_stack": detected_stack,
            "architecture": architecture_result,
            "graph_summary": graph_summary,
            "api_route_count": len(api_routes),
            "service_count": len(services),
        }

        return f"""
You are a principal software architect.

Review this repository architecture.

Provide:

1. Architecture strengths
2. Potential weaknesses
3. Scalability observations
4. Maintainability concerns
5. Suggested improvements

Repository Metadata:
{json.dumps(structured_context, indent=2)}

Keep response concise, technical,
and actionable.
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

            return "Architecture review failed."
