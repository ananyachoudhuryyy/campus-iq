from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd


def build_student_vector(skills: list, interests: list) -> str:
    """Combine skills and interests into a single text string for vectorization."""
    return " ".join(skills + interests).lower()


def recommend(student_skills: list, student_interests: list, items: list, tag_key: str, top_n: int = 5) -> list:
    """
    Generic recommender using TF-IDF + cosine similarity.

    Args:
        student_skills:    list of student's skills
        student_interests: list of student's interests
        items:             list of dicts (events / internships / projects)
        tag_key:           the dict key that holds the tags string
        top_n:             number of recommendations to return

    Returns:
        List of dicts sorted by similarity score (highest first)
    """
    if not items:
        return []

    student_text = build_student_vector(student_skills, student_interests)
    item_texts = [item[tag_key].replace(",", " ").lower() for item in items]

    # Build TF-IDF matrix over [student] + all items
    corpus = [student_text] + item_texts
    vectorizer = TfidfVectorizer(stop_words="english")
    tfidf_matrix = vectorizer.fit_transform(corpus)

    # Similarity between student (index 0) and each item
    similarities = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:]).flatten()

    # Attach scores and sort
    scored = []
    for idx, item in enumerate(items):
        scored.append({**item, "score": round(float(similarities[idx]), 3)})

    scored.sort(key=lambda x: x["score"], reverse=True)
    return scored[:top_n]


def recommend_events(student_skills, student_interests, events, top_n=5):
    return recommend(student_skills, student_interests, events, "tags", top_n)


def recommend_internships(student_skills, student_interests, internships, top_n=5):
    return recommend(student_skills, student_interests, internships, "tags", top_n)


def recommend_projects(student_skills, student_interests, projects, top_n=5):
    return recommend(student_skills, student_interests, projects, "tags", top_n)
