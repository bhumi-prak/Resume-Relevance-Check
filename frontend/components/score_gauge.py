# frontend/components/score_gauge.py
import streamlit as st

def show_score(score):
    # Display relevance score as metric
    st.metric(label="Relevance Score", value=f"{score}/100")
