import streamlit as st
from utils.api_client import get_accounts, get_insights
 
def render():
    st.markdown(f"### Welcome, {'You' if not st.session_state.get('customer_name') else st.session_state.customer_name} 👋")
    st.caption("Your accounts at a glance")
 
    customer_id = st.session_state.customer_id
    accounts = get_accounts(customer_id)
 
    if not accounts:
        st.info("No accounts found.")
        return
 
    # Account cards grid
    cols = st.columns(len(accounts)) if len(accounts) <= 3 else st.columns(3)
    for i, acc in enumerate(accounts):
        col = cols[i % len(cols)]
        status_color = "🟢" if acc["status"] == "ACTIVE" else ("🔴" if acc["status"] == "FROZEN" else "⚫")
        with col:
            st.metric(
                label=f"{acc['account_type'].capitalize()} #{acc['account_id']}",
                value=f"₹{acc['balance']:,.2f}",
            )
            st.caption(f"{status_color} {acc['status']}")
 
    st.divider()
 
    # Action buttons
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("💸 Transfer money", use_container_width=True):
            st.session_state.page = "transfer"
            st.rerun()
    with col2:
        if st.button("📄 View statement", use_container_width=True):
            st.session_state.page = "history"
            st.rerun()
    with col3:
        if st.button("🔧 My accounts", use_container_width=True):
            st.session_state.page = "account"
            st.rerun()
    with col4:
        ai_clicked = st.button("🤖 AI Insight", use_container_width=True)
 
    # AI Insight section
    if ai_clicked:
        if accounts:
            default_account_id = accounts[0]["account_id"]
            with st.spinner("Generating insight..."):
                result = get_insights(default_account_id)
            insight = result.get("insight", "No insight available.")
            st.session_state["dashboard_insight"] = insight
 
    if st.session_state.get("dashboard_insight"):
        st.info(f"🤖 **AI Insight:** {st.session_state['dashboard_insight']}")
 