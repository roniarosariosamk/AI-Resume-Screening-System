import streamlit as st


def show_candidate_card(candidate):
    """
    Professional Candidate Card
    """

    with st.container():

        st.markdown("---")

        # =====================================================
        # HEADER
        # =====================================================

        col1, col2 = st.columns([3, 1])

        with col1:

            st.subheader(f"👤 {candidate['name']}")

            resume_name = candidate.get(
                "resume",
                candidate["name"]
            )

            st.caption(f"📄 Resume : {resume_name}")

        with col2:

            ats = candidate["ats_score"]

            st.metric(
                "📊 ATS Score",
                f"{ats:.2f}%"
            )

            if ats >= 90:

                st.success("🟢 Excellent Match")

            elif ats >= 75:

                st.info("🔵 Strong Candidate")

            elif ats >= 60:

                st.warning("🟡 Average Match")

            else:

                st.error("🔴 Needs Improvement")

        # =====================================================
        # SKILLS SECTION
        # =====================================================

        left, right = st.columns(2)

        # ---------------------------
        # Matched Skills
        # ---------------------------

        with left:

            st.markdown("### 💼 Matched Skills")

            matched = candidate.get("matched", [])

            if matched:

                for skill in matched:

                    st.success(f"✔ {skill}")

            else:

                st.info("No matched skills found.")

        # ---------------------------
        # Missing Skills
        # ---------------------------

        with right:

            st.markdown("### ❌ Missing Skills")

            missing = candidate.get("missing", [])

            if missing:

                for skill in missing:

                    st.warning(f"❌ {skill}")

            else:

                st.success("No missing skills 🎉")

        # =====================================================
        # STATISTICS
        # =====================================================

        st.markdown("### 📈 Candidate Statistics")

        stat1, stat2, stat3 = st.columns(3)

        with stat1:

            st.metric(
                "Matched Skills",
                len(matched)
            )

        with stat2:

            st.metric(
                "Missing Skills",
                len(missing)
            )

        with stat3:

            st.metric(
                "ATS",
                f"{ats:.0f}%"
            )

        # =====================================================
        # AI RECOMMENDATION
        # =====================================================

        st.markdown("### 🤖 AI Recommendation")

        recommendation = candidate.get(
            "recommendation",
            "Review"
        )

        if recommendation.lower() == "shortlist":

            st.success(
                """
### ✅ SHORTLIST

The candidate demonstrates an excellent
match with the Job Description.

Recommended for Technical Interview.
"""
            )

        elif recommendation.lower() == "review":

            st.warning(
                """
### ⚠ REVIEW

The candidate satisfies several
important requirements.

Manual review is recommended.
"""
            )

        else:

            st.error(
                """
### ❌ REJECT

The candidate currently does not satisfy
the required skills.

Not recommended for this position.
"""
            )

        # =====================================================
        # ACTIONS
        # =====================================================

        st.markdown("### ⚙ Candidate Actions")

        btn1, btn2, btn3 = st.columns(3)

        with btn1:

            st.button(
                "👀 View Resume",
                key=f"view_{candidate['name']}"
            )

        with btn2:

            st.button(
                "🎤 Interview Questions",
                key=f"questions_{candidate['name']}"
            )

        with btn3:

            st.button(
                "📧 Send Email",
                key=f"email_{candidate['name']}"
            )

        st.markdown("")