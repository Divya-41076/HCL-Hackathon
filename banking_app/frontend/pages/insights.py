import streamlit as st
from utils.api_client import get_accounts, get_insights
 
def render():
    st.markdown("### AI Insights")
    st.caption("Groq AI-powered spending analysis for your account")
 
    customer_id = st.session_state.customer_id
    accounts = get_accounts(customer_id)
 
    if not accounts:
        st.info("No accounts found.")
        return
 
    options = {f"{a['account_type'].capitalize()} #{a['account_id']}": a["account_id"] for a in accounts}
    selected_label = st.selectbox("Select account", list(options.keys()))
    selected_id = options[selected_label]
 
    if st.button("🤖 Generate Insight", use_container_width=True):
        with st.spinner("Analysing your transactions..."):
            result = get_insights(selected_id)
        insight = result.get("insight", "No insight available.")
        st.session_state["insights_result"] = insight
 
    if st.session_state.get("insights_result"):
        st.markdown(
            f"""
            <div style="background:#EEEDFE;border-radius:10px;padding:16px 18px;
                        font-size:14px;color:#3C3489;line-height:1.7;margin-top:10px">
                🤖 {st.session_state['insights_result']}
            </div>
            """,
            unsafe_allow_html=True,
        )