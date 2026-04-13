import requests
import streamlit as st

API_BASE = "http://localhost:8000"
MOCK_MODE = False  # Set to False when backend is live


def get_headers():
    token = st.session_state.get("token", "")
    return {"Authorization": f"Bearer {token}"}


# ---------- AUTH ----------


def login(email: str, password: str) -> dict:
    if MOCK_MODE:
        return {"access_token": "mock_token", "token_type": "bearer", "customer_id": 1}
    try:
        r = requests.post(
            f"{API_BASE}/auth/login", json={"email": email, "password": password}
        )
        return r.json()
    except Exception as e:
        return {"detail": str(e)}


def register(
    name: str, email: str, password: str, phone: str = "", address: str = ""
) -> dict:
    if MOCK_MODE:
        return {"customer_id": 1, "name": name, "email": email}
    try:
        r = requests.post(
            f"{API_BASE}/auth/register",
            json={
                "name": name,
                "email": email,
                "password": password,
                "phone": phone,
                "address": address,
            },
        )
        return r.json()
    except Exception as e:
        return {"detail": str(e)}


# ---------- ACCOUNTS ----------


def get_accounts(customer_id: int) -> list:
    if MOCK_MODE:
        return [
            {
                "account_id": 1,
                "account_type": "SAVINGS",
                "balance": 10000.0,
                "status": "ACTIVE",
            },
            {
                "account_id": 2,
                "account_type": "CURRENT",
                "balance": 5000.0,
                "status": "ACTIVE",
            },
        ]
    try:
        r = requests.get(
            f"{API_BASE}/accounts/customer/{customer_id}", headers=get_headers()
        )
        return r.json()
    except Exception as e:
        return []


def get_account(account_id: int) -> dict:
    if MOCK_MODE:
        mock = {
            1: {
                "account_id": 1,
                "account_type": "SAVINGS",
                "balance": 10000.0,
                "status": "ACTIVE",
            },
            2: {
                "account_id": 2,
                "account_type": "CURRENT",
                "balance": 5000.0,
                "status": "ACTIVE",
            },
        }
        return mock.get(
            account_id,
            {
                "account_id": account_id,
                "account_type": "SAVINGS",
                "balance": 0.0,
                "status": "ACTIVE",
            },
        )
    try:
        r = requests.get(f"{API_BASE}/accounts/{account_id}", headers=get_headers())
        return r.json()
    except Exception as e:
        return {"detail": str(e)}


# ---------- TRANSACTIONS ----------


def transfer(from_account_id: int, to_account_id: int, amount: float) -> dict:
    if MOCK_MODE:
        return {
            "transaction_id": 1,
            "from_account_id": from_account_id,
            "to_account_id": to_account_id,
            "amount": amount,
            "status": "COMPLETED",
            "date": "2025-04-13T10:00:00",
        }
    try:
        r = requests.post(
            f"{API_BASE}/transactions/transfer",
            json={
                "from_account_id": from_account_id,
                "to_account_id": to_account_id,
                "amount": amount,
            },
            headers=get_headers(),
        )
        return r.json()
    except Exception as e:
        return {"detail": str(e)}


def get_transactions(account_id: int) -> list:
    if MOCK_MODE:
        return [
            {
                "transaction_id": 1,
                "from_account_id": 1,
                "to_account_id": 3,
                "amount": 2000.0,
                "status": "COMPLETED",
                "date": "2025-04-13T10:00:00",
            },
            {
                "transaction_id": 3,
                "from_account_id": 3,
                "to_account_id": 1,
                "amount": 500.0,
                "status": "COMPLETED",
                "date": "2025-04-12T09:00:00",
            },
            {
                "transaction_id": 5,
                "from_account_id": 1,
                "to_account_id": 4,
                "amount": 1000.0,
                "status": "COMPLETED",
                "date": "2025-04-11T15:00:00",
            },
        ]
    try:
        r = requests.get(
            f"{API_BASE}/transactions/account/{account_id}", headers=get_headers()
        )
        return r.json()
    except Exception as e:
        return []


# ---------- SERVICE REQUESTS ----------


def create_service_request(customer_id: int, req_type: str, description: str) -> dict:
    if MOCK_MODE:
        return {
            "request_id": 1,
            "customer_id": customer_id,
            "type": req_type,
            "status": "OPEN",
        }
    try:
        r = requests.post(
            f"{API_BASE}/service-requests/",
            json={
                "customer_id": customer_id,
                "type": req_type,
                "description": description,
            },
            headers=get_headers(),
        )
        return r.json()
    except Exception as e:
        return {"detail": str(e)}


def get_service_request(request_id: int) -> dict:
    if MOCK_MODE:
        return {
            "request_id": request_id,
            "type": "CARD_ISSUE",
            "status": "OPEN",
            "customer_id": 1,
        }
    try:
        r = requests.get(
            f"{API_BASE}/service-requests/{request_id}", headers=get_headers()
        )
        return r.json()
    except Exception as e:
        return {"detail": str(e)}


# ---------- INSIGHTS ----------


def get_insights(account_id: int) -> dict:
    if MOCK_MODE:
        return {
            "insight": "You spent ₹3,000 this week. Balance dropped 18%. Consider reviewing your outflows — particularly transfers to external accounts."
        }
    try:
        r = requests.post(f"{API_BASE}/insights/{account_id}", headers=get_headers())
        return r.json()
    except Exception as e:
        return {"detail": str(e)}
