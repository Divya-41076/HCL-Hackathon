from fastapi import APIRouter
from .database import get_connection

router = APIRouter()

@router.get("/insights/{account_id}")
def get_insights(account_id: int):
    conn = get_connection()
    rows = conn.execute(
        "SELECT * FROM transactions WHERE from_account = ? OR to_account = ? ORDER BY created_at DESC LIMIT 10",
        (account_id, account_id)
    ).fetchall()
    conn.close()

    if not rows:
        return {"summary": "No transactions found.", "total_spent": 0, "total_received": 0, "unusual": []}

    total_spent = sum(r["amount"] for r in rows if r["from_account"] == account_id)
    total_received = sum(r["amount"] for r in rows if r["to_account"] == account_id)
    debits = [r["amount"] for r in rows if r["from_account"] == account_id]
    avg_debit = (sum(debits) / len(debits)) if debits else 0

    unusual = []
    for r in rows:
        if r["from_account"] == account_id and r["amount"] > avg_debit * 2 and len(debits) > 1:
            unusual.append({"transaction_id": r["transaction_id"], "amount": r["amount"]})

    summary = f"You spent ₹{total_spent:.0f} recently. You received ₹{total_received:.0f}."
    if unusual:
        summary += f" {len(unusual)} unusual transaction(s) detected."

    return {
        "summary": summary,
        "total_spent": total_spent,
        "total_received": total_received,
        "unusual": unusual,
        "transactions": [dict(r) for r in rows]
    }
