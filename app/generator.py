from langchain_core.documents import Document
from langchain_core.prompts import PromptTemplate
from langchain_ollama import OllamaLLM
from langsmith import traceable

from app.config import LLM_MODEL

llm = OllamaLLM(
    model=LLM_MODEL,
)


answer_prompt = PromptTemplate.from_template(
    """
You are an editorial archive assistant.

You must answer ONLY from the provided archive context.

Rules:
- Do NOT speculate
- Do NOT invent facts
- Do NOT use outside knowledge
- If evidence is insufficient, say:
  "I could not find enough evidence in the archive."

Every factual claim must be grounded in the context.

Context:
{context}

Question:
{question}

Answer:
"""
)


def build_context(documents: list[Document]) -> str:
    context_parts = []

    for doc in documents:
        source = doc.metadata.get("source", "unknown")
        chunk_id = doc.metadata.get("chunk_id", "unknown")

        context_parts.append(
            f"""
SOURCE: {source}
CHUNK: {chunk_id}

CONTENT:
{doc.page_content}
"""
        )

    return "\n\n".join(context_parts)


def build_citations(documents: list[Document]) -> str:
    citations = []

    seen = set()

    for doc in documents:
        source = doc.metadata.get("source", "unknown")
        chunk_id = doc.metadata.get("chunk_id", "unknown")

        citation = f"- {source} (chunk {chunk_id})"

        if citation not in seen:
            citations.append(citation)
            seen.add(citation)

    return "\n".join(citations)


@traceable(name="answer_generation")
def generate_answer(
    question: str,
    documents: list[Document],
) -> str:
    if not documents:
        return "I could not find enough evidence in the archive."

    context = build_context(documents)

    chain = answer_prompt | llm

    answer = chain.invoke(
        {
            "context": context,
            "question": question,
        }
    )

    clean_answer = answer.strip()

    if "could not find enough evidence" in clean_answer.lower():
        return clean_answer

    citations = build_citations(documents)

    final_response = f"{clean_answer}\n\nSources:\n{citations}"

    return final_response
