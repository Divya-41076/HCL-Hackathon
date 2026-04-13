import requests
import streamlit as st

BASE_URL = "http://localhost:8000"

def login(email, password):
    res = requests.post(f"{BASE_URL}/login", json={"email": email, "password": password})
    return res.json() if res.status_code == 200 else None

def get_accounts(customer_id):
    res = requests.get(f"{BASE_URL}/accounts/{customer_id}")
    return res.json()

def get_balance(account_id):
    res = requests.get(f"{BASE_URL}/balance/{account_id}")
    return res.json()

def transfer_money(from_acc, to_acc, amount):
    res = requests.post(f"{BASE_URL}/transfer", json={
        "from_account": from_acc, "to_account": to_acc, "amount": amount
    })
    return res.json(), res.status_code

def get_transactions(account_id):
    res = requests.get(f"{BASE_URL}/transactions/{account_id}")
    return res.json()

def create_service_request(customer_id, req_type, description):
    res = requests.post(f"{BASE_URL}/request", json={
        "customer_id": customer_id, "type": req_type, "description": description
    })
    return res.json()

def get_service_requests(customer_id):
    res = requests.get(f"{BASE_URL}/requests/{customer_id}")
    return res.json()

def get_insights(account_id):
    res = requests.get(f"{BASE_URL}/insights/{account_id}")
    return res.json()



def get_accounts():
    return requests.get(f"{BASE_URL}/accounts").json()

def get_balance():
    return requests.get(f"{BASE_URL}/balance").json()