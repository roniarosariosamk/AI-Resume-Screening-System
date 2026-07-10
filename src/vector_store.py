from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS


def create_vector_store(all_chunks, embedding):
    """
    Create a FAISS vector database from resume chunks.
    """

    documents = []

    for chunk in all_chunks:

        document = Document(
            page_content=chunk["text"],
            metadata={
                "source": chunk["source"]
            }
        )

        documents.append(document)

    vector_db = FAISS.from_documents(
        documents=documents,
        embedding=embedding
    )

    vector_db.save_local("data/faiss_index")

    return vector_db