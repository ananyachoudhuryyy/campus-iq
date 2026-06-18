import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
from database.db import get_all_skills, get_all_interests, get_search_logs, get_all_students


def show_analytics():
    st.title("📊 Campus Analytics")
    st.caption("Trends across all CampusIQ users")

    students = get_all_students()
    if len(students) < 1:
        st.info("No data yet! Sign up some students to see analytics.")
        return

    st.metric("Total Students", len(students))
    st.divider()

    col1, col2 = st.columns(2)

    # ── Top Skills ──
    with col1:
        st.subheader("🛠️ Most Popular Skills")
        skills = get_all_skills()
        if skills:
            skill_counts = Counter(skills).most_common(10)
            df_skills = pd.DataFrame(skill_counts, columns=["Skill", "Count"])

            fig, ax = plt.subplots(figsize=(5, 4))
            ax.barh(df_skills["Skill"][::-1], df_skills["Count"][::-1], color="#4F86F7")
            ax.set_xlabel("Number of students")
            ax.spines[["top", "right"]].set_visible(False)
            plt.tight_layout()
            st.pyplot(fig)
        else:
            st.info("No skill data yet.")

    # ── Top Interests ──
    with col2:
        st.subheader("💡 Most Common Interests")
        interests = get_all_interests()
        if interests:
            interest_counts = Counter(interests).most_common(10)
            df_interests = pd.DataFrame(interest_counts, columns=["Interest", "Count"])

            fig2, ax2 = plt.subplots(figsize=(5, 4))
            ax2.pie(df_interests["Count"], labels=df_interests["Interest"], autopct="%1.0f%%", startangle=90)
            ax2.axis("equal")
            plt.tight_layout()
            st.pyplot(fig2)
        else:
            st.info("No interest data yet.")

    st.divider()

    # ── Branch distribution ──
    st.subheader("🎓 Students by Branch")
    branches = [s["branch"] for s in students if s["branch"]]
    if branches:
        branch_counts = Counter(branches)
        df_branch = pd.DataFrame(branch_counts.items(), columns=["Branch", "Count"]).sort_values("Count", ascending=False)
        st.bar_chart(df_branch.set_index("Branch"))

    # ── Year distribution ──
    st.subheader("📅 Students by Year")
    years = [f"Year {s['year']}" for s in students if s["year"]]
    if years:
        year_counts = Counter(years)
        df_year = pd.DataFrame(year_counts.items(), columns=["Year", "Count"]).sort_values("Year")
        st.bar_chart(df_year.set_index("Year"))
