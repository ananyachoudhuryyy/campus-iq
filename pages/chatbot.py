import streamlit as st
from database.db import get_student_profile

# ── Rule-based FAQ ──────────────────────────────────────────
FAQ = {
    "how to learn python": "Start with the basics: variables, loops, functions. Try freeCodeCamp or CS50P (free). Then build small projects like a calculator or to-do app. Move on to libraries like Pandas and Matplotlib for data work.",
    "how to learn dsa": "Step 1: Learn arrays, strings, and recursion. Step 2: Study linked lists, stacks, queues. Step 3: Trees and graphs. Step 4: Dynamic programming. Practice daily on LeetCode — start with Easy problems.",
    "how to start machine learning": "Start with Python and NumPy. Then learn scikit-learn for classical ML. Watch Andrew Ng's ML course (Coursera). Build a simple project like house price prediction.",
    "how to prepare for placements": "1. Strengthen DSA (LeetCode 150+ problems). 2. Do 2-3 good projects. 3. Prepare HR answers. 4. Practice mock interviews. 5. Keep your GitHub and LinkedIn active.",
    "what project should i build": "Based on your profile, check the Projects tab for AI-matched suggestions! Popular ones: AI Resume Analyzer, Fake News Detector, Smart Attendance System.",
    "how to learn web development": "Frontend: HTML → CSS → JavaScript → React. Backend: Node.js or Python Flask/Django. Database: SQL basics. Build a full-stack project and deploy it.",
    "how to get internship": "1. Build 2-3 solid projects. 2. Apply on Internshala, LinkedIn, AngelList. 3. Network on LinkedIn. 4. Cold email startups. Check the Internships tab for AI-matched roles!",
    "how to learn sql": "Start with SELECT, WHERE, GROUP BY, JOIN. Practice on SQLZoo or Mode Analytics. Then learn about indexes and query optimization. Build a project that uses a real database.",
    "how to learn cloud": "Start with AWS Free Tier. Learn EC2, S3, Lambda basics. Take the AWS Cloud Practitioner exam (beginner-friendly). Then explore GCP or Azure.",
    "how to improve resume": "Keep it to 1 page. Put projects and skills on top. Use action verbs (built, developed, improved). Include GitHub links. Quantify impact where possible (e.g. '95% accuracy').",
}


def get_faq_answer(query: str) -> str | None:
    query_lower = query.lower().strip()
    for key, answer in FAQ.items():
        # Check if most words from the key appear in the query
        key_words = set(key.split())
        query_words = set(query_lower.split())
        overlap = key_words & query_words
        if len(overlap) / len(key_words) >= 0.6:
            return answer
    return None


def show_chatbot():
    st.title("💬 Campus Chatbot")
    st.caption("Ask me about learning paths, projects, placements, or anything campus-related!")

    profile = get_student_profile(st.session_state.student_id)

    # ── Chat history ──
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = [
            {"role": "assistant", "content": f"Hey {profile['name'].split()[0]}! 👋 I'm your campus AI assistant. Ask me about learning paths, projects, internships, or anything else!"}
        ]

    # Display chat
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    # Quick prompts
    st.write("")
    cols = st.columns(3)
    quick_prompts = [
        "How to learn DSA?",
        "What project should I build?",
        "How to get an internship?",
        "How to prepare for placements?",
        "How to learn Machine Learning?",
        "How to improve my resume?",
    ]
    for i, prompt in enumerate(quick_prompts):
        if cols[i % 3].button(prompt, use_container_width=True, key=f"qp_{i}"):
            handle_message(prompt, profile)

    # ── Chat input ──
    user_input = st.chat_input("Ask me anything...")
    if user_input:
        handle_message(user_input, profile)


def handle_message(user_input: str, profile: dict):
    st.session_state.chat_history.append({"role": "user", "content": user_input})

    # Try FAQ first
    answer = get_faq_answer(user_input)

    if not answer:
        # Fallback: call Claude API
        answer = call_claude(user_input, profile)

    st.session_state.chat_history.append({"role": "assistant", "content": answer})
    st.rerun()


def call_claude(user_input: str, profile: dict) -> str:
    try:
        import anthropic
        client = anthropic.Anthropic()

        system_prompt = f"""You are CampusIQ, a helpful AI assistant for college students in India.
        
Current student profile:
- Name: {profile['name']}
- Year: {profile['year']}, Branch: {profile['branch']}
- Skills: {', '.join(profile['skills'])}
- Interests: {', '.join(profile['interests'])}
- Career Goal: {profile['career_goal']}

Give concise, practical advice relevant to Indian college students. 
Mention specific resources (LeetCode, Internshala, etc.) when helpful.
Keep responses under 200 words."""

        message = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=400,
            system=system_prompt,
            messages=[{"role": "user", "content": user_input}]
        )
        return message.content[0].text

    except Exception as e:
        return "I don't have a ready answer for that, but check the Recommendations and Projects tabs — they might have what you need! You can also try asking more specifically (e.g. 'how to learn Python')."
