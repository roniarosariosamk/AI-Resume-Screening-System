import fitz


def extract_job_description(pdf_path):
    """
    Extract text from a Job Description PDF.
    """

    text = ""

    document = fitz.open(pdf_path)

    for page in document:
        text += page.get_text()

    document.close()

    return text.strip()