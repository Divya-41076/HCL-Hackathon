from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.services.request_service import create_request, get_request, update_status, get_requests_by_customer
from app.core.security import decode_token
from app.db.session import get_db

router = APIRouter(prefix="/service-requests", tags=["service-requests"])

class ServiceRequestCreate(BaseModel):
    customer_id: int
    type: str
    description: str = None

class StatusUpdate(BaseModel):
    status: str

@router.post("/")
def create(req: ServiceRequestCreate, db: Session = Depends(get_db), current_user_id: int = Depends(decode_token)):
    return create_request(db, req.customer_id, req.type, req.description)

@router.get("/me")
def get_my_requests(current_user_id: int = Depends(decode_token), db: Session = Depends(get_db)):
    return get_requests_by_customer(db, current_user_id)

@router.get("/{request_id}")
def get(request_id: int, db: Session = Depends(get_db), current_user_id: int = Depends(decode_token)):
    request = get_request(db, request_id)
    if not request:
        raise HTTPException(status_code=404, detail="Request not found")
    return request

@router.put("/{request_id}/status")
def update(request_id: int, body: StatusUpdate, db: Session = Depends(get_db), current_user_id: int = Depends(decode_token)):
    request = update_status(db, request_id, body.status)
    if not request:
        raise HTTPException(status_code=404, detail="Request not found")
    return request