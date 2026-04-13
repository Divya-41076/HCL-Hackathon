from fastapi import APIRouter, HTTPException
from .database import get_connection

router = APIRouter()

@router.get("/accounts/{customer_id}")
def get_accounts(customer_id: int):
    conn = get_connection()
    rows = conn.execute(
        "SELECT * FROM accounts WHERE customer_id = ?", (customer_id,)
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]

@router.get("/balance/{account_id}")
def get_balance(account_id: int):
    conn = get_connection()
    row = conn.execute(
        "SELECT account_id, account_type, balance, status FROM accounts WHERE account_id = ?",
        (account_id,)
    ).fetchone()
    conn.close()
    if not row:
        raise HTTPException(status_code=404, detail="Account not found")
    return dict(row)
