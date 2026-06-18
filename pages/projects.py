import streamlit as st
from database.db import get_student_profile, get_all_projects
from engine.recommender import recommend_projects

DIFFICULTY_COLORS = {"Beginner": "🟢", "Intermediate": "🟡", "Advanced": "🔴"}


def show_projects():
    st.title("🛠️ Project Ideas")
    st.caption("Personalised project suggestions based on your skills")

    profile = get_student_profile(st.session_state.student_id)
    projects = get_all_projects()

    col1, col2 = st.columns(2)
    with col1:
        top_n = st.slider("Number of ideas", 3, 15, 6)
    with col2:
        difficulties = st.multiselect("Difficulty", ["Beginner", "Intermediate", "Advanced"],
                                      default=["Beginner", "Intermediate", "Advanced"])

    filtered = [p for p in projects if p["difficulty"] in difficulties]
    recommendations = recommend_projects(profile["skills"], profile["interests"], filtered, top_n)

    st.divider()

    cols = st.columns(2)
    for i, rec in enumerate(recommendations):
        match_pct = int(rec["score"] * 100)
        diff_icon = DIFFICULTY_COLORS.get(rec["difficulty"], "⚪")

        with cols[i % 2]:
            with st.container(border=True):
                st.markdown(f"### {rec['title']}")
                st.caption(f"{diff_icon} {rec['difficulty']}  ·  **{match_pct}% match**")
                st.write(rec["description"])
                tags = [t.strip() for t in rec["tags"].split(",")]
                st.markdown(" ".join([f"`{t}`" for t in tags[:5]]))
