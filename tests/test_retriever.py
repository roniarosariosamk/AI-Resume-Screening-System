import sys
import os

sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

from src.embeddings import load_embedding_model
from src.retriever import (
    load_vector_store,
    retrieve_documents
)


def main():

    print("=" * 70)
    print("RESUME RETRIEVAL TEST")
    print("=" * 70)

    embedding = load_embedding_model()

    print("\nLoading FAISS Database...")

    db = load_vector_store(embedding)

    query = input("\nEnter your query: ")

    results = retrieve_documents(
        db,
        query,
        k=3
    )

    print("\n" + "=" * 70)
    print("TOP MATCHING RESUMES")
    print("=" * 70)

    if not results:
        print("No matching resumes found.")
        return

    for i, doc in enumerate(results, start=1):

        print(f"\nResult {i}")
        print("-" * 60)

        print("Source:")
        print(doc.metadata.get("source", "Unknown"))

        print("\nContent Preview:\n")
        print(doc.page_content[:500])

        print("\n" + "-" * 60)

    print("\n✅ Retrieval Test Completed Successfully!")


if __name__ == "__main__":
    main()