import json

import requests

from app.core.config import (
    DEFAULT_LLM_MODEL,
    OLLAMA_BASE_URL,
)
from app.core.logger import app_logger


class ServiceAnalysisAgent:
    """
    Analyze repository services/modules.
    """

    def __init__(self) -> None:

        self.model = DEFAULT_LLM_MODEL
        self.base_url = OLLAMA_BASE_URL

    def analyze_services(
        self,
        services: list[dict],
        dependency_summary: dict,
    ) -> str:
        """
        Analyze service boundaries and modularity.
        """

        app_logger.info("Running service analysis...")

        prompt = self._build_prompt(
            services,
            dependency_summary,
        )

        response = self._call_llm(prompt)

        app_logger.success("Service analysis completed")

        return response

    def _build_prompt(
        self,
        services: list[dict],
        dependency_summary: dict,
    ) -> str:
        reduced_services = [
            {
                "service_name": service["service_name"],
                "file_count": len(service["files"]),
                "languages": service["languages"],
            }
            for service in services
        ]

        context = {
            "services": reduced_services,
            "dependency_graph_size": len(
                dependency_summary.get(
                    "graph",
                    {},
                )
            ),
        }

        return f"""
You are a senior software architect.

Analyze the repository service/module structure.

Provide:
1. Major subsystems
2. Modularity observations
3. Coupling concerns
4. Scalability observations

Repository Service Metadata:
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
            return "Service analysis failed."
