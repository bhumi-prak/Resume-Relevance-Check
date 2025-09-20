# app.py
import sqlite3
import streamlit as st
from backend.database import init_db
from frontend.pages import home, dashboard, login
import hashlib




DB_PATH = "database/resume_checker.db"


# -------------------------------
# 1. App Config
# -------------------------------
st.set_page_config(
    page_title="Resume Relevance Check",
    layout="wide"
)

def get_file_hash(file_bytes):
    return hashlib.sha256(file_bytes).hexdigest()

# Initialize Database
def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # Jobs table
    c.execute('''
    CREATE TABLE IF NOT EXISTS jobs (
        id TEXT PRIMARY KEY,
        title TEXT,
        jd_text TEXT,
        created_at TEXT
    )
    ''')

    # Resumes table with file_hash
    c.execute('''
    CREATE TABLE IF NOT EXISTS resumes (
        id TEXT PRIMARY KEY,
        filename TEXT,
        filepath TEXT,
        file_hash TEXT UNIQUE,   -- ✅ unique hash per resume file
        uploaded_at TEXT
    )
    ''')

    # Evaluations table
    c.execute('''
    CREATE TABLE IF NOT EXISTS evaluations (
        id TEXT PRIMARY KEY,
        job_id TEXT,
        resume_id TEXT,
        score REAL,
        verdict TEXT,
        missing TEXT,
        suggestions TEXT,
        created_at TEXT
    )
    ''')
    conn.commit()
    conn.close()


# -------------------------------
# 2. Session State Initialization
# -------------------------------
if "role" not in st.session_state:
    st.session_state["role"] = "student"  # default role
if "admin_logged_in" not in st.session_state:
    st.session_state["admin_logged_in"] = False

# -------------------------------
# 3. Sidebar Navigation
# -------------------------------
with st.sidebar:
    st.title("Navigation")
    role = st.radio("Login as:", ["Student", "Admin"])
    st.session_state["role"] = role.lower()

# -------------------------------
# 4. Route Pages
# -------------------------------
if st.session_state["role"] == "student":
    home.run()  # Student Home Page

elif st.session_state["role"] == "admin":
    if not st.session_state["admin_logged_in"]:
        login.run()  # Admin Login Page
    else:
        dashboard.show()  # Admin Dashboard Page
