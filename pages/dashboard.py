import streamlit as st
import pandas as pd
import plotly.express as px

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

    # -------------------------------------------------
    # ATS Score Chart
    # -------------------------------------------------

    st.markdown("---")

    st.subheader("📊 ATS Score Comparison")

    chart_data = report_df.set_index("Resume")[["ATS Score"]]

    st.bar_chart(chart_data)

    # -------------------------------------------------
    # Report Table
    # -------------------------------------------------

    st.dataframe(
       report_df,
       use_container_width=True
    )

    # -------------------------------------------------
    # Plotly Chart
    # -------------------------------------------------

    st.subheader("📈 ATS Score Visualization")

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

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # -------------------------------------------------
    # CSV Download
    # -------------------------------------------------

    csv = report_df.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        label="📥 Download ATS Report (CSV)",
        data=csv,
        file_name="ATS_Report.csv",
        mime="text/csv"
    )       