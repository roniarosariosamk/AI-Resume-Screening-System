import streamlit as st

from src.email_sender import send_email
from src.pdf_report import generate_pdf_report
from utils.constants import EVALUATION_KEY


def show_reports():

    if not st.session_state.processed:
        return

    st.markdown("---")
    st.header("📄 Reports")

    # -------------------------------------------------
    # Send Interview Invitation
    # -------------------------------------------------

    st.subheader("📧 Send Interview Invitation")

    candidate_names = [
        candidate["name"]
        for candidate in st.session_state.candidate_data
    ]

    selected_candidate = st.selectbox(
        "Select Candidate",
        candidate_names,
        key="report_email_candidate"
    )

    candidate = next(
        c for c in st.session_state.candidate_data
        if c["name"] == selected_candidate
    )

    receiver_email = st.text_input(
        "Candidate Email",
        placeholder="DEFAULT_EMAIL_PLACEHOLDER"
    )

    interview_date = st.date_input(
        "Interview Date",
        key="report_date"
    )

    interview_time = st.time_input(
        "Interview Time",
        key="report_time"
    )

    if st.button(
        "📧 Send Interview Invitation",
        key="send_report_email"
    ):

        sender_email = st.secrets["EMAIL"]
        sender_password = st.secrets["APP_PASSWORD"]

        subject = "Interview Invitation"

        body = f"""
Dear {candidate['name']},

Congratulations!

You have been shortlisted for the interview.

Interview Details

Date : {interview_date}

Time : {interview_time}

Mode : Online

Regards,

HR Team
"""

        try:

            send_email(
                sender_email,
                sender_password,
                receiver_email,
                subject,
                body
            )

            st.success(
                "✅ Interview Invitation Sent Successfully!"
            )

        except Exception as e:

            st.error(f"Error : {e}")


    # -------------------------------------------------
    # PDF ATS Report
    # -------------------------------------------------

    st.markdown("---")

    st.subheader("📄 Download ATS Report")

    candidate_names = [
        candidate["name"]
        for candidate in st.session_state.candidate_data
    ]

    selected_candidate_pdf = st.selectbox(
        "Select Candidate",
        candidate_names,
        key="pdf_candidate"
    )

    if st.button(
        "Generate PDF Report",
        key="generate_pdf"
    ):

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
                EVALUATION_KEY,
                "Evaluation not available."
            )
        )

        with open(pdf_file, "rb") as file:

            st.download_button(
                label="📄 Download PDF Report",
                data=file,
                file_name=f"{candidate['name']}_ATS_Report.pdf",
                mime="application/pdf"
            )