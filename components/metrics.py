import streamlit as st


def show_metrics(candidate_data):
    """
    Display dashboard KPI metrics.
    """

    col1, col2, col3, col4 = st.columns(4)

    total = len(candidate_data)

    average = (
        sum(c["ats_score"] for c in candidate_data) / total
        if total > 0
        else 0
    )

    shortlisted = sum(
        1 for c in candidate_data
        if c["ats_score"] >= 70
    )

    rejected = total - shortlisted

    with col1:
        st.metric("👥 Total Candidates", total)

    with col2:
        st.metric("⭐ Average ATS", f"{average:.2f}%")

    with col3:
        st.metric("✅ Shortlisted", shortlisted)

    with col4:
        st.metric("❌ Rejected", rejected)