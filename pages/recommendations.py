import streamlit as st
from database.db import get_student_profile, get_all_events, log_search
from engine.recommender import recommend_events


def show_recommendations():
    st.title("🎯 Event Recommendations")
    st.caption("Matched to your skills and interests using AI")

    profile = get_student_profile(st.session_state.student_id)
    events = get_all_events()

    if not profile["skills"] and not profile["interests"]:
        st.warning("Update your profile with skills and interests to get personalised recommendations!")
        return

    # ── Filters ──
    with st.expander("⚙️ Filters", expanded=False):
        event_types = list(set(e["event_type"] for e in events))
        selected_types = st.multiselect("Event Type", event_types, default=event_types)
        top_n = st.slider("Number of recommendations", 3, 15, 5)

    filtered_events = [e for e in events if e["event_type"] in selected_types]
    recommendations = recommend_events(profile["skills"], profile["interests"], filtered_events, top_n)

    # ── Results ──
    st.divider()
    st.subheader(f"Top {len(recommendations)} matches for you")

    for rec in recommendations:
        match_pct = int(rec["score"] * 100)
        with st.container(border=True):
            col1, col2 = st.columns([4, 1])
            with col1:
                st.markdown(f"### {rec['title']}")
                st.caption(f"📅 {rec['date']}  ·  🏷️ {rec['event_type']}")
                st.write(rec["description"])
                tags = [t.strip() for t in rec["tags"].split(",")]
                st.markdown(" ".join([f"`{t}`" for t in tags]))
            with col2:
                color = "green" if match_pct >= 60 else "orange" if match_pct >= 30 else "red"
                st.markdown(f"<h2 style='color:{color};text-align:center'>{match_pct}%</h2>", unsafe_allow_html=True)
                st.caption("match score")
                st.link_button("Register →", rec["link"], use_container_width=True)

    # ── Search log ──
    if recommendations:
        log_search(st.session_state.student_id, "events")
