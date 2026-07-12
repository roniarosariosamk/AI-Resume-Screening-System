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

# -------------------------------------------------
# Sidebar
# -------------------------------------------------

st.sidebar.header("📂 Upload Resume PDFs")

uploaded_files = st.sidebar.file_uploader(
    "Choose Resume PDFs",
    type=["pdf"],
    accept_multiple_files=True
)

st.sidebar.markdown("---")

job_description = st.sidebar.file_uploader(
    "📄 Upload Job Description",
    type=["pdf"],
    accept_multiple_files=False
)


# -------------------------------------------------
# Process Button
# -------------------------------------------------

if st.sidebar.button("Process Resumes"):

    if not uploaded_files:
        st.sidebar.warning("Please upload at least one resume.")
    else:

        # -----------------------------------------
        # Save Job Description
        # -----------------------------------------

        if job_description is not None:

            os.makedirs("data/job_description", exist_ok=True)

            jd_path = os.path.join(
                "data/job_description",
                job_description.name
            )

            with open(jd_path, "wb") as f:
                f.write(job_description.getbuffer())

            st.sidebar.success("✅ Job Description Uploaded Successfully!")

            # Extract JD Text
            jd_text = extract_job_description(jd_path)
            embedding_model = load_embedding_model()

            jd_embedding = embedding_model.embed_query(jd_text)
            jd_skills = extract_skills(jd_text)


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

            pdf_path = os.path.join(
                "data/resumes",
                uploaded_file.name
            )

            with open(pdf_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            text = extract_text(pdf_path)
            summary = generate_resume_summary(text)
            resume_skills = extract_skills(text)
            matched, missing = compare_skills(
                jd_skills,
                resume_skills
           )

            ats_score = calculate_ats_score(jd_skills, matched)
            recommendation = get_recommendation(ats_score)

            candidate_data.append({
                "name": uploaded_file.name,
                "summary": summary,
                "skills": resume_skills,
                "matched": matched,
                "missing": missing,
                "ats_score": ats_score,
                "recommendation": recommendation
           })

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

        st.sidebar.success("✅ Vector Database Created Successfully!")
        st.subheader("🏆 Resume Ranking")

        for index, resume in enumerate(ranking, start=1):
            st.write(
                f"{index}. {resume['name']}  →  {resume['score'] * 100:.2f}% Match"
            )

# -------------------------------------------------
# Download ATS Report
# -------------------------------------------------

        st.subheader("📥 Download ATS Report")

        # Convert report data to a DataFrame
        report_df = pd.DataFrame(report_data)
        
# -----------------------------------------
# Top Candidate Dashboard
# -----------------------------------------

        st.subheader("🏆 Top Candidate")

        if report_df.empty or "ATS Score" not in report_df.columns:
            st.warning("No report data available yet.")
            st.stop()

        top_candidate = report_df.sort_values(
            by="ATS Score",
            ascending=False
        ).iloc[0]

        col1, col2 = st.columns(2)

        with col1:

            st.metric(
                "👤 Resume",
                top_candidate["Resume"]
            )

            st.metric(
                "📊 ATS Score",
                f"{top_candidate['ATS Score']:.2f}%"
            )

        with col2:

            st.metric(
                "⭐ Recommendation",
                top_candidate["Recommendation"]
            )

            if top_candidate["ATS Score"] >= 80:
                st.success("🎯 Recommended for Interview")
            elif top_candidate["ATS Score"] >= 60:
                st.warning("📄 Consider for Shortlisting")
            else:
                st.error("❌ Needs Improvement")

        total_resumes = len(report_df)

        average_score = report_df["ATS Score"].mean()

        highest_score = report_df["ATS Score"].max()

        lowest_score = report_df["ATS Score"].min()

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                "📄 Total Resumes",
                total_resumes
            )

        with col2:
            st.metric(
                "📊 Average ATS",
                f"{average_score:.2f}%"
            )

        with col3:
            st.metric(
                "🏆 Highest ATS",
                f"{highest_score:.2f}%"
            )

        with col4:
            st.metric(
                "📉 Lowest ATS",
                f"{lowest_score:.2f}%"
            )

