import streamlit as st

def run():
    st.title("Admin Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username == "admin" and password == "innomatics123":  # ✅ Replace with env-based check later
            st.session_state["admin_logged_in"] = True
            st.success("Login successful! Go to Dashboard from sidebar.")
        else:
            st.error("Invalid credentials")
