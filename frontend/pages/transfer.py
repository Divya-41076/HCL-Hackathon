import streamlit as st
from utils.api import get_accounts, transfer_money

def show():
    st.title("💸 Transfer Money")
    st.markdown("---")

    customer_id = st.session_state.get("customer_id")
    accounts = get_accounts(customer_id)
    acc_options = {f"{a['account_type']} (#{a['account_id']})": a["account_id"] for a in accounts}

    from_acc = st.selectbox("From Account", list(acc_options.keys()))
    to_acc_id = st.number_input("To Account ID", min_value=1, step=1)
    amount = st.number_input("Amount (₹)", min_value=1.0, step=100.0)

    if st.button("Transfer", type="primary"):
        from_id = acc_options[from_acc]
        if from_id == to_acc_id:
            st.error("Cannot transfer to the same account.")
            return
        result, status_code = transfer_money(from_id, int(to_acc_id), amount)
        if status_code == 200:
            st.success(f"✅ Transfer {result['status']}! Updated balance: ₹{result['updated_balance']:,.2f}")
            st.balloons()
        else:
            st.error(f"❌ Transfer failed: {result.get('detail', 'Unknown error')}")