# -----------------------------------------
# ATS Score Chart
# -----------------------------------------

        st.markdown("---")
        st.subheader("📊 ATS Score Comparison")

        chart_data = report_df.set_index("Resume")[["ATS Score"]]

        st.bar_chart(chart_data)

        # Display the report in Streamlit
        st.dataframe(report_df, use_container_width=True)

# -----------------------------------------
# ATS Score Bar Chart
# -----------------------------------------

        st.subheader("📊 ATS Score Comparison")

        fig = px.bar(
            report_df,
            x="Resume",
            y="ATS Score",
            color="ATS Score",
            text="ATS Score",
            title="ATS Score by Resume"
        )

        fig.update_layout(
            xaxis_title="Candidate",
            yaxis_title="ATS Score (%)"
        )

        st.plotly_chart(fig, use_container_width=True)

        # Convert DataFrame to CSV
        csv = report_df.to_csv(index=False).encode("utf-8")

        # Download button
        st.download_button(
            label="📥 Download ATS Report (CSV)",
            data=csv,
            file_name="ATS_Report.csv",
            mime="text/csv"
        )

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
# Send Interview Invitation
# -------------------------------------------------

if st.session_state.processed:

    st.markdown("---")
    st.header("📧 Send Interview Invitation")

    candidate_names = [
        candidate["name"]
        for candidate in st.session_state.candidate_data
    ]

    selected_candidate_email = st.selectbox(
        "Select Candidate",
        candidate_names,
        key="email_candidate"
    )

    receiver_email = st.text_input(
        "Candidate Email Address",
        placeholder="candidate@example.com"
    )

    interview_date = st.date_input("Interview Date")

    interview_time = st.time_input("Interview Time")

    if st.button("📧 Send Interview Invitation"):

        sender_email = st.secrets["EMAIL"]
        sender_password = st.secrets["APP_PASSWORD"]

        subject = "Interview Invitation"

        body = f"""
Dear {candidate['name']},

Congratulations!

We are pleased to inform you that you have been shortlisted for the interview based on your resume screening and AI evaluation.

Interview Details
-------------------------
Date : {interview_date}
Time : {interview_time}
Mode : Online

Please join the interview 10 minutes before the scheduled time.

We look forward to speaking with you.

Best Regards,
HR Team
Resume Screening AI System
"""

        try:

            send_email(
                sender_email,
                sender_password,
                receiver_email,
                subject,
                body
            )

            st.success("✅ Interview Invitation Sent Successfully!")

        except Exception as e:

            st.error(f"Error: {e}") 

# -------------------------------------------------
# PDF ATS Report
# -------------------------------------------------

if st.session_state.processed:

    st.markdown("---")
    st.header("📄 Download ATS Report (PDF)")

    candidate_names = [
        candidate["name"]
        for candidate in st.session_state.candidate_data
    ]

    selected_candidate_pdf = st.selectbox(
        "Select Candidate",
        candidate_names,
        key="pdf_candidate"
    )

    if st.button("Generate PDF Report"):

        candidate = next(
            c for c in st.session_state.candidate_data
            if c["name"] == selected_candidate_pdf
        )

        pdf_file = generate_pdf_report(
            filename=f"{candidate['name']}_ATS_Report.pdf",
            candidate_name=candidate["name"],
            ats_score=candidate["ats_score"],
            matched_skills=", ".join(candidate["matched"]),
            missing_skills=", ".join(candidate["missing"]),
            recommendation=candidate["recommendation"],
            evaluation=st.session_state.get(
                "evaluation",
                "Evaluation not available."
            )
        )

        with open(pdf_file, "rb") as file:

            st.download_button(
                label="📄 Download PDF Report",
                data=file,
                file_name="ATS_Report.pdf",
                mime="application/pdf"
            )                  

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