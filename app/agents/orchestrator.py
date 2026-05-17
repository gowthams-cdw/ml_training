from typing import TypedDict

from langgraph.graph import END, StateGraph

from app.agents.api_review_agent import (
    APIReviewAgent,
)
from app.agents.architecture_review_agent import (
    ArchitectureReviewAgent,
)
from app.agents.repo_summary_agent import (
    RepoSummaryAgent,
)
from app.agents.service_analysis_agent import (
    ServiceAnalysisAgent,
)


class GraphState(TypedDict):
    detected_stack: dict
    architecture_result: dict
    graph_summary: dict
    api_routes: list
    services: list
    dependency_result: dict

    repository_summary: str
    architecture_review: str
    service_analysis: str
    api_review: str


# agents
summary_agent = RepoSummaryAgent()
review_agent = ArchitectureReviewAgent()
service_analysis_agent = ServiceAnalysisAgent()
api_review_agent = APIReviewAgent()


# nodes
def generate_summary(
    state: GraphState,
):
    summary = summary_agent.generate_summary(
        detected_stack=state["detected_stack"],
        architecture_result=state["architecture_result"],
        graph_summary=state["graph_summary"],
    )

    return {"repository_summary": summary}


def review_architecture(
    state: GraphState,
):
    review = review_agent.review_architecture(
        detected_stack=state["detected_stack"],
        architecture_result=state["architecture_result"],
        graph_summary=state["graph_summary"],
        api_routes=state["api_routes"],
        services=state["services"],
    )

    return {"architecture_review": review}


def analyze_services(
    state: GraphState,
):
    analysis = service_analysis_agent.analyze_services(
        services=state["services"],
        dependency_summary=state["dependency_result"],
    )

    return {"service_analysis": analysis}


def review_apis(
    state: GraphState,
):
    review = api_review_agent.review_apis(
        api_routes=state["api_routes"],
    )

    return {"api_review": review}


# graph
workflow = StateGraph(GraphState)

workflow.add_node(
    "summary",
    generate_summary,
)

workflow.add_node(
    "architecture_review",
    review_architecture,
)

workflow.add_node(
    "service_analysis",
    analyze_services,
)

workflow.add_node(
    "api_review",
    review_apis,
)

workflow.set_entry_point("summary")

workflow.add_edge(
    "summary",
    "architecture_review",
)

workflow.add_edge(
    "architecture_review",
    "service_analysis",
)

workflow.add_edge(
    "service_analysis",
    "api_review",
)

workflow.add_edge(
    "api_review",
    END,
)

graph = workflow.compile()
