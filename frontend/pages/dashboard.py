import streamlit as st
import pandas as pd
import sqlite3

from frontend.components.filters import show_filters
from frontend.components.score_gauge import show_score
from frontend.components.resume_viewer import show_resume
from frontend.components.analytics import show_analytics
from backend.database import get_jobs, get_resumes_for_job
from backend.relevance_scoring import evaluate_resume_for_job

DB_PATH = "database/resume_checker.db"

def show():
    st.title("Placement Team Dashboard")

    # Sidebar Filters
    jobs_list = get_jobs()
    job_id, min_score, max_score, verdicts = show_filters(jobs_list)

    # Fetch resumes based on filters
    resumes = get_resumes_for_job(
        job_id=job_id,
        min_score=min_score,
        max_score=max_score,
        verdicts=verdicts
    )

    # Layout
    col1, col2 = st.columns([3, 1])

    # Column 1: Resume List
    with col1:
        st.subheader("Resumes")
        if not resumes:
            st.info("No resumes found for the selected filters.")
        else:
            for r in resumes:
                cols = st.columns([6, 1, 1, 1])
                cols[0].markdown(f"**{r['name']}**  \n{r['college']}  \n{r['location']}")
                cols[1].metric("Score", r['score'])
                cols[2].markdown(r['verdict'])
                if cols[3].button("Review", key=f"review_{r['id']}"):
                    st.session_state['selected_resume'] = r['id']

    # Column 2: Actions
    with col2:
        st.subheader("Actions")
        if st.button("Evaluate All Resumes"):
            if resumes:
                for r in resumes:
                    evaluate_resume_for_job(resume_id=r['id'], job_id=job_id)
                st.success("All resumes evaluated!")
            else:
                st.warning("No resumes to evaluate for this job.")

    # Resume Review Panel
    if 'selected_resume' in st.session_state:
        sel = st.session_state['selected_resume']
        st.markdown("---")
        st.header("Resume Review")

        eval_res = evaluate_resume_for_job(resume_id=sel, job_id=job_id)

        # Show score gauge
        show_score(eval_res['score'])

        # Show resume details
        show_resume(
            name=eval_res['name'],
            college=eval_res['college'],
            location=eval_res['location'],
            text=eval_res['resume_text'],
            missing_skills=eval_res['missing_skills'],
            feedback=eval_res['feedback']
        )

    # Analytics & Reports
    st.markdown("---")
    st.subheader("Analytics & Reports")
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql("""
        SELECT r.filename, j.title as job_title, e.relevance_score, e.verdict, e.feedback
        FROM evaluations e
        JOIN resumes r ON e.resume_id = r.id
        JOIN jobs j ON e.job_id = j.id
    """, conn)
    conn.close()

    if not df.empty:
        show_analytics(df)
    else:
        st.info("No evaluation data yet.")
