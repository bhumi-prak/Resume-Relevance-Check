# app.py
import streamlit as st
from backend.database import init_db
from frontend.pages import home, dashboard, login

# -------------------------------
# 1. App Config
# -------------------------------
st.set_page_config(
    page_title="Resume Relevance Check",
    layout="wide"
)

# Initialize Database
init_db()

# -------------------------------
# 2. Session State Initialization
# -------------------------------
if "role" not in st.session_state:
    st.session_state["role"] = "student"  # default role
if "admin_logged_in" not in st.session_state:
    st.session_state["admin_logged_in"] = False

# -------------------------------
# 3. Sidebar Navigation
# -------------------------------
with st.sidebar:
    st.title("Navigation")
    role = st.radio("Login as:", ["Student", "Admin"])
    st.session_state["role"] = role.lower()

# -------------------------------
# 4. Route Pages
# -------------------------------
if st.session_state["role"] == "student":
    home.run()  # Student Home Page

elif st.session_state["role"] == "admin":
    if not st.session_state["admin_logged_in"]:
        login.run()  # Admin Login Page
    else:
        dashboard.show()  # Admin Dashboard Page
