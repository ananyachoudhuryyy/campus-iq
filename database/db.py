import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "campus.db")


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # lets you access columns by name
    return conn


def init_db():
    """Create all tables if they don't exist."""
    conn = get_connection()
    c = conn.cursor()

    c.executescript("""
        CREATE TABLE IF NOT EXISTS students (
            student_id   INTEGER PRIMARY KEY AUTOINCREMENT,
            name         TEXT NOT NULL,
            email        TEXT UNIQUE NOT NULL,
            password     TEXT NOT NULL,
            year         INTEGER,
            branch       TEXT,
            career_goal  TEXT
        );

        CREATE TABLE IF NOT EXISTS skills (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER,
            skill      TEXT,
            FOREIGN KEY (student_id) REFERENCES students(student_id)
        );

        CREATE TABLE IF NOT EXISTS interests (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER,
            interest   TEXT,
            FOREIGN KEY (student_id) REFERENCES students(student_id)
        );

        CREATE TABLE IF NOT EXISTS events (
            event_id    INTEGER PRIMARY KEY AUTOINCREMENT,
            title       TEXT NOT NULL,
            description TEXT,
            tags        TEXT,
            event_type  TEXT,
            date        TEXT,
            link        TEXT
        );

        CREATE TABLE IF NOT EXISTS internships (
            internship_id INTEGER PRIMARY KEY AUTOINCREMENT,
            title         TEXT NOT NULL,
            company       TEXT,
            description   TEXT,
            tags          TEXT,
            link          TEXT
        );

        CREATE TABLE IF NOT EXISTS projects (
            project_id  INTEGER PRIMARY KEY AUTOINCREMENT,
            title       TEXT NOT NULL,
            description TEXT,
            tags        TEXT,
            difficulty  TEXT
        );

        CREATE TABLE IF NOT EXISTS search_log (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER,
            query      TEXT,
            timestamp  DATETIME DEFAULT CURRENT_TIMESTAMP
        );
    """)

    conn.commit()
    conn.close()


# ─── STUDENT ───────────────────────────────────────────────

def create_student(name, email, password, year, branch, career_goal, skills, interests):
    conn = get_connection()
    c = conn.cursor()
    try:
        c.execute(
            "INSERT INTO students (name, email, password, year, branch, career_goal) VALUES (?,?,?,?,?,?)",
            (name, email, password, year, branch, career_goal)
        )
        student_id = c.lastrowid

        for skill in skills:
            if skill.strip():
                c.execute("INSERT INTO skills (student_id, skill) VALUES (?,?)", (student_id, skill.strip()))

        for interest in interests:
            if interest.strip():
                c.execute("INSERT INTO interests (student_id, interest) VALUES (?,?)", (student_id, interest.strip()))

        conn.commit()
        return student_id
    except sqlite3.IntegrityError:
        return None  # email already exists
    finally:
        conn.close()


def get_student_by_email(email, password):
    conn = get_connection()
    c = conn.cursor()
    row = c.execute(
        "SELECT * FROM students WHERE email=? AND password=?", (email, password)
    ).fetchone()
    conn.close()
    return dict(row) if row else None


def get_student_profile(student_id):
    conn = get_connection()
    c = conn.cursor()

    student = c.execute("SELECT * FROM students WHERE student_id=?", (student_id,)).fetchone()
    skills = c.execute("SELECT skill FROM skills WHERE student_id=?", (student_id,)).fetchall()
    interests = c.execute("SELECT interest FROM interests WHERE student_id=?", (student_id,)).fetchall()

    conn.close()

    if not student:
        return None

    return {
        **dict(student),
        "skills": [r["skill"] for r in skills],
        "interests": [r["interest"] for r in interests],
    }


def update_student_profile(student_id, year, branch, career_goal, skills, interests):
    conn = get_connection()
    c = conn.cursor()

    c.execute(
        "UPDATE students SET year=?, branch=?, career_goal=? WHERE student_id=?",
        (year, branch, career_goal, student_id)
    )

    c.execute("DELETE FROM skills WHERE student_id=?", (student_id,))
    for skill in skills:
        if skill.strip():
            c.execute("INSERT INTO skills (student_id, skill) VALUES (?,?)", (student_id, skill.strip()))

    c.execute("DELETE FROM interests WHERE student_id=?", (student_id,))
    for interest in interests:
        if interest.strip():
            c.execute("INSERT INTO interests (student_id, interest) VALUES (?,?)", (student_id, interest.strip()))

    conn.commit()
    conn.close()


def get_all_students():
    conn = get_connection()
    rows = conn.execute("SELECT * FROM students").fetchall()
    conn.close()
    return [dict(r) for r in rows]


# ─── EVENTS / INTERNSHIPS / PROJECTS ───────────────────────

def get_all_events():
    conn = get_connection()
    rows = conn.execute("SELECT * FROM events").fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_all_internships():
    conn = get_connection()
    rows = conn.execute("SELECT * FROM internships").fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_all_projects():
    conn = get_connection()
    rows = conn.execute("SELECT * FROM projects").fetchall()
    conn.close()
    return [dict(r) for r in rows]


# ─── ANALYTICS ─────────────────────────────────────────────

def get_all_skills():
    conn = get_connection()
    rows = conn.execute("SELECT skill FROM skills").fetchall()
    conn.close()
    return [r["skill"] for r in rows]


def get_all_interests():
    conn = get_connection()
    rows = conn.execute("SELECT interest FROM interests").fetchall()
    conn.close()
    return [r["interest"] for r in rows]


def log_search(student_id, query):
    conn = get_connection()
    conn.execute("INSERT INTO search_log (student_id, query) VALUES (?,?)", (student_id, query))
    conn.commit()
    conn.close()


def get_search_logs():
    conn = get_connection()
    rows = conn.execute("SELECT query FROM search_log").fetchall()
    conn.close()
    return [r["query"] for r in rows]
