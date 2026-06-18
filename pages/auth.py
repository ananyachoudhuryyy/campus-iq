import streamlit as st
from database.db import create_student, get_student_by_email

BRANCHES = ["CSE", "ECE", "EEE", "ME", "CE", "IT", "AIDS", "AIML", "Cybersecurity", "Other"]

COMMON_SKILLS = ["Python", "Java", "C++", "JavaScript", "SQL", "Machine Learning", "Deep Learning",
                 "React", "Node.js", "HTML/CSS", "DSA", "Git", "Docker", "AWS", "Android", "Flutter"]

COMMON_INTERESTS = ["AI", "Web Development", "Data Science", "Cybersecurity", "Cloud Computing",
                    "Mobile Development", "Blockchain", "UI/UX Design", "Open Source", "Research"]


def show_auth():
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.title("🎓 CampusIQ")
        st.caption("Your AI-powered campus companion")
        st.divider()

        tab_login, tab_signup = st.tabs(["Login", "Sign Up"])

        # ── LOGIN ──
        with tab_login:
            st.subheader("Welcome back!")
            email = st.text_input("Email", placeholder="you@college.edu", key="login_email")
            password = st.text_input("Password", type="password", key="login_password")

            if st.button("Login", use_container_width=True, type="primary"):
                if not email or not password:
                    st.error("Please fill in all fields.")
                else:
                    student = get_student_by_email(email, password)
                    if student:
                        st.session_state.logged_in = True
                        st.session_state.student_id = student["student_id"]
                        st.session_state.student_name = student["name"]
                        st.success(f"Welcome back, {student['name']}!")
                        st.rerun()
                    else:
                        st.error("Invalid email or password.")

        # ── SIGN UP ──
        with tab_signup:
            st.subheader("Create your profile")

            name = st.text_input("Full Name", placeholder="Ananya Sharma")
            email = st.text_input("College Email", placeholder="ananya@college.edu")
            password = st.text_input("Password", type="password", key="signup_password")

            col_a, col_b = st.columns(2)
            with col_a:
                year = st.selectbox("Year", [1, 2, 3, 4])
            with col_b:
                branch = st.selectbox("Branch", BRANCHES)

            career_goal = st.text_input("Career Goal", placeholder="e.g. Software Engineer at a product company")

            st.write("**Skills** *(select all that apply)*")
            selected_skills = st.multiselect("Skills", COMMON_SKILLS, label_visibility="collapsed")
            other_skills = st.text_input("Other skills (comma-separated)", placeholder="e.g. Rust, Go, Figma")

            st.write("**Interests** *(select all that apply)*")
            selected_interests = st.multiselect("Interests", COMMON_INTERESTS, label_visibility="collapsed")
            other_interests = st.text_input("Other interests (comma-separated)", placeholder="e.g. Robotics, Game Dev")

            if st.button("Create Account", use_container_width=True, type="primary"):
                if not all([name, email, password, career_goal]):
                    st.error("Please fill in all required fields.")
                else:
                    all_skills = selected_skills + [s.strip() for s in other_skills.split(",") if s.strip()]
                    all_interests = selected_interests + [i.strip() for i in other_interests.split(",") if i.strip()]

                    if not all_skills:
                        st.warning("Add at least one skill so we can personalise recommendations!")
                    else:
                        student_id = create_student(name, email, password, year, branch, career_goal, all_skills, all_interests)
                        if student_id:
                            st.session_state.logged_in = True
                            st.session_state.student_id = student_id
                            st.session_state.student_name = name
                            st.success("Account created! Let's find your opportunities 🚀")
                            st.rerun()
                        else:
                            st.error("This email is already registered. Try logging in.")
