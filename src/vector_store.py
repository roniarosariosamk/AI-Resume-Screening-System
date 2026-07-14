import os

from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS


INDEX_PATH = "data/faiss_index"


def create_vector_store(all_chunks, embedding):
    """
    Create FAISS index only if it doesn't already exist.
    """

    if os.path.exists(INDEX_PATH):
        return FAISS.load_local(
            INDEX_PATH,
            embedding,
            allow_dangerous_deserialization=True
        )

    documents = []

    for chunk in all_chunks:

        documents.append(
            Document(
                page_content=chunk["text"],
                metadata={
                    "source": chunk["source"]
                }
            )
        )

    vector_db = FAISS.from_documents(
        documents,
        embedding
    )

    vector_db.save_local(INDEX_PATH)

    return vector_db