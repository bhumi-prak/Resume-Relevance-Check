import sqlite3
import os
from backend.logger import get_logger

logger = get_logger("database")


DB_PATH = "database/resume_checker.db"

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cur = conn.cursor()
    
    # Jobs table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS jobs (
            id INTEGER PRIMARY KEY,
            title TEXT,
            description TEXT
        )
    """)
    
    # Resumes table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS resumes (
            id INTEGER PRIMARY KEY,
            job_id INTEGER,
            name TEXT,
            college TEXT,
            location TEXT,
            resume_text TEXT
        )
    """)
    
    # Evaluations table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS evaluations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            resume_id INTEGER,
            job_id INTEGER,
            score INTEGER,
            verdict TEXT,
            missing_skills TEXT,
            feedback TEXT
        )
    """)
    
    conn.commit()
    conn.close()

def insert_job(id, title, description):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO jobs (id, title, description) VALUES (?, ?, ?)", 
                    (id, title, description))
        conn.commit()
    except sqlite3.IntegrityError:
        print("⚠️ Duplicate job ignored:", title)
    finally:
        conn.close()


def insert_resume(id, job_id, name, college, location, resume_text, file_hash):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            INSERT INTO resumes (id, job_id, name, college, location, resume_text, file_hash) 
            VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (id, job_id, name, college, location, resume_text, file_hash))
        conn.commit()
    except sqlite3.IntegrityError:
        print("⚠️ Duplicate resume ignored:", name)
    finally:
        conn.close()


def init_db():
    os.makedirs("database", exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    # Jobs table
    c.execute("""
    CREATE TABLE IF NOT EXISTS jobs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        description TEXT
    )
    """)
    # Resumes table
    c.execute("""
    CREATE TABLE IF NOT EXISTS resumes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        college TEXT,
        location TEXT,
        filename TEXT,
        content TEXT
    )
    """)
    # Evaluations table
    c.execute("""
    CREATE TABLE IF NOT EXISTS evaluations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        resume_id INTEGER,
        job_id INTEGER,
        score INTEGER,
        verdict TEXT,
        missing_skills TEXT,
        feedback TEXT,
        FOREIGN KEY(resume_id) REFERENCES resumes(id),
        FOREIGN KEY(job_id) REFERENCES jobs(id)
    )
    """)
    conn.commit()
    conn.close()

def get_jobs():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT id, title FROM jobs")
    jobs = [{"id": row[0], "title": row[1]} for row in c.fetchall()]
    conn.close()
    return jobs

def get_resumes_for_job(job_id, min_score=0, max_score=100, verdicts=None):
    verdicts = verdicts or ["High","Medium","Low"]
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    query = """
    SELECT r.id, r.name, r.college, r.location, e.score, e.verdict, r.content
    FROM resumes r
    LEFT JOIN evaluations e ON r.id = e.resume_id AND e.job_id=?
    WHERE (e.score BETWEEN ? AND ? OR e.score IS NULL)
    AND (e.verdict IN ({seq}) OR e.verdict IS NULL)
    """.format(seq=','.join('?'*len(verdicts)))
    params = [job_id, min_score, max_score] + verdicts
    c.execute(query, params)
    resumes = []
    for row in c.fetchall():
        resumes.append({
            "id": row[0],
            "name": row[1],
            "college": row[2],
            "location": row[3],
            "score": row[4] if row[4] is not None else 0,
            "verdict": row[5] if row[5] is not None else "Not Evaluated",
            "resume_text": row[6]
        })
    conn.close()
    return resumes

def insert_evaluation(resume_id, job_id, score, verdict, missing_skills, feedback):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        INSERT INTO evaluations(resume_id, job_id, score, verdict, missing_skills, feedback)
        VALUES (?,?,?,?,?,?)
    """, (resume_id, job_id, score, verdict, ",".join(missing_skills), feedback))
    conn.commit()
    conn.close()

# backend/database.py
def seed_jobs():
    jobs = [
        {"id": 1, "title": "Data Analyst", "description": "Python, SQL, Excel required"},
        {"id": 2, "title": "Machine Learning Intern", "description": "Python, ML, Pandas"}
    ]
    for job in jobs:
        # Insert into jobs table if not exists
        insert_job(job["id"], job["title"], job["description"])

# backend/database.py
def seed_resumes():
    resumes = [
        {"id": 1, "job_id": 1, "name": "Alice", "college": "ABC College", "location": "Hyderabad", "resume_text": "Python, SQL, Excel"},
        {"id": 2, "job_id": 1, "name": "Bob", "college": "XYZ University", "location": "Bangalore", "resume_text": "Python, Excel"}
    ]
    for r in resumes:
        insert_resume(r["id"], r["job_id"], r["name"], r["college"], r["location"], r["resume_text"])

