# ─────────────────────────────────────────────────────────────
#  app/schemas/customer.py
#  Pydantic schemas for Customer.
#  Used by Person 1 in auth_service.py and routers/auth.py.
# ─────────────────────────────────────────────────────────────

from datetime import datetime
from pydantic import BaseModel, EmailStr, Field


# ── Input schemas (request bodies) ────────────────────────────

class CustomerCreate(BaseModel):
    """Body for POST /auth/register"""
    name: str = Field(..., min_length=1, max_length=100, examples=["Ravi Kumar"])
    email: EmailStr = Field(..., examples=["ravi@demo.com"])
    password: str = Field(..., min_length=6, examples=["demo123"])
    phone: str | None = Field(None, max_length=20, examples=["9876543210"])
    address: str | None = Field(None, max_length=255, examples=["Mumbai"])


class CustomerLogin(BaseModel):
    """Body for POST /auth/login"""
    email: EmailStr = Field(..., examples=["ravi@demo.com"])
    password: str = Field(..., examples=["demo123"])


# ── Output schemas (response bodies) ──────────────────────────

class CustomerOut(BaseModel):
    """Returned after register or wherever customer data is exposed."""
    customer_id: int
    name: str
    email: EmailStr
    phone: str | None = None
    address: str | None = None
    created_at: datetime

    model_config = {"from_attributes": True}


class CustomerOutBrief(BaseModel):
    """Minimal customer info — returned in POST /auth/register response."""
    customer_id: int
    name: str
    email: EmailStr

    model_config = {"from_attributes": True}


# ── Auth response ──────────────────────────────────────────────

class TokenOut(BaseModel):
    """Returned by POST /auth/login"""
    access_token: str
    token_type: str = "bearer"
    customer_id: int