import os
import streamlit as st
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

#Load variables from .env
load_dotenv()

def get_llm():
    st.write("Current directory:", os.getcwd())
    st.write("Secrets available:", list(st.secrets.keys()))

    api_key = st.secrets.get(
        "GOOGLE_API_KEY",
        os.getenv("GOOGLE_API_KEY")
    )

    st.write("API key from secrets:", api_key is not None)
    st.write("API key from env:", os.getenv("GOOGLE_API_KEY") is not None)

    if not api_key:
        st.error("GOOGLE_API_KEY not found.env")
        st.stop()

    return ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",
        google_api_key=os.getenv("GOOGLE_API_KEY"),
        temperature=0.7
    )