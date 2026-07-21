import streamlit as st
from langchain_community.vectorstores import FAISS


@st.cache_resource(show_spinner=False)
def load_vector_store(embedding):
    """
    Load the FAISS vector database only once.
    """

    db = FAISS.load_local(
        "data/faiss_index",
        embedding,
        allow_dangerous_deserialization=True
    )

    return db


def retrieve_documents(db, question, k=3):
    """
    Retrieve relevant documents from FAISS.
    """

    docs = db.similarity_search(
        question,
        k=k
    )

    return docs