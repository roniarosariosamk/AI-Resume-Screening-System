import os
import streamlit as st
import pandas as pd
import statistics
import plotly.express as px 

from src.parser import extract_text, generate_resume_summary
from src.chunking import split_text
from src.embeddings import load_embedding_model
from src.vector_store import create_vector_store
from src.chatbot import ask_question
from src.jd_parser import extract_job_description
from src.resume_ranker import rank_resumes
from src.skill_matcher import (extract_skills, compare_skills, calculate_ats_score, get_recommendation)
from src.interview_generator import generate_interview_questions
from src.candidate_evaluator import evaluate_candidate
from src.email_sender import send_email
from src.pdf_report import generate_pdf_report
from src.auth import authenticate
from components.sidebar import show_sidebar
from components.metrics import show_metrics
from components.candidate_card import show_candidate_card
from pages.upload import show_upload_page
from utils.jd_processor import process_job_description
from utils.resume_processor import process_resume
from pages.dashboard import show_dashboard
from pages.analytics import show_analytics
from pages.reports import show_reports
# -------------------------------------------------
# Streamlit Page Configuration
# -------------------------------------------------

st.set_page_config(
    page_title="Resume Screening RAG Chatbot",
    page_icon="📄",
    layout="wide"
)

page = show_sidebar()

# -------------------------------------------------
# Session State Initialization
# -------------------------------------------------

if "processed" not in st.session_state:
    st.session_state.processed = False

if "report_data" not in st.session_state:
    st.session_state.report_data = []

if "all_chunks" not in st.session_state:
    st.session_state.all_chunks = []

if "jd_text" not in st.session_state:
    st.session_state.jd_text = ""

if "candidate_data" not in st.session_state:
    st.session_state.candidate_data = []

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

st.title("📄 Resume Screening RAG Chatbot")
# -------------------------------------------------
# Login Screen
# -------------------------------------------------

if not st.session_state.logged_in:

    st.subheader("🔐 Admin Login")

    username = st.text_input("Username")

    password = st.text_input(
        "Password",
        type="password"
    )

    if st.button("Login"):

        if authenticate(username, password):

            st.session_state.logged_in = True
            st.success("✅ Login Successful!")
            st.rerun()

        else:

            st.error("❌ Invalid Username or Password")

    st.stop()
st.write("Upload resumes, upload a Job Description, and ask questions about the candidates.")

st.markdown("---")

show_metrics(st.session_state.candidate_data)

st.subheader("🔍 Search & Filter Candidates")

search_name = st.text_input(
    "Search by Resume Name",
    placeholder="Example: John"
)

search_skill = st.text_input(
    "Search by Skill",
    placeholder="Example: Python"
)

min_ats = st.slider(
    "Minimum ATS Score",
    min_value=0,
    max_value=100,
    value=0
)

st.markdown("---")

uploaded_files, job_description, process = show_upload_page()


# -------------------------------------------------
# Process Button
# -------------------------------------------------

