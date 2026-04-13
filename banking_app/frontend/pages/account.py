import streamlit as st
from utils.api_client import get_accounts, get_account
 
def render():
    st.markdown("### My Accounts")
    st.caption("View and manage your accounts")
 
    customer_id = st.session_state.customer_id
    accounts = get_accounts(customer_id)
 
    if not accounts:
        st.info("No accounts found.")
        return
 
    # Account selector
    options = {f"{a['account_type'].capitalize()} #{a['account_id']}": a["account_id"] for a in accounts}
    selected_label = st.selectbox("Select account", list(options.keys()))
    selected_id = options[selected_label]
    st.session_state.selected_account_id = selected_id
 
    # Fetch selected account detail
    acc = get_account(selected_id)
 
    st.divider()
 
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Account details**")
        st.markdown(f"**Account ID:** {acc['account_id']}")
        st.markdown(f"**Type:** {acc['account_type']}")
        status_color = "🟢" if acc["status"] == "ACTIVE" else "🔴"
        st.markdown(f"**Status:** {status_color} {acc['status']}")
    with col2:
        st.metric("Current Balance", f"₹{acc['balance']:,.2f}")
 
    st.divider()
 
    col1, col2 = st.columns(2)
    with col1:
        if st.button("💸 Transfer from this account", use_container_width=True):
            st.session_state.selected_account_id = selected_id
            st.session_state.page = "transfer"
            st.rerun()
    with col2:
        if st.button("📄 View statement", use_container_width=True):
            st.session_state.selected_account_id = selected_id
            st.session_state.page = "history"
            st.rerun()