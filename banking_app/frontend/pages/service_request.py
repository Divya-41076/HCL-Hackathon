import streamlit as st
from utils.api_client import create_service_request, get_service_request
 
REQUEST_TYPES = {
    "Card issue": "CARD_ISSUE",
    "Statement": "STATEMENT",
    "Cheque": "CHEQUE",
}
 
STATUS_COLORS = {
    "OPEN": "🔵",
    "IN_PROGRESS": "🟡",
    "RESOLVED": "🟢",
}
 
def render():
    st.markdown("### Service Requests")
    st.caption("Raise a request or track an existing one")
 
    customer_id = st.session_state.customer_id
 
    col1, col2 = st.columns(2)
 
    # --- RAISE REQUEST ---
    with col1:
        st.markdown("**Raise a request**")
        with st.form("raise_request_form"):
            req_type_label = st.selectbox("Request type", list(REQUEST_TYPES.keys()))
            description = st.text_area("Description", placeholder="Lost my debit card...", height=100)
            submitted = st.form_submit_button("Submit", use_container_width=True)
 
        if submitted:
            req_type = REQUEST_TYPES[req_type_label]
            result = create_service_request(customer_id, req_type, description)
            if "request_id" in result:
                st.success(f"✅ Request #{result['request_id']} raised. Status: {result['status']}")
            else:
                st.error(result.get("detail", "Failed to raise request."))
 
    # --- TRACK REQUEST ---
    with col2:
        st.markdown("**Track a request**")
        with st.form("track_request_form"):
            request_id = st.number_input("Enter request ID", min_value=1, step=1)
            track_submitted = st.form_submit_button("Check status", use_container_width=True)
 
        if track_submitted:
            result = get_service_request(int(request_id))
            if "request_id" in result:
                status = result.get("status", "OPEN")
                icon = STATUS_COLORS.get(status, "⚪")
                st.markdown(f"**Request #{result['request_id']}**")
                st.markdown(f"Type: {result.get('type', '')}")
                st.markdown(f"Status: {icon} {status}")
                st.caption(f"Customer ID: {result.get('customer_id', '')}")
            else:
                st.error(result.get("detail", "Request not found."))