# frontend/components/analytics.py
import streamlit as st
import matplotlib.pyplot as plt

def show_analytics(df=None):
    st.subheader("Resume Evaluation Analytics")

    if df is None or df.empty:
        st.info("No data available for analytics.")
        return

    # Verdict Distribution
    verdict_counts = df["verdict"].value_counts().to_dict()
    fig, ax = plt.subplots()
    ax.bar(verdict_counts.keys(), verdict_counts.values())
    ax.set_title("Verdict Distribution")
    st.pyplot(fig)

    # Average Score
    avg_score = round(df["relevance_score"].mean(), 2)
    st.metric("Average Relevance Score", f"{avg_score}/100")
