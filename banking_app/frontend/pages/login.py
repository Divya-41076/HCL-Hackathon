import streamlit as st
from utils.api_client import login, register
 
def render():
    st.markdown("""
    <style>
    .login-title { font-size: 22px; font-weight: 600; margin-bottom: 4px; }
    .login-sub { font-size: 13px; color: #888; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)
 
    st.markdown('<div class="login-title">NexaBank</div>', unsafe_allow_html=True)
    st.markdown('<div class="login-sub">Secure online banking</div>', unsafe_allow_html=True)
 
    tab1, tab2 = st.tabs(["Login", "Register"])
 
    # --- LOGIN TAB ---
    with tab1:
        with st.form("login_form"):
            email = st.text_input("Email", placeholder="ravi@demo.com")
            password = st.text_input("Password", type="password", placeholder="••••••••")
            submitted = st.form_submit_button("Login", use_container_width=True)
 
        if submitted:
            if not email or not password:
                st.error("Please enter email and password.")
            else:
                result = login(email, password)
                if "access_token" in result:
                    st.session_state.token = result["access_token"]
                    st.session_state.customer_id = result["customer_id"]
                    st.session_state.page = "dashboard"
                    st.rerun()
                else:
                    st.error(result.get("detail", "Login failed. Check credentials."))
 
    # --- REGISTER TAB ---
    with tab2:
        with st.form("register_form"):
            name = st.text_input("Full name", placeholder="Ravi Kumar")
            col1, col2 = st.columns(2)
            with col1:
                reg_email = st.text_input("Email", placeholder="ravi@demo.com", key="reg_email")
            with col2:
                phone = st.text_input("Phone", placeholder="9876543210")
            address = st.text_input("Address", placeholder="Mumbai")
            reg_password = st.text_input("Password", type="password", placeholder="••••••••", key="reg_pass")
            reg_submitted = st.form_submit_button("Create account", use_container_width=True)
 
        if reg_submitted:
            if not all([name, reg_email, reg_password]):
                st.error("Name, email and password are required.")
            else:
                result = register(name, reg_email, reg_password, phone, address)
                if "customer_id" in result:
                    st.success(f"Account created! Welcome, {result['name']}. Please login.")
                else:
                    st.error(result.get("detail", "Registration failed."))