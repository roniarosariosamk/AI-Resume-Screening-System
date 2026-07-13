import streamlit as st

from src.interview_generator import generate_interview_questions
from src.candidate_evaluator import evaluate_candidate
from utils.constants import EVALUATION_KEY


def show_ai_tools():

    if not st.session_state.processed:
        return

    st.markdown("---")
    st.header("🤖 AI Tools")

    # -------------------------------------------------
    # Interview Question Generator
    # -------------------------------------------------

    st.subheader("🎤 AI Interview Question Generator")

    candidate_names = [
        candidate["name"]
        for candidate in st.session_state.candidate_data
    ]

    selected_candidate = st.selectbox(
        "Select Candidate",
        candidate_names,
        key="interview_candidate"
    )

    if st.button(
        "Generate Interview Questions",
        key="generate_questions"
    ):

        candidate = next(
            c for c in st.session_state.candidate_data
            if c["name"] == selected_candidate
        )

        with st.spinner("Generating Interview Questions..."):

            questions = generate_interview_questions(
                candidate["summary"],
                candidate["skills"],
                st.session_state.jd_text
            )

        st.subheader("🤖 Interview Questions")

        st.write(questions)

    st.markdown("---")

    # -------------------------------------------------
    # Candidate Evaluation
    # -------------------------------------------------

    st.subheader("🤖 AI Candidate Evaluation")

    selected_candidate_eval = st.selectbox(
        "Select Candidate for Evaluation",
        candidate_names,
        key="evaluation_candidate"
    )

    if st.button(
        "Evaluate Candidate",
        key="evaluate_candidate"
    ):

        candidate = next(
            c for c in st.session_state.candidate_data
            if c["name"] == selected_candidate_eval
        )

        with st.spinner("Evaluating Candidate..."):

            evaluation = evaluate_candidate(
                candidate["summary"],
                candidate["skills"],
                st.session_state.jd_text
            )

            st.session_state[EVELUATION_KEY] = evaluation

        st.subheader("📋 AI Evaluation Report")

        st.write(evaluation)