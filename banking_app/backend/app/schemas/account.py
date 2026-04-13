# ─────────────────────────────────────────────────────────────
#  app/schemas/account.py
#  Pydantic schemas for Account.
#  Used by Person 1 in account_service.py and routers/accounts.py.
# ─────────────────────────────────────────────────────────────

from decimal import Decimal
from typing import Literal
from pydantic import BaseModel, Field


# ── Input schemas ──────────────────────────────────────────────

class AccountCreate(BaseModel):
    """Body for POST /accounts"""
    customer_id: int = Field(..., examples=[1])
    account_type: Literal["SAVINGS", "CURRENT"] = Field(..., examples=["SAVINGS"])


# ── Output schemas ─────────────────────────────────────────────

class AccountOut(BaseModel):
    """Returned by POST /accounts and GET /customers/{id}/accounts"""
    account_id: int
    customer_id: int
    account_type: str
    balance: Decimal
    status: str

    model_config = {"from_attributes": True}