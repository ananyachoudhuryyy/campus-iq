"""
Run this once to populate the database with sample data.
Usage: python data/seed_data.py
"""
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from database.db import get_connection, init_db

EVENTS = [
    ("AI & ML Hackathon", "48-hour hackathon focused on AI/ML solutions", "python,machine learning,ai,deep learning,nlp", "Hackathon", "2024-08-10", "#"),
    ("Web Dev Bootcamp", "Full-stack web development intensive workshop", "html,css,javascript,react,nodejs,web development", "Workshop", "2024-08-15", "#"),
    ("DSA Championship", "Competitive programming contest on data structures and algorithms", "dsa,algorithms,competitive programming,c++,java", "Contest", "2024-08-20", "#"),
    ("Cloud Computing Summit", "Learn AWS, GCP and Azure fundamentals", "cloud,aws,gcp,azure,devops,linux", "Summit", "2024-08-25", "#"),
    ("Open Source Contribution Drive", "Contribute to real open-source projects on GitHub", "git,github,open source,python,javascript", "Event", "2024-09-01", "#"),
    ("Cybersecurity CTF", "Capture The Flag competition for ethical hacking", "cybersecurity,ethical hacking,networking,linux,python", "Contest", "2024-09-05", "#"),
    ("Data Science Expo", "Showcase data science and analytics projects", "data science,python,pandas,matplotlib,sql,statistics", "Expo", "2024-09-10", "#"),
    ("Mobile App Dev Sprint", "Build an Android/iOS app in 24 hours", "android,flutter,kotlin,java,mobile development", "Hackathon", "2024-09-15", "#"),
    ("Blockchain Workshop", "Intro to blockchain, smart contracts, and Web3", "blockchain,web3,solidity,ethereum,cryptography", "Workshop", "2024-09-20", "#"),
    ("UI/UX Design Sprint", "Design thinking and Figma workshop", "ui,ux,figma,design,product design,user research", "Workshop", "2024-09-25", "#"),
    ("Database Design Workshop", "SQL, NoSQL, and database architecture", "sql,mysql,mongodb,database,postgresql", "Workshop", "2024-10-01", "#"),
    ("DevOps Bootcamp", "CI/CD, Docker, Kubernetes for beginners", "devops,docker,kubernetes,ci cd,linux,bash", "Bootcamp", "2024-10-05", "#"),
    ("NLP & Text Mining Talk", "Natural language processing with Python", "nlp,python,text mining,machine learning,ai", "Talk", "2024-10-10", "#"),
    ("Computer Vision Workshop", "OpenCV and image processing", "computer vision,opencv,python,deep learning,ai", "Workshop", "2024-10-15", "#"),
    ("Startup Pitch Competition", "Pitch your startup idea to investors", "entrepreneurship,startup,pitch,product,business", "Competition", "2024-10-20", "#"),
]

INTERNSHIPS = [
    ("Data Analyst Intern", "TechCorp", "Analyze data using Python and SQL, build dashboards", "python,sql,data analysis,pandas,excel,statistics", "#"),
    ("AI/ML Engineer Intern", "InnovatAI", "Build ML models and deploy to production", "python,machine learning,deep learning,tensorflow,pytorch,ai", "#"),
    ("Frontend Developer Intern", "WebStudio", "Build responsive UIs with React", "react,javascript,html,css,figma,frontend", "#"),
    ("Backend Developer Intern", "CloudBase", "REST APIs with Node.js and databases", "nodejs,javascript,sql,mongodb,rest api,backend", "#"),
    ("Full Stack Intern", "StartupHub", "End-to-end feature development", "python,javascript,react,sql,git,full stack", "#"),
    ("Cybersecurity Analyst Intern", "SecureNet", "Vulnerability assessment and threat analysis", "cybersecurity,linux,networking,python,ethical hacking", "#"),
    ("Cloud Engineer Intern", "CloudSys", "AWS infrastructure and automation scripts", "aws,cloud,python,linux,devops,bash", "#"),
    ("Android Developer Intern", "AppVenture", "Build Android apps with Kotlin", "android,kotlin,java,mobile development,firebase", "#"),
    ("Data Science Intern", "DataLabs", "EDA, feature engineering, and model building", "python,data science,machine learning,sql,pandas,statistics", "#"),
    ("UI/UX Design Intern", "DesignCo", "User research, wireframing, Figma prototypes", "figma,ui,ux,design,user research,product design", "#"),
    ("NLP Research Intern", "AIResearch", "Work on NLP models and text classification", "python,nlp,machine learning,deep learning,pytorch,ai", "#"),
    ("DevOps Intern", "Infratech", "Manage CI/CD pipelines and containerization", "devops,docker,kubernetes,linux,ci cd,aws", "#"),
]

