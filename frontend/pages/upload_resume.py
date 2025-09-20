# frontend/pages/upload_resume.py
import streamlit as st
from backend.parsing import extract_text
import os

def show():
    st.header("Upload Resume(s)")
    uploaded_files = st.file_uploader("Choose Resume files (PDF/DOCX/TXT)", type=['pdf','docx','txt'], accept_multiple_files=True)
    if uploaded_files:
        os.makedirs("database/resumes", exist_ok=True)
        for uploaded_file in uploaded_files:
            path = f"database/resumes/{uploaded_file.name}"
            with open(path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            text = extract_text(path)
            st.success(f"Uploaded: {uploaded_file.name}")
            st.text_area(f"Extracted Text: {uploaded_file.name}", text, height=200)
