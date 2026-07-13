import streamlit as st


def show_analytics(ranking):

    if not st.session_state.processed:
        return

    st.markdown("---")

    st.header("📈 Analytics")

    st.subheader("🏆 Resume Ranking")

    for index, resume in enumerate(ranking, start=1):

        st.write(
            f"{index}. {resume['name']} → {resume['score'] * 100:.2f}% Match"
        )