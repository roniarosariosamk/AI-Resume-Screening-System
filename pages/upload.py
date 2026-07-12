import streamlit as st


def show_upload_page():

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

    process = st.sidebar.button(
        "Process Resumes"
    )

    return (
        uploaded_files,
        job_description,
        process
    )