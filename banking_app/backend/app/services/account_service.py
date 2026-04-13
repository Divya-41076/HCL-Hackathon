FAKE_ACCOUNTS = {}
ACCOUNT_COUNTER = [1]

def create_account(customer_id: int, account_type: str):
    account = {
        "account_id": ACCOUNT_COUNTER[0],
        "customer_id": customer_id,
        "account_type": account_type,
        "balance": 0.0,
        "status": "ACTIVE"
    }
    if customer_id not in FAKE_ACCOUNTS:
        FAKE_ACCOUNTS[customer_id] = []
    FAKE_ACCOUNTS[customer_id].append(account)
    ACCOUNT_COUNTER[0] += 1
    return account

def get_account(account_id: int):
    for accounts in FAKE_ACCOUNTS.values():
        for acc in accounts:
            if acc["account_id"] == account_id:
                return acc
    return None

def add_balance(account_id: int, amount: float):
    account = get_account(account_id)
    if account:
        account["balance"] += amount
    return account

def list_accounts(customer_id: int):
    return FAKE_ACCOUNTS.get(customer_id, [])