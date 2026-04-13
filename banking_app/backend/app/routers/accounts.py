from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.services.account_service import create_account, get_account, list_accounts
from app.core.security import decode_token
from app.db.session import get_db

router = APIRouter(prefix="/accounts", tags=["accounts"])

class AccountCreate(BaseModel):
    customer_id: int
    account_type: str

@router.post("/")
def create(req: AccountCreate, db: Session = Depends(get_db), current_user_id: int = Depends(decode_token)):
    return create_account(db, req.customer_id, req.account_type)

@router.get("/customer/{customer_id}")
def list_by_customer(customer_id: int, db: Session = Depends(get_db), current_user_id: int = Depends(decode_token)):
    return list_accounts(db, customer_id)

@router.get("/{account_id}")
def get(account_id: int, db: Session = Depends(get_db), current_user_id: int = Depends(decode_token)):
    account = get_account(db, account_id)
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    return account