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
    st.title("🛠 Service Requests")
    st.markdown("---")

    customer_id = st.session_state.get("customer_id")

    st.subheader("Create New Request")
    req_type = st.selectbox("Request Type", ["Card Issue", "Transaction Issue", "Account Issue", "Loan Query", "Other"])
    description = st.text_area("Description", placeholder="Describe your issue...")

    if st.button("Submit Request", type="primary"):
        if not description:
            st.error("Please provide a description.")
            return
        result = create_service_request(customer_id, req_type, description)
        st.success(result.get("status", "Request submitted!"))

    st.markdown("---")
    st.subheader("Your Requests")
    reqs = get_service_requests(customer_id)
    if not reqs:
        st.info("No service requests found.")
        return

    data = []
    for r in reqs:
        data.append({
            "ID": r["request_id"],
            "Type": r["type"],
            "Description": r["description"],
            "Status": r["status"],
            "Date": r["created_at"]
        })
    df = pd.DataFrame(data)
    st.dataframe(df, use_container_width=True, hide_index=True)
