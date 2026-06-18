import streamlit as st
from database.db import init_db
from data.seed_data import seed

# ─── PAGE CONFIG ───────────────────────────────────────────
st.set_page_config(
    page_title="CampusIQ",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── INIT DB ON FIRST RUN ──────────────────────────────────
if "db_ready" not in st.session_state:
    init_db()
    seed()
    st.session_state.db_ready = True

# ─── SESSION STATE ─────────────────────────────────────────
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "student_id" not in st.session_state:
    st.session_state.student_id = None
if "student_name" not in st.session_state:
    st.session_state.student_name = ""

# ─── ROUTING ───────────────────────────────────────────────
def show_auth_pages():
    from pages.auth import show_auth
    show_auth()

def show_main_app():
    with st.sidebar:
        st.title("🎓 CampusIQ")
        st.write(f"Welcome, **{st.session_state.student_name}** 👋")
        st.divider()

        page = st.radio(
            "Navigate",
            ["🏠 Dashboard", "👤 My Profile", "🎯 Recommendations", "💼 Internships", "🛠️ Projects", "💬 Chatbot", "📊 Analytics"],
            label_visibility="collapsed"
        )

        st.divider()
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.student_id = None
            st.session_state.student_name = ""
            st.rerun()

    # Route to the right page
    if page == "🏠 Dashboard":
        from pages.dashboard import show_dashboard
        show_dashboard()
    elif page == "👤 My Profile":
        from pages.profile import show_profile
        show_profile()
    elif page == "🎯 Recommendations":
        from pages.recommendations import show_recommendations
        show_recommendations()
    elif page == "💼 Internships":
        from pages.internships import show_internships
        show_internships()
    elif page == "🛠️ Projects":
        from pages.projects import show_projects
        show_projects()
    elif page == "💬 Chatbot":
        from pages.chatbot import show_chatbot
        show_chatbot()
    elif page == "📊 Analytics":
        from pages.analytics import show_analytics
        show_analytics()

# ─── MAIN ──────────────────────────────────────────────────
if st.session_state.logged_in:
    show_main_app()
else:
    show_auth_pages()
