import os
import streamlit as st
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()


@st.cache_resource
def get_llm():

    api_key = st.secrets.get(
        "GOOGLE_API_KEY",
        os.getenv("GOOGLE_API_KEY")
    )

    st.write("Current directory:", os.getcwd())
    st.write("Secrets available:", list(st.secrets.keys()))
    st.write("API Key Loaded:", api_key is not None)

    if not api_key:
        st.error("GOOGLE_API_KEY not found.")
        st.stop()

    return ChatGoogleGenerativeAI(
        model="gemini-3.5-flash",
        google_api_key=api_key,   # <-- use api_key here
        temperature=0.7
    )