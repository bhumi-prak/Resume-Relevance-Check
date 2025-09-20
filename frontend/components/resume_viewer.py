# frontend/components/resume_viewer.py
import streamlit as st

def show_resume(name, college, location, text, missing_skills=None, feedback=None):
    st.subheader(f"{name} ({college}, {location})")
    
    st.markdown("### Resume Content")
    st.text_area("Resume Text", text, height=300)
    
    if missing_skills:
        st.markdown("### Missing Skills")
        st.write(missing_skills)
    
    if feedback:
        st.markdown("### LLM Feedback")
        st.write(feedback)
