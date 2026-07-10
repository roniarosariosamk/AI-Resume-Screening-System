import sys
import os

# Add the project root to Python path
sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

# Import project modules
from src.utils import get_pdf_files
from src.parser import extract_text
from src.chunking import split_text


def main():

    print("=" * 70)
    print("           RESUME CHUNKING TEST")
    print("=" * 70)

    # Get all PDF files
    pdf_files = get_pdf_files("data/resumes")

    print(f"\nPDF Files Found: {len(pdf_files)}")
    print(pdf_files)

    # Check whether PDFs exist
    if len(pdf_files) == 0:
        print("\n❌ No PDF files found!")
        print("Please place resume PDFs inside:")
        print("data/resumes/")
        return

    # Process each PDF
    for pdf in pdf_files:

        print("\n" + "=" * 70)
        print(f"Processing Resume: {pdf}")
        print("=" * 70)

        # Extract text
        text = extract_text(pdf)

        print(f"\nCharacters Extracted: {len(text)}")

        # Split text into chunks
        chunks = split_text(text)

        print(f"Total Chunks Created: {len(chunks)}")

        # Print first 3 chunks only
        for i, chunk in enumerate(chunks[:3]):

            print("\n" + "-" * 60)
            print(f"Chunk {i + 1}")
            print("-" * 60)

            print(chunk[:300])

    print("\n" + "=" * 70)
    print("✅ Chunking Test Completed Successfully!")
    print("=" * 70)


if __name__ == "__main__":
    main()