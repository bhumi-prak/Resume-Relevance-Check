# frontend/pages/home.py
import streamlit as st
from backend import templates

def run():
    st.title("Student Portal – Upload Resume")

    # JD Selection
    jd_choice = st.selectbox("Select a Job Description", list(templates.TEMPLATES.keys()))
    st.text_area("Job Description Preview", templates.TEMPLATES[jd_choice], height=200)

    # Resume Upload
    uploaded_file = st.file_uploader("Upload your Resume (PDF/DOCX)", type=["pdf", "docx"])
    if uploaded_file:
        st.success(f"Uploaded: {uploaded_file.name}")
        # TODO: Save resume & JD choice into DB
        st.info("Your resume will be evaluated against the selected JD.")
