import fitz  # PyMuPDF
import streamlit as st

@st.cache_data(show_spinner=False)
def extract_text(pdf_path):
    """
    Extract text from a PDF file.
    """

    document = fitz.open(pdf_path)

    text = ""

    for page in document:
        text += page.get_text()

    document.close()

    return text

def generate_resume_summary(text, max_lines=5):
    """
    Generate a simple resume summary using the first few non-empty lines.
    """

    lines = [
        line.strip()
        for line in text.split("\n")
        if line.strip()
    ]

    return "\n".join(lines[:max_lines])