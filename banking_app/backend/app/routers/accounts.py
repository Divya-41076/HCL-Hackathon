from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from app.services.account_service import create_account, get_account, list_accounts
from app.core.security import decode_token

router = APIRouter(prefix="/accounts", tags=["accounts"])

class AccountCreate(BaseModel):
    customer_id: int
    account_type: str  # SAVINGS or CURRENT

@router.post("/")
def create(req: AccountCreate, current_user_id: int = Depends(decode_token)):
    account = create_account(req.customer_id, req.account_type)
    return account

@router.get("/{account_id}")
def get(account_id: int, current_user_id: int = Depends(decode_token)):
    account = get_account(account_id)
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    return account

@router.get("/customer/{customer_id}")
def list_by_customer(customer_id: int, current_user_id: int = Depends(decode_token)):
    return list_accounts(customer_id)