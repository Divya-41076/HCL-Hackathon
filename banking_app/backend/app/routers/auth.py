from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.services.auth_service import register_customer, login_customer, get_customer
from app.core.security import decode_token
from app.db.session import get_db

router = APIRouter(prefix="/auth", tags=["auth"])

class RegisterRequest(BaseModel):
    name: str
    email: str
    password: str
    phone: str = None
    address: str = None

class LoginRequest(BaseModel):
    email: str
    password: str

@router.post("/register")
def register(req: RegisterRequest, db: Session = Depends(get_db)):
    customer = register_customer(db, req.name, req.email, req.password, req.phone, req.address)
    if not customer:
        raise HTTPException(status_code=400, detail="Email already registered")
    return {"customer_id": customer.customer_id, "name": customer.name, "email": customer.email}

@router.post("/login")
def login(req: LoginRequest, db: Session = Depends(get_db)):
    result = login_customer(db, req.email, req.password)
    if not result:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    return result

@router.get("/me")
def get_me(current_user_id: int = Depends(decode_token), db: Session = Depends(get_db)):
    customer = get_customer(db, current_user_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return {"customer_id": customer.customer_id, "name": customer.name, "email": customer.email}