import streamlit as st
from langchain_ollama import ChatOllama


@st.cache_resource
def load_llm():
    """
    Load the Ollama Llama 3 model only once.
    """

    return ChatOllama(
        model="llama3",
        temperature=0
    )