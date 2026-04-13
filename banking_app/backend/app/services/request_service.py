from sqlalchemy.orm import Session
from app.models.service_request import ServiceRequest

def create_request(db: Session, customer_id: int, type: str, description: str = None):
    request = ServiceRequest(
        customer_id=customer_id,
        type=type,
        description=description,
        status="OPEN"
    )
    db.add(request)
    db.commit()
    db.refresh(request)
    return request

def get_request(db: Session, request_id: int):
    return db.query(ServiceRequest).filter(ServiceRequest.request_id == request_id).first()

def update_status(db: Session, request_id: int, status: str):
    request = get_request(db, request_id)
    if not request:
        return None
    request.status = status
    db.commit()
    db.refresh(request)
    return request

def get_requests_by_customer(db: Session, customer_id: int):
    return db.query(ServiceRequest).filter(ServiceRequest.customer_id == customer_id).all()