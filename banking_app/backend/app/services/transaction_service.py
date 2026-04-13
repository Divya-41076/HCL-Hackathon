FAKE_TRANSACTIONS = []
TRANSACTION_COUNTER = [1]

from app.services.account_service import get_account
from fastapi import HTTPException

def transfer_funds(from_account_id: int, to_account_id: int, amount: float):

    # Rule 1 — from account exists
    from_account = get_account(from_account_id)
    if not from_account:
        raise HTTPException(status_code=404, detail="Source account not found")

    # Rule 2 — to account exists
    to_account = get_account(to_account_id)
    if not to_account:
        raise HTTPException(status_code=404, detail="Destination account not found")

    # Rule 3 — both accounts active
    if from_account["status"] != "ACTIVE" or to_account["status"] != "ACTIVE":
        raise HTTPException(status_code=403, detail="One or both accounts are not active")

    # Rule 4 — no self transfer
    if from_account_id == to_account_id:
        raise HTTPException(status_code=400, detail="Cannot transfer to the same account")

    # Rule 5 — sufficient balance
    if from_account["balance"] < amount:
        raise HTTPException(status_code=400, detail="Insufficient balance")

    # Commit — atomic debit + credit
    from_account["balance"] -= amount
    to_account["balance"] += amount

    transaction = {
        "transaction_id": TRANSACTION_COUNTER[0],
        "from_account_id": from_account_id,
        "to_account_id": to_account_id,
        "amount": amount,
        "type": "TRANSFER",
        "status": "COMPLETED",
        "date": str(__import__("datetime").datetime.utcnow())
    }
    FAKE_TRANSACTIONS.append(transaction)
    TRANSACTION_COUNTER[0] += 1
    return transaction

def get_transactions(account_id: int):
    return [
        t for t in FAKE_TRANSACTIONS
        if t["from_account_id"] == account_id or t["to_account_id"] == account_id
    ]