if process:

    if not uploaded_files:
        st.sidebar.warning("Please upload at least one resume.")
    else:

        # -----------------------------------------
        # Save Job Description
        # -----------------------------------------

        if job_description is not None:

            # Process Job Description
            jd_text, jd_embedding, jd_skills = process_job_description(
                job_description
            )

            # Success Message
            st.sidebar.success(
                "✅ Job Description Uploaded Successfully!"
            )

            # Preview
            st.markdown("---")
            st.subheader("📄 Job Description Preview")

            st.text_area(
                "Extracted Job Description",
                jd_text,
                height=250
            )

            # -----------------------------------------
            # Save Resume PDFs
            # -----------------------------------------

            os.makedirs("data/resumes", exist_ok=True)

            all_chunks = []
            report_data = []
            candidate_data = []

            for uploaded_file in uploaded_files:

                (
                    text,
                    summary,
                    resume_skills,
                    matched,
                    missing,
                    ats_score,
                    recommendation,
                ) = process_resume(
                    uploaded_file,
                    jd_skills
                )

                candidate_data.append({
                    "name": uploaded_file.name,
                    "summary": summary,
                    "skills": resume_skills,
                    "matched": matched,
                    "missing": missing,
                    "ats_score": ats_score,
                    "recommendation": recommendation
               })
                
                show_candidate = True

                # -----------------------------------------
                # Apply Search & Filter
                # -----------------------------------------

                show_candidate = True

                if search_name:
                    if search_name.lower() not in uploaded_file.name.lower():
                        show_candidate = False

                if search_skill:
                    if search_skill.lower() not in [skill.lower() for skill in resume_skills]:
                        show_candidate = False

                if ats_score < min_ats:
                    show_candidate = False

                # -----------------------------------------
                # Display Candidate
                # -----------------------------------------
                if show_candidate:

                    with st.expander(f"👤 Candidate: {uploaded_file.name}", expanded=False):

                        col1, col2 = st.columns([2, 1])

                        with col1:

                            st.subheader("📝 Candidate Summary")
                            st.info(summary)

                            st.subheader("🛠 Skills Found")
                            st.write(", ".join(resume_skills))

                            st.subheader("✅ Matched Skills")
                            st.success(", ".join(matched))

                            st.subheader("❌ Missing Skills")
                            st.error(", ".join(missing))

                        with col2:

                            st.metric(
                                label="📊 ATS Score",
                                value=f"{ats_score:.2f}%"
                            )

                            st.progress(min(ats_score / 100, 1.0))

                            st.metric(
                                label="⭐ Recommendation",
                                value=recommendation
                            )
                        st.markdown("---")

                        if st.button(
                            f"🎤 Generate Interview Questions - {uploaded_file.name}"
                        ):

                            with st.spinner("Generating interview questions..."):

                                questions = generate_interview_questions(
                                        summary,
                                        resume_skills,
                                        jd_text
                                )

                                st.subheader("🤖 AI Interview Questions")
                                st.write(questions)

                    report_data.append({
                        "Resume": uploaded_file.name,
                        "Matched Skills":", ".join(matched),
                        "Missing Skills":", ".join(missing),
                        "ATS Score": ats_score,
                        "Recommendation": recommendation
                   })

                chunks = split_text(text)

                for chunk in chunks:

                    all_chunks.append(
                        {
                            "text": chunk,
                            "source": uploaded_file.name
                        }
                    )

            # -----------------------------------------
            # Create Vector Database
            # -----------------------------------------

            embedding = load_embedding_model()

            create_vector_store(
                all_chunks,
                embedding
           )
            
            # -----------------------------------------
            # Save Data to Session State
            # -----------------------------------------

            st.session_state.processed = True
            st.session_state.report_data = report_data
            st.session_state.all_chunks = all_chunks
            st.session_state.jd_text = jd_text
            st.session_state.candidate_data = candidate_data

        else:

            st.sidebar.warning(
                "⚠ Please upload a Job Description."
            )


# -----------------------------------------
# Create Resume Embeddings
# -----------------------------------------

        resume_embeddings = []

        for resume in all_chunks:

            resume_embeddings.append({
               "name": resume["source"],
               "embedding": embedding.embed_query(resume["text"])
       })

# -----------------------------------------
# Rank Resumes
# -----------------------------------------

        ranking = rank_resumes(
            jd_embedding,
            resume_embeddings
        )

        st.sidebar.success(
            "✅ Vector Database Created Successfully!"
        )

        show_analytics(ranking)       

# -------------------------------------------------
# Download ATS Report
# -------------------------------------------------

        st.subheader("📥 Download ATS Report")

        # Convert report data to a DataFrame
        report_df = pd.DataFrame(report_data)

        show_dashboard(
            st.session_state.candidate_data,
            report_df
        )

        show_analytics(ranking)

        show_reports()

# -------------------------------------------------
# Interview Question Generator
# -------------------------------------------------

if st.session_state.processed:

    st.markdown("---")
    st.header("🎤 AI Interview Question Generator")

    candidate_names = [
        candidate["name"]
        for candidate in st.session_state.candidate_data
    ]

    selected_candidate = st.selectbox(
        "Select Candidate",
        candidate_names
    )

    if st.button("Generate Interview Questions"):

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

# -------------------------------------------------
# AI Candidate Evaluation
# -------------------------------------------------

if st.session_state.processed:

    st.markdown("---")
    st.header("🤖 AI Candidate Evaluation")

    candidate_names = [
        candidate["name"]
        for candidate in st.session_state.candidate_data
    ]

    selected_candidate_eval = st.selectbox(
        "Select Candidate for Evaluation",
        candidate_names,
        key="evaluation_candidate"
    )

    if st.button("Evaluate Candidate"):

        candidate = next(
            c for c in st.session_state.candidate_data
            if c["name"] == selected_candidate_eval
        )

        with st.spinner("Evaluating candidate..."):

            evaluation = evaluate_candidate(
                candidate["summary"],
                candidate["skills"],
                st.session_state.jd_text
            )

            st.session_state["evaluation"] = evaluation

        st.subheader("📋 AI Evaluation Report")
        st.write(evaluation)             

# -------------------------------------------------
# Chat Section
# -------------------------------------------------

st.header("💬 Ask Questions")

question = st.text_input(
    "Example: Which candidate has Python and SQL experience?"
)

if st.button("Search"):

    if question.strip() == "":
        st.warning("Please enter a question.")

    else:

        with st.spinner("Searching resumes..."):

            answer = ask_question(question)

        st.success("Answer")

        st.write(answer)