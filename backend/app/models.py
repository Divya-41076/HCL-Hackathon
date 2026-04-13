from pydantic import BaseModel
from typing import Optional

class LoginRequest(BaseModel):
    email: str
    password: str

class TransferRequest(BaseModel):
    from_account: int
    to_account: int
    amount: float

class ServiceRequestCreate(BaseModel):
    customer_id: int
    type: str
    description: str
