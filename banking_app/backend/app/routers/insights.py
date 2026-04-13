from fastapi import APIRouter, Depends, HTTPException
from app.services.insights_service import generate_spending_insights
from app.services.transaction_service import get_transactions
from app.services.account_service import get_account
from app.core.security import decode_token

router = APIRouter(prefix="/insights", tags=["insights"])

@router.post("/{account_id}")
def get_insights(account_id: int, current_user_id: int = Depends(decode_token)):
    account = get_account(account_id)
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    transactions = get_transactions(account_id)
    insight = generate_spending_insights(transactions, account["balance"])
    return {"insight": insight}