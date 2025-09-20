# frontend/pages/upload_jd.py
import streamlit as st
from backend.parsing import extract_text

def show():
    st.header("Upload Job Description (JD)")
    uploaded_file = st.file_uploader("Choose a JD file (PDF/DOCX/TXT)", type=['pdf', 'docx', 'txt'])
    if uploaded_file:
        with open(f"database/job_descriptions/{uploaded_file.name}", "wb") as f:
            f.write(uploaded_file.getbuffer())
        text = extract_text(f"database/job_descriptions/{uploaded_file.name}")
        st.success("JD uploaded successfully!")
        st.text_area("Extracted Text", text, height=300)
