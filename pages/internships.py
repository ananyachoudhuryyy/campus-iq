import streamlit as st
from database.db import get_student_profile, get_all_internships, log_search
from engine.recommender import recommend_internships


def show_internships():
    st.title("💼 Internship Recommendations")
    st.caption("AI-matched to your skills and career goal")

    profile = get_student_profile(st.session_state.student_id)
    internships = get_all_internships()

    top_n = st.slider("Number of results", 3, 12, 6)
    recommendations = recommend_internships(profile["skills"], profile["interests"], internships, top_n)

    st.divider()

    for rec in recommendations:
        match_pct = int(rec["score"] * 100)
        with st.container(border=True):
            col1, col2 = st.columns([4, 1])
            with col1:
                st.markdown(f"### {rec['title']}")
                st.caption(f"🏢 {rec['company']}")
                st.write(rec["description"])
                tags = [t.strip() for t in rec["tags"].split(",")]
                st.markdown(" ".join([f"`{t}`" for t in tags]))
            with col2:
                color = "green" if match_pct >= 60 else "orange" if match_pct >= 30 else "red"
                st.markdown(f"<h2 style='color:{color};text-align:center'>{match_pct}%</h2>", unsafe_allow_html=True)
                st.caption("match score")
                st.link_button("Apply →", rec["link"], use_container_width=True)

    log_search(st.session_state.student_id, "internships")
