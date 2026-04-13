import streamlit as st
from utils.api_client import get_accounts, get_transactions, get_insights
 
def render():
    st.markdown("### Account Statement")
    st.caption("Full transaction history")
 
    customer_id = st.session_state.customer_id
    accounts = get_accounts(customer_id)
 
    if not accounts:
        st.info("No accounts found.")
        return
 
    # Account selector — pre-select if coming from dashboard/account page
    options = {f"{a['account_type'].capitalize()} #{a['account_id']}": a["account_id"] for a in accounts}
    
    preselect = st.session_state.get("selected_account_id")
    preselect_label = None
    if preselect:
        for label, aid in options.items():
            if aid == preselect:
                preselect_label = label
                break
 
    default_index = list(options.keys()).index(preselect_label) if preselect_label else 0
    selected_label = st.selectbox("Select account", list(options.keys()), index=default_index)
    selected_id = options[selected_label]
    st.session_state.selected_account_id = selected_id
 
    # Fetch transactions
    transactions = get_transactions(selected_id)
 
    if not transactions:
        st.info("No transactions found for this account.")
    else:
        st.markdown("#### Transactions")
        for txn in transactions:
            is_outgoing = txn["from_account_id"] == selected_id
            direction = "out" if is_outgoing else "in"
            sign = "−" if is_outgoing else "+"
            color = "#A32D2D" if is_outgoing else "#0F6E56"
            label = f"Transfer to Acc #{txn['to_account_id']}" if is_outgoing else f"Received from Acc #{txn['from_account_id']}"
            date = txn.get("date", "")
            if date and "T" in date:
                date = date.split("T")[0]
 
            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown(f"**{label}**")
                st.caption(f"Txn #{txn['transaction_id']} · {date} · {txn['status']}")
            with col2:
                st.markdown(
                    f"<div style='text-align:right;color:{color};font-weight:600;font-size:15px'>"
                    f"{sign} ₹{txn['amount']:,.2f}</div>",
                    unsafe_allow_html=True
                )
            st.divider()
 
    # AI Insight button
    if st.button("🤖 Get AI insight for this account", use_container_width=True):
        with st.spinner("Generating insight..."):
            result = get_insights(selected_id)
        insight = result.get("insight", "No insight available.")
        st.session_state["history_insight"] = insight
 
    if st.session_state.get("history_insight"):
        st.info(f"🤖 **AI Insight:** {st.session_state['history_insight']}")