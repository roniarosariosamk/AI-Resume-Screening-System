import os
import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI


def get_llm():
    api_key = st.secrets.get(
        "GOOGLE_API_KEY",
        os.getenv("GOOGLE_API_KEY")
    )

    st.write("API Key loaded:", api_key is not None)

    return ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        google_api_key=api_key,
        temperature=0
    )