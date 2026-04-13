from fastapi import APIRouter, HTTPException
from .database import get_connection
from .models import TransferRequest

router = APIRouter()

@router.post("/transfer")
def transfer(req: TransferRequest):
    conn = get_connection()
    from_acc = conn.execute("SELECT * FROM accounts WHERE account_id = ?", (req.from_account,)).fetchone()
    to_acc = conn.execute("SELECT * FROM accounts WHERE account_id = ?", (req.to_account,)).fetchone()

    if not from_acc or not to_acc:
        conn.execute(
            "INSERT INTO transactions (from_account, to_account, amount, status) VALUES (?, ?, ?, 'FAILED')",
            (req.from_account, req.to_account, req.amount)
        )
        conn.commit()
        conn.close()
        raise HTTPException(status_code=404, detail="Account not found")

    if from_acc["balance"] < req.amount:
        conn.execute(
            "INSERT INTO transactions (from_account, to_account, amount, status) VALUES (?, ?, ?, 'FAILED')",
            (req.from_account, req.to_account, req.amount)
        )
        conn.commit()
        conn.close()
        raise HTTPException(status_code=400, detail="Insufficient balance")

    if req.amount <= 0:
        raise HTTPException(status_code=400, detail="Amount must be positive")

    conn.execute("UPDATE accounts SET balance = balance - ? WHERE account_id = ?", (req.amount, req.from_account))
    conn.execute("UPDATE accounts SET balance = balance + ? WHERE account_id = ?", (req.amount, req.to_account))
    conn.execute(
        "INSERT INTO transactions (from_account, to_account, amount, status) VALUES (?, ?, ?, 'SUCCESS')",
        (req.from_account, req.to_account, req.amount)
    )
    conn.commit()

    updated = conn.execute("SELECT balance FROM accounts WHERE account_id = ?", (req.from_account,)).fetchone()
    conn.close()
    return {"status": "SUCCESS", "updated_balance": updated["balance"]}

@router.get("/transactions/{account_id}")
def get_transactions(account_id: int):
    conn = get_connection()
    rows = conn.execute(
        "SELECT * FROM transactions WHERE from_account = ? OR to_account = ? ORDER BY created_at DESC",
        (account_id, account_id)
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]

@router.get("/transaction/{transaction_id}")
def get_transaction(transaction_id: int):
    conn = get_connection()
    row = conn.execute("SELECT * FROM transactions WHERE transaction_id = ?", (transaction_id,)).fetchone()
    conn.close()
    if not row:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return dict(row)
