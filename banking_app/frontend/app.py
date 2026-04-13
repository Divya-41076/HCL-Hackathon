import streamlit as st
 
st.set_page_config(page_title="NexaBank", page_icon="🏦", layout="centered")
 
st.markdown("""
<style>
/* Hide default streamlit nav */
[data-testid="stSidebarNav"] { display: none; }
 
/* Global background */
.stApp { background-color: #0B1120; }
 
/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #0D1526 !important;
    border-right: 1px solid #C9A84C33;
}
 
/* Sidebar buttons */
[data-testid="stSidebar"] .stButton > button {
    background-color: transparent !important;
    color: #C9A84C !important;
    border: 1px solid #C9A84C44 !important;
    border-radius: 8px !important;
    font-weight: 500 !important;
    transition: all 0.2s;
}
[data-testid="stSidebar"] .stButton > button:hover {
    background-color: #C9A84C22 !important;
    border-color: #C9A84C !important;
}
[data-testid="stSidebar"] .stButton > button[kind="primary"] {
    background-color: #C9A84C !important;
    color: #0B1120 !important;
    border-color: #C9A84C !important;
}
 
/* Main content text */
h1, h2, h3, .stMarkdown h3 { color: #C9A84C !important; }
p, label, .stCaption, .stText { color: #CBD5E1 !important; }
 
/* Cards / containers */
[data-testid="stMetric"] {
    background-color: #131F35 !important;
    border: 1px solid #C9A84C33 !important;
    border-radius: 10px !important;
    padding: 12px !important;
}
[data-testid="stMetricLabel"] { color: #94A3B8 !important; }
[data-testid="stMetricValue"] { color: #C9A84C !important; }
 
/* Inputs */
.stTextInput > div > div > input,
.stNumberInput > div > div > input,
.stSelectbox > div > div,
.stTextArea textarea {
    background-color: #131F35 !important;
    color: #E2E8F0 !important;
    border: 1px solid #C9A84C44 !important;
    border-radius: 8px !important;
}
 
/* Primary buttons */
.stButton > button[kind="primary"],
.stFormSubmitButton > button {
    background-color: #C9A84C !important;
    color: #0B1120 !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
}
.stButton > button[kind="secondary"] {
    background-color: transparent !important;
    color: #C9A84C !important;
    border: 1px solid #C9A84C55 !important;
    border-radius: 8px !important;
}
 
/* Tabs */
.stTabs [data-baseweb="tab"] {
    color: #94A3B8 !important;
}
.stTabs [aria-selected="true"] {
    color: #C9A84C !important;
    border-bottom-color: #C9A84C !important;
}
 
/* Divider */
hr { border-color: #C9A84C33 !important; }
 
/* Info/success/error boxes */
.stInfo { background-color: #1E2D4A !important; color: #C9A84C !important; border-left-color: #C9A84C !important; }
.stSuccess { background-color: #0F2A1A !important; border-left-color: #4CAF82 !important; }
.stError { background-color: #2A0F0F !important; border-left-color: #CF4444 !important; }
</style>
""", unsafe_allow_html=True)
 
# --- Session state defaults ---
defaults = {
    "token": None,
    "customer_id": None,
    "customer_name": None,
    "page": "login",
    "selected_account_id": None,
    "dashboard_insight": None,
    "history_insight": None,
    "insights_result": None,
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v
 
# --- Sidebar nav (only when logged in) ---
if st.session_state.token:
    with st.sidebar:
        st.markdown("## 🏦 NexaBank")
        st.divider()
 
        nav_items = [
            ("🏠 Home", "dashboard"),
            ("👤 My Accounts", "account"),
            ("💸 Transfer", "transfer"),
            ("📄 Statement", "history"),
            ("🔧 Service Requests", "service_request"),
            ("🤖 AI Insights", "insights"),
        ]
        for label, page_key in nav_items:
            active = st.session_state.page == page_key
            if st.button(label, use_container_width=True,
                         type="primary" if active else "secondary"):
                st.session_state.page = page_key
                st.rerun()
 
        st.divider()
        if st.button("🚪 Logout", use_container_width=True):
            for k in defaults:
                st.session_state[k] = defaults[k]
            st.rerun()
 
# --- Page routing ---
page = st.session_state.page
 
if page == "login":
    from pages import login
    login.render()
 
elif st.session_state.token is None:
    # Not logged in — force back to login
    st.session_state.page = "login"
    st.rerun()
 
elif page == "dashboard":
    from pages import dashboard
    dashboard.render()
 
elif page == "account":
    from pages import account
    account.render()
 
elif page == "transfer":
    from pages import transfer
    transfer.render()
 
elif page == "history":
    from pages import history
    history.render()
 
elif page == "service_request":
    from pages import service_request
    service_request.render()
 
elif page == "insights":
    from pages import insights
    insights.render()