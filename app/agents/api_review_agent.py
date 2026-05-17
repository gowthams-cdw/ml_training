import json

import requests

from app.core.config import (
    DEFAULT_LLM_MODEL,
    OLLAMA_BASE_URL,
)
from app.core.logger import app_logger


class APIReviewAgent:
    """
    Analyze repository API structure.
    """

    def __init__(self) -> None:

        self.model = DEFAULT_LLM_MODEL
        self.base_url = OLLAMA_BASE_URL

    def review_apis(
        self,
        api_routes: list[dict],
    ) -> str:
        """
        Analyze API architecture.
        """

        app_logger.info("Running API review...")

        prompt = self._build_prompt(api_routes)

        response = self._call_llm(prompt)

        app_logger.success("API review completed")

        return response

    def _build_prompt(
        self,
        api_routes: list[dict],
    ) -> str:
        reduced_routes = api_routes[:50]

        context = {
            "route_count": len(api_routes),
            "routes": reduced_routes,
        }

        return f"""
You are a senior backend architect.

Review the API structure.

Provide:
1. API architecture observations
2. REST design observations
3. Scalability concerns
4. API organization quality

API Metadata:
{json.dumps(context, indent=2)}

Keep response concise and technical.
"""

    def _call_llm(
        self,
        prompt: str,
    ) -> str:
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
            return "API review failed."
