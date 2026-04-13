from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.transaction import Transaction
from app.models.account import Account
import datetime

def transfer_funds(db: Session, from_account_id: int, to_account_id: int, amount: float):
    # Rule 1 — from account exists
    from_account = db.query(Account).filter(Account.account_id == from_account_id).first()
    if not from_account:
        raise HTTPException(status_code=404, detail="Source account not found")

    # Rule 2 — to account exists
    to_account = db.query(Account).filter(Account.account_id == to_account_id).first()
    if not to_account:
        raise HTTPException(status_code=404, detail="Destination account not found")

    # Rule 3 — both active
    if from_account.status != "ACTIVE" or to_account.status != "ACTIVE":
        raise HTTPException(status_code=403, detail="One or both accounts are not active")

    # Rule 4 — no self transfer
    if from_account_id == to_account_id:
        raise HTTPException(status_code=400, detail="Cannot transfer to the same account")

    # Rule 5 — sufficient balance
    if from_account.balance < amount:
        raise HTTPException(status_code=400, detail="Insufficient balance")

    # Atomic commit
    from_account.balance -= amount
    to_account.balance += amount

    transaction = Transaction(
        from_account_id=from_account_id,
        to_account_id=to_account_id,
        amount=amount,
        type="TRANSFER",
        status="COMPLETED",
        date=datetime.datetime.utcnow()
    )
    db.add(transaction)
    db.commit()
    db.refresh(transaction)
    return transaction

def get_transactions(db: Session, account_id: int):
    return db.query(Transaction).filter(
        (Transaction.from_account_id == account_id) |
        (Transaction.to_account_id == account_id)
    ).all()