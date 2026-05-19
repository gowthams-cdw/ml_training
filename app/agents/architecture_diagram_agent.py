import requests
from langsmith import traceable

from app.core.config import (
    DEFAULT_LLM_MODEL,
    OLLAMA_BASE_URL,
)
from app.core.logger import app_logger


class ArchitectureDiagramAgent:
    """
    Generate high-level architecture diagrams.
    """

    def __init__(self) -> None:
        self.model = DEFAULT_LLM_MODEL
        self.base_url = OLLAMA_BASE_URL

    @traceable(
        name="Architecture Diagram Generation",
        run_type="llm",
    )
    def generate_diagram(
        self,
        repository_summary: str,
        architecture_review: str,
        service_analysis: str,
        api_review: str,
    ) -> str:
        """
        Generate Mermaid architecture diagram.
        """

        app_logger.info("Generating architecture diagram...")

        prompt = self._build_prompt(
            repository_summary,
            architecture_review,
            service_analysis,
            api_review,
        )

        response = self._call_llm(prompt)

        app_logger.success("Architecture diagram generated")

        return response

    def _build_prompt(
        self,
        repository_summary: str,
        architecture_review: str,
        service_analysis: str,
        api_review: str,
    ) -> str:

        return f"""
You are a senior software architect.

Generate a HIGH-LEVEL Mermaid architecture diagram.

Rules:
- ONLY return Mermaid markdown
- NO explanations
- Keep diagram clean
- Keep it high-level
- Focus on services/modules/apis
- Avoid file-level details
- Don't make the diagram messy, keep it simple
- Don't make so many nodes and arrows
- keep the flow mostly linear, have some arrows to some, don't make things so messy
- Want to be easy to understand
- If API, service, DB layer is not avail tell, not avail in diagram

Repository Summary:
{repository_summary}

Architecture Review:
{architecture_review}

Service Analysis:
{service_analysis}

API Review:
{api_review}

Return ONLY:

```mermaid
graph TD
...
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
                "Diagram generation failed.",
            )

        except Exception as exc:
            app_logger.error(f"LLM call failed: {exc}")
            return "Diagram generation failed."
