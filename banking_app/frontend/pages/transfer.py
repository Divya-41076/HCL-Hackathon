import streamlit as st
from utils.api_client import get_accounts, transfer, get_account
 
def render():
    st.markdown("### Transfer Money")
    st.caption("Funds transfer between accounts")
 
    customer_id = st.session_state.customer_id
    accounts = get_accounts(customer_id)
 
    if not accounts:
        st.warning("No accounts available for transfer.")
        return
 
    # Build dropdown options
    acc_options = {
        f"{a['account_type'].capitalize()} #{a['account_id']} — ₹{a['balance']:,.2f}": a["account_id"]
        for a in accounts
        if a["status"] == "ACTIVE"
    }
 
    if not acc_options:
        st.warning("No active accounts available.")
        return
 
    with st.form("transfer_form"):
        from_label = st.selectbox("From account", list(acc_options.keys()))
        to_account_id = st.number_input("To account ID", min_value=1, step=1, help="Enter the recipient's account ID")
        amount = st.number_input("Amount (₹)", min_value=0.01, step=0.01, format="%.2f")
        submitted = st.form_submit_button("Transfer", use_container_width=True)
 
    if submitted:
        from_account_id = acc_options[from_label]
 
        # Basic validations on frontend
        if from_account_id == to_account_id:
            st.error("From and To accounts cannot be the same.")
            return
        if amount <= 0:
            st.error("Amount must be greater than zero.")
            return
 
        with st.spinner("Processing transfer..."):
            result = transfer(from_account_id, int(to_account_id), amount)
 
        if "transaction_id" in result:
            st.success("✅ Transfer successful!")
            # Refresh balance for the from account
            updated = get_account(from_account_id)
 
            st.markdown("#### Transfer Confirmation")
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"**Transaction ID:** #{result['transaction_id']}")
                st.markdown(f"**Amount:** ₹{result['amount']:,.2f}")
                st.markdown(f"**Status:** {result['status']}")
            with col2:
                st.metric(
                    f"Updated balance (Acc #{from_account_id})",
                    f"₹{updated['balance']:,.2f}"
                )
        else:
            detail = result.get("detail", "Transfer failed.")
            st.error(f"❌ {detail}")