import streamlit as st

from components.candidate_card import show_candidate_card


def show_dashboard(candidate_data, report_df):

    if not st.session_state.processed:
        return

    # ------------------------------------
    # Candidate Cards
    # ------------------------------------

    st.markdown("---")

    st.header("👥 Candidate Dashboard")

    for candidate in candidate_data:

        show_candidate_card(candidate)

    # ------------------------------------
    # Top Candidate
    # ------------------------------------

    st.markdown("---")

    st.subheader("🏆 Top Candidate")

    if report_df.empty:

        st.warning("No report data available.")

        return

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

            st.success(
                "🎯 Recommended for Interview"
            )

        elif top_candidate["ATS Score"] >= 60:

            st.warning(
                "📄 Consider for Shortlisting"
            )

        else:

            st.error(
                "❌ Needs Improvement"
            )  

    # ------------------------------------
    # Candidate Statistics
    # ------------------------------------

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