import streamlit as st
from fastapi import APIRouter

router = APIRouter()

@router.get("/accounts")
def get_accounts():
    return {"accounts": ["Savings", "Current"]}

@router.get("/balance")
def get_balance():
    return {"balance": 5000}

def show():
    st.title("🏦 Account Management")
    st.markdown("---")

    customer_id = st.session_state.get("customer_id")
    accounts = get_accounts(customer_id)

    if not accounts:
        st.warning("No accounts found.")
        return

    acc_options = {f"{a['account_type']} (#{a['account_id']})": a["account_id"] for a in accounts}
    selected = st.selectbox("Select an Account", list(acc_options.keys()))
    account_id = acc_options[selected]

    if st.button("View Details"):
        details = get_balance(account_id)
        st.markdown("### Account Details")
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"**Account ID:** {details['account_id']}")
            st.write(f"**Type:** {details['account_type']}")
        with col2:
            st.write(f"**Status:** {details['status']}")
            st.metric("Balance", f"₹{details['balance']:,.2f}")
