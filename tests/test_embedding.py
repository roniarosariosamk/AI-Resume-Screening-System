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


def main():

    print("=" * 70)
    print("EMBEDDING MODEL TEST")
    print("=" * 70)

    embedding = load_embedding_model()

    sample_text = "Python Developer with Machine Learning and SQL skills."

    vector = embedding.embed_query(sample_text)

    print("\nSample Text:")
    print(sample_text)

    print("\nVector Dimension:")
    print(len(vector))

    print("\nFirst 10 Values:")
    print(vector[:10])

    print("\n✅ Embedding Model Working Successfully!")


if __name__ == "__main__":
    main()