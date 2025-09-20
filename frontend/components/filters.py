import streamlit as st

def show_filters(job_titles):
    st.sidebar.subheader("Filters")

    # Job Filter
    job_options = ["All"] + list(job_titles)
    job_id = st.sidebar.selectbox("Select Job", job_options)

    # Score Range Filter
    min_score, max_score = st.sidebar.slider(
        "Relevance Score Range",
        min_value=0,
        max_value=100,
        value=(0, 100),
        step=5
    )

    # Verdict Filter
    verdicts = st.sidebar.multiselect(
        "Filter by Verdict",
        ["High", "Medium", "Low"],
        default=["High", "Medium", "Low"]
    )

    return job_id, min_score, max_score, verdicts
