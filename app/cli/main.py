from pathlib import Path
from typing import Optional, cast

import typer

from app.agents.orchestrator import (
    GraphState,
    graph,
)
from app.agents.repository_qa_agent import RepositoryQAAgent
from app.analyzers.api_detector import (
    APIDetector,
)
from app.analyzers.architecture_detector import (
    ArchitectureDetector,
)
from app.analyzers.dependency_analyzer import (
    DependencyAnalyzer,
)
from app.analyzers.service_detector import (
    ServiceDetector,
)
from app.core.logger import app_logger
from app.diagrams.mermaid_generator import (
    MermaidGenerator,
)
from app.embeddings.chunker import (
    Chunker,
)
from app.embeddings.embedder import (
    Embedder,
)
from app.graph.graph_builder import (
    GraphBuilder,
)
from app.ingestion.repo_manager import (
    RepoManager,
)
from app.outputs.markdown_writer import (
    MarkdownWriter,
)
from app.parsers.parser_registry import (
    ParserRegistry,
)
from app.scanners.file_scanner import (
    FileScanner,
)
from app.scanners.language_detector import (
    LanguageDetector,
)
from app.utils.cache import (
    CacheManager,
)

app = typer.Typer(help=("AI Powered Codebase Architecture Analyzer"))


# cli input validation
def validate_inputs(
    git_url: Optional[str],
    directory: Optional[Path],
) -> None:

    if not git_url and not directory:
        raise typer.BadParameter("Provide either --git or --dir")

    if git_url and directory:
        raise typer.BadParameter("Use only one: --git OR --dir")

    if directory and not directory.exists():
        raise typer.BadParameter(f"Directory does not exist: {directory}")


# app main command
@app.command()
def analyze(
    git: Optional[str] = typer.Option(
        None,
        "--git",
        help="Git repository URL",
    ),
    dir: Optional[Path] = typer.Option(
        None,
        "--dir",
        help="Local project directory",
    ),
) -> None:

    validate_inputs(git, dir)

    app_logger.info("=== AI Architecture Analyzer ===")

    # repo ingestion
    repo_manager = RepoManager()

    repository_path = repo_manager.prepare_repository(
        git_url=git,
        local_dir=dir,
    )

    app_logger.info(f"Repository ready at: {repository_path}")

    # scanning all files
    scanner = FileScanner()

    source_files = scanner.scan_repository(repository_path)

    app_logger.info(f"Ready for parsing: {len(source_files)} files")

    # language detection
    language_detector = LanguageDetector()

    detected_stack = language_detector.detect_repository_stack(
        repository_path=repository_path,
        source_files=source_files,
    )

    app_logger.info(f"Detected technologies: {detected_stack}")

    # files parser
    parser_registry = ParserRegistry()

    # use cache if file content hash hit or misses
    cache_manager = CacheManager()

    parsed_results = []

    for file_path in source_files:
        parser = parser_registry.get_parser(file_path)

        if not parser:
            continue

        file_hash = cache_manager.generate_file_hash(file_path)

        cached_result = cache_manager.get_parsed_result(file_hash)

        if cached_result:
            app_logger.info(f"Cache hit: {file_path}")

            parsed_results.append(cached_result)

            continue

        parsed_data = parser.parse_file(file_path)

        cache_manager.store_parsed_result(
            file_hash,
            parsed_data,
        )

        parsed_results.append(parsed_data)

    app_logger.success(f"Parsed {len(parsed_results)} files")

    # dependency analysis
    dependency_analyzer = DependencyAnalyzer()

    dependency_result = dependency_analyzer.analyze(parsed_results)

    app_logger.info(f"Dependency graph nodes: {len(dependency_result['graph'])}")

    # graph building
    graph_builder = GraphBuilder()

    dependency_graph = graph_builder.build_dependency_graph(dependency_result)

    graph_summary = graph_builder.summarize_graph()

    app_logger.info(f"Graph summary: {graph_summary}")

    # architecture detection
    architecture_detector = ArchitectureDetector()

    architecture_result = architecture_detector.detect(
        repository_path=repository_path,
        detected_stack=detected_stack,
        dependency_graph=dependency_graph,
    )

    app_logger.info(f"Architecture result: {architecture_result}")

    # api detection
    api_detector = APIDetector()

    api_routes = api_detector.detect_apis(source_files)

    app_logger.info(f"Detected API routes: {len(api_routes)}")

    # service detection
    service_detector = ServiceDetector()

    services = service_detector.detect_services(
        repository_path=repository_path,
        source_files=source_files,
    )

    app_logger.info(f"Detected services/modules: {len(services)}")

    # diagram generator
    diagram_generator = MermaidGenerator()

    diagram_path = diagram_generator.generate_dependency_diagram(dependency_graph)

    app_logger.success(f"Diagram created at: {diagram_path}")

    # chunking and embeding for cache
    # incremental changes and semantic searches for qa agent
    chunker = Chunker()

    chunks = chunker.create_chunks(parsed_results)

    app_logger.info(f"Generated semantic chunks: {len(chunks)}")

    # embedding
    embedder = Embedder()

    embedder.embed_chunks(chunks)

    search_results = embedder.search("architecture analysis")

    app_logger.info(f"Semantic search results: {len(search_results['ids'][0])}")

    # langgraph agents
    agent_state = cast(
        GraphState,
        {
            "detected_stack": detected_stack,
            "architecture_result": architecture_result,
            "graph_summary": graph_summary,
            "api_routes": api_routes,
            "services": services,
            "dependency_result": dependency_result,
        },
    )
    agent_result = graph.invoke(agent_state)

    repository_summary = agent_result["repository_summary"]

    architecture_review = agent_result["architecture_review"]

    service_analysis = agent_result["service_analysis"]

    api_review = agent_result["api_review"]

    app_logger.info("\n===== REPOSITORY SUMMARY =====\n")

    print(repository_summary)

    app_logger.info("\n===== ARCHITECTURE REVIEW =====\n")

    print(architecture_review)

    app_logger.info("\n===== SERVICE ANALYSIS =====\n")

    print(service_analysis)

    app_logger.info("\n===== API REVIEW =====\n")

    print(api_review)

    # generate markdown report
    markdown_writer = MarkdownWriter()

    report_path = markdown_writer.generate_report(
        repository_name=(repository_path.name),
        detected_stack=(detected_stack),
        architecture_result=(architecture_result),
        graph_summary=(graph_summary),
        repository_summary=(repository_summary),
        diagram_path=diagram_path,
    )

    app_logger.success(f"Architecture report created: {report_path}")

    app_logger.success("CLI bootstrap complete.")

    # qa agent
    qa_agent = RepositoryQAAgent(embedder=embedder)

    app_logger.info("\n===== INTERACTIVE REPOSITORY QA =====\n")

    app_logger.info("Type 'exit' to quit.\n")

    while True:
        question = input("\nAsk about the repository > ").strip()

        if not question:
            continue

        if question.lower() in (
            "exit",
            "quit",
            "q",
        ):
            app_logger.info("Exiting repository QA...")
            break

        qa_response = qa_agent.ask(question)

        print("\n")
        print(qa_response)


if __name__ == "__main__":
    app()
