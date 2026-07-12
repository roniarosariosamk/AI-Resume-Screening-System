import streamlit as st


def show_sidebar():
    """
    Display the application sidebar.
    """

    with st.sidebar:

        st.image(
            "https://img.icons8.com/color/96/resume.png",
            width=80
        )

        st.title("AI Recruiter")

        st.markdown("---")

        page = st.radio(
            "Navigation",
            [
                "🏠 Dashboard",
                "📄 Resume Screening",
                "📊 Analytics",
                "💬 AI Chatbot",
                "⚙️ Settings"
            ]
        )

        st.markdown("---")

        st.success("🟢 System Online")

    return page