PROJECTS = [
    ("AI Resume Analyzer", "Upload a resume PDF and get skill gap analysis and job match scores", "python,nlp,machine learning,pdf,streamlit,ai", "Intermediate"),
    ("Smart Attendance System", "Face recognition-based attendance using OpenCV", "python,computer vision,opencv,deep learning,database", "Advanced"),
    ("Student Performance Predictor", "Predict exam scores using ML based on study habits", "python,machine learning,pandas,scikit-learn,data science", "Intermediate"),
    ("Campus Event Finder", "Location-aware event discovery app for college students", "python,sql,streamlit,maps api,web development", "Beginner"),
    ("Plagiarism Detector", "Compare documents using NLP similarity techniques", "python,nlp,text mining,cosine similarity,streamlit", "Intermediate"),
    ("Expense Tracker with AI Insights", "Track expenses and get AI-generated saving tips", "python,sql,streamlit,pandas,matplotlib,ai", "Beginner"),
    ("Chatbot for College FAQ", "Answer college FAQs using NLP and intent detection", "python,nlp,chatbot,streamlit,machine learning", "Intermediate"),
    ("Stock Price Predictor", "LSTM-based stock price prediction", "python,deep learning,lstm,pandas,tensorflow,data science", "Advanced"),
    ("Online Code Judge", "Submit code problems and get real-time verdicts", "python,web development,algorithms,docker,backend", "Advanced"),
    ("Mental Health Tracker", "Daily mood journaling app with trend analysis", "python,streamlit,pandas,matplotlib,sql,data analysis", "Beginner"),
    ("Fake News Detector", "Classify news articles as real or fake using ML", "python,nlp,machine learning,scikit-learn,ai,text mining", "Intermediate"),
    ("Smart Library System", "Book recommendation + availability tracking", "python,sql,machine learning,streamlit,recommendation system", "Intermediate"),
    ("Road Pothole Detector", "Detect potholes in road images using computer vision", "python,computer vision,deep learning,opencv,ai", "Advanced"),
    ("Notes Summarizer App", "Upload notes and get AI-generated summaries", "python,nlp,ai,streamlit,text mining,machine learning", "Beginner"),
    ("Peer Tutoring Matcher", "Match students with tutors based on subject needs", "python,sql,streamlit,recommendation system,machine learning", "Intermediate"),
]


def seed():
    init_db()
    conn = get_connection()
    c = conn.cursor()

    # Only seed if tables are empty
    if c.execute("SELECT COUNT(*) FROM events").fetchone()[0] == 0:
        c.executemany(
            "INSERT INTO events (title, description, tags, event_type, date, link) VALUES (?,?,?,?,?,?)",
            EVENTS
        )
        print(f"✅ Inserted {len(EVENTS)} events")
    else:
        print("⚠️  Events already seeded, skipping")

    if c.execute("SELECT COUNT(*) FROM internships").fetchone()[0] == 0:
        c.executemany(
            "INSERT INTO internships (title, company, description, tags, link) VALUES (?,?,?,?,?)",
            INTERNSHIPS
        )
        print(f"✅ Inserted {len(INTERNSHIPS)} internships")
    else:
        print("⚠️  Internships already seeded, skipping")

    if c.execute("SELECT COUNT(*) FROM projects").fetchone()[0] == 0:
        c.executemany(
            "INSERT INTO projects (title, description, tags, difficulty) VALUES (?,?,?,?)",
            PROJECTS
        )
        print(f"✅ Inserted {len(PROJECTS)} projects")
    else:
        print("⚠️  Projects already seeded, skipping")

    conn.commit()
    conn.close()
    print("\n🎉 Database ready!")


if __name__ == "__main__":
    seed()
