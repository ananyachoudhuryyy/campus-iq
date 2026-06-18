import streamlit as st
from database.db import get_student_profile, get_all_events, get_all_internships, get_all_projects


def show_dashboard():
    profile = get_student_profile(st.session_state.student_id)

    st.title(f"Hey {profile['name'].split()[0]} 👋")
    st.caption(f"Year {profile['year']} · {profile['branch']} · Goal: *{profile['career_goal']}*")
    st.divider()

    # ── Quick stats ──
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Your Skills", len(profile["skills"]))
    col2.metric("Your Interests", len(profile["interests"]))
    col3.metric("Events Available", len(get_all_events()))
    col4.metric("Internships Available", len(get_all_internships()))

    st.divider()

    # ── Skills + Interests ──
    col_left, col_right = st.columns(2)

    with col_left:
        st.subheader("🛠️ Your Skills")
        if profile["skills"]:
            cols = st.columns(3)
            for i, skill in enumerate(profile["skills"]):
                cols[i % 3].markdown(f"`{skill}`")
        else:
            st.info("No skills added yet. Update your profile!")

    with col_right:
        st.subheader("💡 Your Interests")
        if profile["interests"]:
            cols = st.columns(3)
            for i, interest in enumerate(profile["interests"]):
                cols[i % 3].markdown(f"`{interest}`")
        else:
            st.info("No interests added yet. Update your profile!")

    st.divider()

    # ── Quick navigation cards ──
    st.subheader("What do you want to explore?")
    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.markdown("### 🎯")
        st.write("**Events & Opportunities**")
        st.caption("Find hackathons, workshops, contests")
        if st.button("Explore Events", use_container_width=True):
            st.info("Go to → Recommendations in the sidebar")

    with c2:
        st.markdown("### 💼")
        st.write("**Internships**")
        st.caption("AI-matched to your profile")
        if st.button("Find Internships", use_container_width=True):
            st.info("Go to → Internships in the sidebar")

    with c3:
        st.markdown("### 🛠️")
        st.write("**Project Ideas**")
        st.caption("Build something for your portfolio")
        if st.button("Get Project Ideas", use_container_width=True):
            st.info("Go to → Projects in the sidebar")

    with c4:
        st.markdown("### 💬")
        st.write("**Campus Chatbot**")
        st.caption("Ask anything about learning paths")
        if st.button("Chat Now", use_container_width=True):
            st.info("Go to → Chatbot in the sidebar")
