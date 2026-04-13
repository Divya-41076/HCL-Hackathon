import streamlit as st
from utils.api import get_accounts

def show():
    st.title(f"👋 Welcome, {st.session_state.get('customer_name', 'User')}!")
    st.markdown("---")

    customer_id = st.session_state.get("customer_id")
    accounts = get_accounts(customer_id)

    st.subheader("Your Accounts")
    cols = st.columns(len(accounts))
    for i, acc in enumerate(accounts):
        with cols[i]:
            st.metric(
                label=f"{acc['account_type']} (#{acc['account_id']})",
                value=f"₹{acc['balance']:,.2f}",
                delta=acc["status"]
            )

    st.markdown("---")
    st.subheader("Quick Actions")
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        if st.button("💸 Transfer Money"):
            st.session_state["page"] = "Transfer"
            st.rerun()
    with c2:
        if st.button("📋 Transactions"):
            st.session_state["page"] = "Transactions"
            st.rerun()
    with c3:
        if st.button("🛠 Service Requests"):
            st.session_state["page"] = "Requests"
            st.rerun()
    with c4:
        if st.button("🤖 AI Insights"):
            st.session_state["page"] = "AI Insights"
            st.rerun()
