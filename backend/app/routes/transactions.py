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
    st.title("📋 Transaction History")
    st.markdown("---")

    customer_id = st.session_state.get("customer_id")
    accounts = get_accounts(customer_id)
    acc_options = {f"{a['account_type']} (#{a['account_id']})": a["account_id"] for a in accounts}

    selected = st.selectbox("Select Account", list(acc_options.keys()))
    account_id = acc_options[selected]

    txns = get_transactions(account_id)
    if not txns:
        st.info("No transactions found.")
        return

    data = []
    for t in txns:
        tx_type = "Debit" if t["from_account"] == account_id else "Credit"
        data.append({
            "ID": t["transaction_id"],
            "Date": t["created_at"],
            "Amount": f"₹{t['amount']:,.2f}",
            "Type": tx_type,
            "Status": t["status"]
        })

    df = pd.DataFrame(data)
    st.dataframe(df, use_container_width=True, hide_index=True)
