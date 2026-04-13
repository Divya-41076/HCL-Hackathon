import streamlit as st
import pandas as pd
from fastapi import APIRouter

router = APIRouter()

@router.get("/accounts")
def get_accounts():
    return {"accounts": ["Savings", "Current"]}

@router.get("/balance")
def get_balance():
    return {"balance": 5000}

def show():
    st.title("🤖 AI Insights")
    st.markdown("---")

    customer_id = st.session_state.get("customer_id")
    accounts = get_accounts(customer_id)
    acc_options = {f"{a['account_type']} (#{a['account_id']})": a["account_id"] for a in accounts}

    selected = st.selectbox("Select Account", list(acc_options.keys()))
    account_id = acc_options[selected]

    if st.button("Generate Insights", type="primary"):
        data = get_insights(account_id)

        st.markdown("### 📊 Summary")
        st.info(data["summary"])

        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total Spent", f"₹{data['total_spent']:,.2f}")
        with col2:
            st.metric("Total Received", f"₹{data['total_received']:,.2f}")

        if data.get("unusual"):
            st.markdown("### ⚠️ Unusual Transactions")
            for u in data["unusual"]:
                st.warning(f"Transaction #{u['transaction_id']} — ₹{u['amount']:,.2f}")

        if data.get("transactions"):
            st.markdown("### 📈 Spending Chart")
            txns = data["transactions"]
            debits = [t["amount"] for t in txns if t["from_account"] == account_id]
            credits = [t["amount"] for t in txns if t["to_account"] == account_id]
            chart_data = pd.DataFrame({
                "Debits": pd.Series(debits),
                "Credits": pd.Series(credits)
            }).fillna(0)
            st.bar_chart(chart_data)
