from langchain_community.vectorstores import FAISS


def load_vector_store(embedding):
    """
    Load the saved FAISS vector database.
    """

    db = FAISS.load_local(
        "data/faiss_index",
        embedding,
        allow_dangerous_deserialization=True
    )

    return db


def retrieve_documents(db, query, k=3):
    """
    Retrieve the top-k most relevant resume chunks.
    """

    results = db.similarity_search(
        query,
        k=k
    )

    return results