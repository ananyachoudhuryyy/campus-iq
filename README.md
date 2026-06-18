# 🎓 CampusIQ — AI-Powered Campus Assistant

An AI-powered platform that helps college students discover events, internships, and project ideas personalised to their skills and interests.

## ✨ Features

- **Smart Recommendations** — TF-IDF + cosine similarity to match students with events and internships
- **Project Suggester** — AI-ranked project ideas based on your skill stack
- **Campus Chatbot** — Rule-based FAQ + Claude AI for open-ended questions
- **Analytics Dashboard** — Skill trends and interest distribution across all users
- **Student Profiles** — Skills, interests, year, branch, career goals

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Streamlit |
| Backend | Python |
| Database | SQLite |
| AI Engine | scikit-learn (TF-IDF + Cosine Similarity) |
| Chatbot AI | Anthropic Claude API |
| Visualization | Matplotlib, Plotly |

## 🚀 Getting Started

```bash
# 1. Clone the repo
git clone https://github.com/yourusername/campus-iq
cd campus-iq

# 2. Create and activate virtual environment
python -m venv venv
venv\Scripts\activate      # Windows
source venv/bin/activate   # Mac/Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. (Optional) Set Claude API key for chatbot AI
# Create a .env file:
echo ANTHROPIC_API_KEY=your_key_here > .env

# 5. Run the app
streamlit run app.py
```

## 📁 Project Structure

```
campus-iq/
├── app.py                  # Entry point + routing
├── database/
│   ├── db.py               # All DB operations
│   └── campus.db           # SQLite database (auto-created)
├── engine/
│   └── recommender.py      # TF-IDF recommendation engine
├── pages/
│   ├── auth.py             # Login & signup
│   ├── dashboard.py        # Home screen
│   ├── recommendations.py  # Events
│   ├── internships.py      # Internships
│   ├── projects.py         # Project ideas
│   ├── chatbot.py          # Campus chatbot
│   └── analytics.py        # Charts & trends
└── data/
    └── seed_data.py        # Sample data loader
```

ication on Streamlit Cloud with user authentication and real-time analytics dashboard
