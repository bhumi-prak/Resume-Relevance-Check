# app.py
import streamlit as st
from pathlib import Path
import pandas as pd
import sqlite3
import uuid
import datetime
import altair as alt
import re
import numpy as np

# NEW imports
import pdfplumber
import docx
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity as sklearn_cosine

# ---------- CONFIG ----------
DB_PATH = Path("resume_relevance.db")
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

# ---------- DB helpers ----------
def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
    CREATE TABLE IF NOT EXISTS jobs (
        id TEXT PRIMARY KEY, title TEXT, jd_text TEXT, created_at TEXT
    )
    ''')
    c.execute('''
    CREATE TABLE IF NOT EXISTS resumes (
        id TEXT PRIMARY KEY, filename TEXT, filepath TEXT, uploaded_at TEXT
    )
    ''')
    c.execute('''
    CREATE TABLE IF NOT EXISTS evaluations (
        id TEXT PRIMARY KEY, job_id TEXT, resume_id TEXT, score REAL,
        verdict TEXT, missing TEXT, suggestions TEXT, created_at TEXT
    )
    ''')
    conn.commit()
    conn.close()

def insert_job(job_id, title, jd_text):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('INSERT INTO jobs (id,title,jd_text,created_at) VALUES (?,?,?,?)',
              (job_id,title,jd_text, datetime.datetime.utcnow().isoformat()))
    conn.commit()
    conn.close()

def list_jobs():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql("SELECT * FROM jobs ORDER BY created_at DESC", conn)
    conn.close()
    return df

def insert_resume(res_id, filename, filepath):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('INSERT INTO resumes (id,filename,filepath,uploaded_at) VALUES (?,?,?,?)',
              (res_id,filename,filepath, datetime.datetime.utcnow().isoformat()))
    conn.commit()
    conn.close()

def list_resumes():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql("SELECT * FROM resumes ORDER BY uploaded_at DESC", conn)
    conn.close()
    return df

def insert_evaluation(eval_id, job_id, resume_id, score, verdict, missing, suggestions):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('INSERT INTO evaluations (id,job_id,resume_id,score,verdict,missing,suggestions,created_at) VALUES (?,?,?,?,?,?,?,?)',
              (eval_id,job_id,resume_id,score,verdict,missing,suggestions, datetime.datetime.utcnow().isoformat()))
    conn.commit()
    conn.close()

def list_evaluations(job_id=None):
    conn = sqlite3.connect(DB_PATH)
    if job_id:
        df = pd.read_sql("SELECT * FROM evaluations WHERE job_id=? ORDER BY created_at DESC", conn, params=(job_id,))
    else:
        df = pd.read_sql("SELECT * FROM evaluations ORDER BY created_at DESC", conn)
    conn.close()
    return df

# ---------- Parsing & Scoring ----------
def parse_resume_file(filepath: Path):
    """
    Parse resume text from PDF or DOCX.
    Returns a dict with text + extracted skills/education/projects (basic regex).
    """
    text = ""

    if str(filepath).lower().endswith(".pdf"):
        with pdfplumber.open(filepath) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ""

    elif str(filepath).lower().endswith(".docx"):
        doc = docx.Document(filepath)
        text = "\n".join([p.text for p in doc.paragraphs])

    # crude skill extraction
    skills = re.findall(r"\b(Python|Java|C\+\+|SQL|Excel|AWS|React|Flask|Django|Docker|Kubernetes|Tableau|Power BI)\b",
                        text, flags=re.I)

    education = re.findall(r"(B\.?Tech|M\.?Tech|B\.?Sc|M\.?Sc|MBA|Bachelor|Master)", text, flags=re.I)
    projects = re.findall(r"Project[:\- ](.+)", text, flags=re.I)

    return {
        "text": text,
        "skills": list(set([s.strip() for s in skills])),
        "education": list(set(education)),
        "projects": list(set(projects))
    }

def parse_job_description(jd_text: str):
    """
    Extract job title, must-have, and good-to-have skills from JD.
    """
    must, good = [], []
    for line in jd_text.splitlines():
        if "must" in line.lower():
            must.extend(re.findall(r"[A-Za-z\+\# ]+", line))
        elif "good" in line.lower():
            good.extend(re.findall(r"[A-Za-z\+\# ]+", line))

    title = jd_text.splitlines()[0] if jd_text else "Untitled Role"
    return {"title": title, "must_have": [m.strip() for m in must if m.strip()],
            "good_to_have": [g.strip() for g in good if g.strip()]}

def compute_relevance_score(parsed_resume, parsed_jd):
    """
    Compute a 0-100 relevance score between resume and JD.
    Combines TF-IDF cosine similarity with must-have keyword coverage.
    """
    resume_text = parsed_resume["text"]
    jd_text = "\n".join([parsed_jd["title"]] + parsed_jd["must_have"] + parsed_jd["good_to_have"])

    if not resume_text.strip() or not jd_text.strip():
        return 0, "Low", "Missing JD or resume content", "Please re-upload clean files."

    # cosine similarity
    vectorizer = TfidfVectorizer().fit([resume_text, jd_text])
    vecs = vectorizer.transform([resume_text, jd_text])
    cos_sim = sklearn_cosine(vecs[0], vecs[1])[0][0]

    # must-have coverage
    must_have = parsed_jd["must_have"]
    matched = [m for m in must_have if m.lower() in resume_text.lower()]
    coverage = len(matched) / len(must_have) if must_have else 0

    # final score
    score = int((0.7 * cos_sim + 0.3 * coverage) * 100)

    verdict = "High" if score >= 70 else "Medium" if score >= 40 else "Low"
    missing = [m for m in must_have if m.lower() not in resume_text.lower()]
    suggestions = f"Consider adding: {', '.join(missing)}" if missing else "Resume covers most required skills."

    return score, verdict, ", ".join(missing), suggestions

# ---------- UI ----------
st.set_page_config(layout="wide", page_title="Automated Resume Relevance Check System")
init_db()

st.markdown("<h1 style='color:#2f6f4f'>Automated Resume Relevance Check System — Placement Dashboard</h1>", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("Filters & Actions")
    region = st.selectbox("Region", ["All", "Hyderabad", "Bangalore", "Pune", "Delhi NCR"])
    st.markdown("---")
    st.subheader("Job templates")
    template_choice = st.selectbox("Choose Template", ["-- none --", "Software Engineer (Full Stack)", "Data Analyst", "Associate Product Manager"])
    st.markdown("---")
    score_min, score_max = st.slider("Score range", 0, 100, (30, 100))
    verdict_filter = st.multiselect("Verdict", ["High", "Medium", "Low"], default=["High","Medium","Low"])
    skill_query = st.text_input("Skill filter (comma separated)", "")
    st.markdown("---")
    st.subheader("Actions")
    if st.button("Export Shortlist (CSV)"):
        st.info("Export will include evaluated results for selected job.")

# MAIN: job create / JD editor
col1, col2 = st.columns([2,1])

with col1:
    st.subheader("Job Details (create / edit)")
    default_jd = ""
    if template_choice == "Software Engineer (Full Stack)":
        default_jd = """Software Engineer (Full Stack)
Must-have: Python, Django/Flask, REST APIs, SQL, Git
Good-to-have: React, TypeScript, Docker, Kubernetes, AWS
"""
    elif template_choice == "Data Analyst":
        default_jd = """Data Analyst
Must-have: SQL, Excel, Python (pandas), data visualization (Tableau/Power BI)
Good-to-have: Statistics, A/B testing, ETL, BigQuery
"""
    elif template_choice == "Associate Product Manager":
        default_jd = """Associate Product Manager
Must-have: Product thinking, stakeholder communication, basic analytics (SQL/Excel)
Good-to-have: Wireframing, user research, Agile
"""
    jd_text = st.text_area("Job Description (editable)", value=default_jd, height=260)
    job_title = st.text_input("Role title", value=(jd_text.splitlines()[0] if jd_text else "Untitled Role"))
    if st.button("Save Job"):
        job_id = str(uuid.uuid4())
        insert_job(job_id, job_title, jd_text)
        st.success(f"Saved job '{job_title}'")

    st.markdown("### Recent Jobs")
    jobs_df = list_jobs()
    if not jobs_df.empty:
        st.dataframe(jobs_df[["title", "created_at"]].head(6))
    else:
        st.info("No jobs created yet.")

with col2:
    st.subheader("Uploads")
    uploaded_jd = st.file_uploader("Upload Job Description (TXT/DOCX/PDF)", type=["txt","pdf","docx"])
    if uploaded_jd:
        raw = uploaded_jd.read()
        p = UPLOAD_DIR / f"jd_{uuid.uuid4().hex}_{uploaded_jd.name}"
        p.write_bytes(raw)
        st.success(f"Saved JD file to {p}")

    uploaded_resume = st.file_uploader("Upload Resume(s) (PDF/DOCX)", type=["pdf","docx"], accept_multiple_files=True)
    if uploaded_resume:
        for f in uploaded_resume:
            res_id = str(uuid.uuid4())
            p = UPLOAD_DIR / f"resume_{res_id}_{f.name}"
            p.write_bytes(f.read())
            insert_resume(res_id, f.name, str(p))
        st.success("Uploaded resumes.")

st.markdown("---")
# Evaluation area
st.subheader("Evaluate & Results")
colA, colB = st.columns([2,1])
with colA:
    jobs_df = list_jobs()
    job_options = ["-- select job --"] + jobs_df["title"].tolist()
    job_selected = st.selectbox("Existing Jobs", job_options)
    if st.button("Evaluate All Resumes for Selected Job"):
        if job_selected == "-- select job --":
            st.error("Pick a saved job first.")
        else:
            job_row = jobs_df[jobs_df["title"] == job_selected].iloc[0]
            job_id = job_row["id"]
            parsed_jd = parse_job_description(job_row["jd_text"])
            resumes_df = list_resumes()
            if resumes_df.empty:
                st.warning("No resumes uploaded.")
            else:
                progress = st.progress(0)
                total = len(resumes_df)
                for i, row in resumes_df.iterrows():
                    parsed_resume = parse_resume_file(Path(row["filepath"]))
                    score, verdict, missing, suggestions = compute_relevance_score(parsed_resume, parsed_jd)
                    eval_id = str(uuid.uuid4())
                    insert_evaluation(eval_id, job_id, row["id"], score, verdict, missing, suggestions)
                    progress.progress(int((i+1)/total*100))
                st.success(f"Evaluated {len(resumes_df)} resumes for job '{job_selected}'.")

with colB:
    st.markdown("**Quick analytics**")
    evaluations_all = list_evaluations()
    if not evaluations_all.empty:
        st.metric("Evaluations stored", len(evaluations_all))
    else:
        st.info("No evaluations yet.")

st.markdown("### Evaluation Results Table")
if job_selected and job_selected != "-- select job --":
    job_row = jobs_df[jobs_df["title"] == job_selected].iloc[0]
    evals = list_evaluations(job_row["id"])
    if evals.empty:
        st.info("No evaluations for this job yet.")
    else:
        resumes = list_resumes()
        merged = evals.merge(resumes, left_on="resume_id", right_on="id", how="left")
        display_df = merged[["filename","score","verdict","missing","suggestions","created_at"]].rename(columns={"filename":"Resume"})
        st.dataframe(display_df)
        chart_df = display_df.groupby("verdict").size().reset_index(name="count")
        chart = alt.Chart(chart_df).mark_bar().encode(x="verdict", y="count")
        st.altair_chart(chart, use_container_width=True)
else:
    st.info("Select a job to view evaluations.")
