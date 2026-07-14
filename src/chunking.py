import streamlit as st
from langchain_text_splitters import RecursiveCharacterTextSplitter

@st.cache_data(show_spinner=False)
def split_text(text):
    """
    Split extracted resume text into smaller chunks.
    """

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100,
        separators=[
            "\n\n",
            "\n",
            ". ",
            " ",
            ""
        ]
    )

    chunks = text_splitter.split_text(text)

    return chunks