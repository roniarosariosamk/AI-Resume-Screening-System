import streamlit as st
from langchain_huggingface import HuggingFaceEmbeddings


@st.cache_resource
def load_embedding_model():
    """
    Load the Hugging Face embedding model only once.
    """

    embedding = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    return embedding