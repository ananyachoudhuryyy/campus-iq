import streamlit as st
from database.db import get_student_profile, update_student_profile

BRANCHES = ["CSE", "ECE", "EEE", "ME", "CE", "IT", "AIDS", "AIML", "Cybersecurity", "Other"]


def show_profile():
    st.title("👤 My Profile")
    profile = get_student_profile(st.session_state.student_id)

    with st.form("profile_form"):
        st.subheader("Basic Info")
        col1, col2 = st.columns(2)
        with col1:
            year = st.selectbox("Year", [1, 2, 3, 4], index=profile["year"] - 1)
        with col2:
            branch_idx = BRANCHES.index(profile["branch"]) if profile["branch"] in BRANCHES else 0
            branch = st.selectbox("Branch", BRANCHES, index=branch_idx)

        career_goal = st.text_input("Career Goal", value=profile["career_goal"] or "")

        st.subheader("Skills")
        skills_str = st.text_area(
            "Skills (one per line)",
            value="\n".join(profile["skills"]),
            height=120
        )

        st.subheader("Interests")
        interests_str = st.text_area(
            "Interests (one per line)",
            value="\n".join(profile["interests"]),
            height=100
        )

        submitted = st.form_submit_button("Save Changes", type="primary", use_container_width=True)

        if submitted:
            skills = [s.strip() for s in skills_str.split("\n") if s.strip()]
            interests = [i.strip() for i in interests_str.split("\n") if i.strip()]
            update_student_profile(st.session_state.student_id, year, branch, career_goal, skills, interests)
            st.success("Profile updated! Recommendations will refresh automatically.")
            st.rerun()
