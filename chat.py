from dotenv import load_dotenv

from app.generator import generate_answer
from app.retrieval import (
    build_bm25_index,
    retrieve_documents,
)
from app.vectordb import get_vectorstore

load_dotenv()


def rebuild_bm25() -> None:
    vectorstore = get_vectorstore()

    documents = vectorstore.get()

    texts = documents["documents"]
    metadatas = documents["metadatas"]

    reconstructed_documents = []

    from langchain_core.documents import Document

    for text, metadata in zip(texts, metadatas):
        reconstructed_documents.append(
            Document(
                page_content=text,
                metadata=metadata,
            )
        )

    build_bm25_index(reconstructed_documents)


def main() -> None:
    print("\nLoading archive assistant...\n")

    rebuild_bm25()

    print("Archive assistant ready.")
    print("Type 'exit' to quit.\n")

    while True:
        question = input("> Ask: ").strip()

        if question.lower() in {"exit", "quit"}:
            print("\nGoodbye.\n")
            break

        if not question:
            continue

        print("\nSearching archive...\n")

        documents = retrieve_documents(question)

        answer = generate_answer(
            question,
            documents,
        )

        print(answer)
        print(f"\n{'-' * 20}\n")


if __name__ == "__main__":
    main()
