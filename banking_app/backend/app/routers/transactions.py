from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.services.transaction_service import transfer_funds, get_transactions
from app.core.security import decode_token
from app.db.session import get_db

router = APIRouter(prefix="/transactions", tags=["transactions"])

class TransferRequest(BaseModel):
    from_account_id: int
    to_account_id: int
    amount: float

@router.post("/transfer")
def transfer(req: TransferRequest, db: Session = Depends(get_db), current_user_id: int = Depends(decode_token)):
    if req.amount <= 0:
        raise HTTPException(status_code=400, detail="Amount must be greater than zero")
    return transfer_funds(db, req.from_account_id, req.to_account_id, req.amount)

@router.get("/account/{account_id}")
def history(account_id: int, db: Session = Depends(get_db), current_user_id: int = Depends(decode_token)):
    return get_transactions(db, account_id)