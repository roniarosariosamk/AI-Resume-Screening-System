import os


def get_pdf_files(folder_path):
    """
    Returns a list of PDF file paths from the given folder.
    """

    pdf_files = []

    for file in os.listdir(folder_path):
        if file.lower().endswith(".pdf"):
            pdf_files.append(os.path.join(folder_path, file))

    return pdf_files