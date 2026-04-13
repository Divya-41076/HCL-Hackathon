from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from app.services.request_service import create_request, get_request, update_status, get_requests_by_customer
from app.core.security import decode_token

router = APIRouter(prefix="/service-requests", tags=["service-requests"])

class ServiceRequestCreate(BaseModel):
    customer_id: int
    type: str
    description: str = None

class StatusUpdate(BaseModel):
    status: str

@router.post("/")
def create(req: ServiceRequestCreate, current_user_id: int = Depends(decode_token)):
    return create_request(req.customer_id, req.type, req.description)

@router.get("/{request_id}")
def get(request_id: int, current_user_id: int = Depends(decode_token)):
    request = get_request(request_id)
    if not request:
        raise HTTPException(status_code=404, detail="Request not found")
    return request

@router.put("/{request_id}/status")
def update(request_id: int, body: StatusUpdate, current_user_id: int = Depends(decode_token)):
    request = update_status(request_id, body.status)
    if not request:
        raise HTTPException(status_code=404, detail="Request not found")
    return request

@router.get("/customer/{customer_id}")
def list_by_customer(customer_id: int, current_user_id: int = Depends(decode_token)):
    return get_requests_by_customer(customer_id)

@router.get("/me")
def get_my_requests(current_user_id: int = Depends(decode_token)):
    return get_requests_by_customer(current_user_id)