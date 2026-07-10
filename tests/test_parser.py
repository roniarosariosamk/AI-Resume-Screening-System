import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.utils import get_pdf_files
from src.parser import extract_text


pdf_files = get_pdf_files("data/resumes")

print("PDF Files Found:")
print(pdf_files)

print("\n" + "=" * 60)

for pdf in pdf_files:

    print(f"Reading: {pdf}")

    text = extract_text(pdf)

    print(text[:1000])

    print("=" * 60)