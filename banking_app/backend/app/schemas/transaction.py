# ─────────────────────────────────────────────────────────────
#  app/schemas/transaction.py
#  Pydantic schemas for Transaction.
#  Used by Person 1 in transaction_service.py and routers/transactions.py.
# ─────────────────────────────────────────────────────────────

from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, Field, model_validator


# ── Input schemas ──────────────────────────────────────────────

class TransferRequest(BaseModel):
    """Body for POST /transactions/transfer"""
    from_account_id: int = Field(..., examples=[1])
    to_account_id: int = Field(..., examples=[3])
    amount: Decimal = Field(..., gt=0, examples=[500.00])

    @model_validator(mode="after")
    def accounts_must_differ(self) -> "TransferRequest":
        """
        Schema-level guard: from and to accounts must differ.
        The service layer also enforces Rule 4, but catching it here
        gives a cleaner 422 before the DB is touched.
        """
        if self.from_account_id == self.to_account_id:
            raise ValueError("from_account_id and to_account_id must be different.")
        return self


# ── Output schemas ─────────────────────────────────────────────

class TransactionOut(BaseModel):
    """Returned by POST /transactions/transfer and GET /accounts/{id}/transactions"""
    transaction_id: int
    from_account_id: int
    to_account_id: int
    amount: Decimal
    type: str
    status: str
    date: datetime

    model_config = {"from_attributes": True}