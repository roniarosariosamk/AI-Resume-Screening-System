import streamlit as st

from src.chatbot import ask_question


def show_chatbot():

    if not st.session_state.processed:
        return

    st.markdown("---")

    st.header("💬 Ask Questions")

    question = st.text_input(
        "Example: Which candidate has Python and SQL experience?",
        key="chat_question"
    )

    if st.button(
        "Search",
        key="chat_search"
    ):

        if question.strip() == "":

            st.warning("Please enter a question.")

        else:

            with st.spinner("Searching resumes..."):

                answer = ask_question(question)

            st.success("Answer")

            st.write(answer)