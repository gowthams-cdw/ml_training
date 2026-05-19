import re

import requests
from langsmith import traceable

from app.core.config import (
    OLLAMA_BASE_URL,
    VALIDATION_LLM_MODEL,
)
from app.core.logger import (
    app_logger,
)


class DiagramValidationAgent:
    """
    Validate AI-generated architecture diagrams.
    """

    def __init__(self) -> None:
        self.model = VALIDATION_LLM_MODEL
        self.base_url = OLLAMA_BASE_URL

    @traceable(
        name="Architecture Diagram Validation",
        run_type="llm",
    )
    def validate_diagram(
        self,
        repository_summary: str,
        architecture_review: str,
        service_analysis: str,
        api_review: str,
        architecture_diagram: str,
    ) -> dict:
        """
        Validate generated architecture diagram.
        """

        app_logger.info("Validating architecture diagram...")

        prompt = self._build_prompt(
            repository_summary,
            architecture_review,
            service_analysis,
            api_review,
            architecture_diagram,
        )

        validation_response = self._call_llm(prompt)

        accuracy_score = self._extract_accuracy(validation_response)

        app_logger.success(
            f"Diagram validation completed ({accuracy_score}% confidence)"
        )

        return {
            "accuracy_score": (accuracy_score),
            "validation": (validation_response),
        }

    # =====================================================
    # PROMPT
    # =====================================================

    def _build_prompt(
        self,
        repository_summary: str,
        architecture_review: str,
        service_analysis: str,
        api_review: str,
        architecture_diagram: str,
    ) -> str:

        return f"""
You are a senior software architect.

Validate this Mermaid architecture diagram.

Repository Summary:
{repository_summary}

Architecture Review:
{architecture_review}

Service Analysis:
{service_analysis}

API Review:
{api_review}

Generated Mermaid Diagram:
{architecture_diagram}

Tasks:
1. Verify architecture correctness
2. Verify Mermaid syntax quality
3. Verify service relationships
4. Verify high-level clarity
5. Give an overall accuracy/confidence score from 0-100

IMPORTANT:
Return concise validation only.

Format:
Accuracy Score: <number>

Validation:
<short validation>
"""

    # =====================================================
    # LLM CALL
    # =====================================================

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
                timeout=180,
            )

            response.raise_for_status()

            result = response.json()

            return result.get(
                "response",
                "Validation failed.",
            )

        except Exception as exc:
            app_logger.error(f"LLM call failed: {exc}")

            return "Validation failed."

    def _extract_accuracy(
        self,
        validation_text: str,
    ) -> int:
        matches = re.findall(
            r"(\d{1,3})",
            validation_text,
        )

        if not matches:
            return 70

        value = int(matches[0])

        return max(
            0,
            min(value, 100),
        )
