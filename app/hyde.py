from langchain_core.prompts import PromptTemplate
from langchain_ollama import OllamaLLM
from langsmith import traceable

from app.config import LLM_MODEL

hyde_prompt = PromptTemplate.from_template(
    """
You are generating a hypothetical newspaper archive snippet.

The snippet should:
- resemble a newspaper report
- contain likely terminology
- be concise
- stay relevant to the query

Question:
{question}

Hypothetical Archive Snippet:
"""
)


llm = OllamaLLM(
    model=LLM_MODEL,
)


@traceable(name="hyde_generation")
def generate_hypothetical_document(question: str) -> str:
    chain = hyde_prompt | llm

    hypothetical_document = chain.invoke(
        {
            "question": question,
        }
    )

    return hypothetical_document.strip()
