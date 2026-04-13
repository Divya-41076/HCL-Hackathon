import streamlit as st
from utils.api import login

def show():
    st.title("🏦 Bank Login")
    st.markdown("---")

    email = st.text_input("Email", placeholder="ravi@bank.com")
    password = st.text_input("Password", type="password", placeholder="password123")

    if st.button("Login", type="primary"):
        if not email or not password:
            st.error("Please enter both email and password.")
            return
        result = login(email, password)
        if result and "customer_id" in result:
            st.session_state["token"] = result["token"]
            st.session_state["customer_id"] = result["customer_id"]
            st.session_state["customer_name"] = result["name"]
            st.success(f"Welcome, {result['name']}!")
            st.rerun()
        else:
            st.error("Invalid credentials. Try ravi@bank.com / password123")
