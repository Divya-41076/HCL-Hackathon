# ─────────────────────────────────────────────────────────────
#  app/schemas/service_request.py
#  Pydantic schemas for ServiceRequest.
#  Used by Person 1 in request_service.py and routers/service_requests.py.
# ─────────────────────────────────────────────────────────────

from typing import Literal
from pydantic import BaseModel, Field


# ── Input schemas ──────────────────────────────────────────────

class ServiceRequestCreate(BaseModel):
    """Body for POST /service-requests"""
    customer_id: int = Field(..., examples=[1])
    type: Literal["CARD_ISSUE", "STATEMENT", "CHEQUE"] = Field(
        ..., examples=["CARD_ISSUE"]
    )
    description: str | None = Field(
        None, max_length=500, examples=["Lost my debit card"]
    )


class ServiceRequestStatusUpdate(BaseModel):
    """Body for PUT /service-requests/{id}/status"""
    status: Literal["OPEN", "IN_PROGRESS", "RESOLVED"] = Field(
        ..., examples=["IN_PROGRESS"]
    )


# ── Output schemas ─────────────────────────────────────────────

class ServiceRequestOut(BaseModel):
    """Returned by POST /service-requests and GET /service-requests/{id}"""
    request_id: int
    customer_id: int
    type: str
    description: str | None = None
    status: str

    model_config = {"from_attributes": True}