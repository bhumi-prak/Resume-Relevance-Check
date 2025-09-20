# frontend/components/header.py
import streamlit as st

def show_header():
    st.markdown(
        """
        <div style='background-color:#4CAF50;padding:10px;border-radius:5px'>
            <h2 style='color:white;text-align:center;'>📄 Automated Resume Relevance System</h2>
        </div>
        """,
        unsafe_allow_html=True
    )
