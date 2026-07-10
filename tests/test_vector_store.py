import sys
import os

sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

from src.utils import get_pdf_files
from src.parser import extract_text
from src.chunking import split_text
from src.embeddings import load_embedding_model
from src.vector_store import create_vector_store


def main():

    print("=" * 70)
    print("FAISS VECTOR STORE TEST")
    print("=" * 70)

    pdf_files = get_pdf_files("data/resumes")

    print(f"\nTotal PDFs Found: {len(pdf_files)}")

    all_chunks = []

    for pdf in pdf_files:

        print(f"\nProcessing: {pdf}")

        text = extract_text(pdf)

        chunks = split_text(text)

        print(f"Chunks Created: {len(chunks)}")

        for chunk in chunks:

            all_chunks.append({
                "text": chunk,
                "source": pdf
            })

    print(f"\nTotal Chunks: {len(all_chunks)}")

    embedding = load_embedding_model()

    print("\nLoading Embedding Model...")

    db = create_vector_store(
        all_chunks,
        embedding
    )

    print("\n✅ FAISS Vector Store Created Successfully!")

    print("\nLocation:")
    print("data/faiss_index")


if __name__ == "__main__":
    main()