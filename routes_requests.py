from fastapi import APIRouter
from .database import get_connection
from .models import ServiceRequestCreate

router = APIRouter()

@router.post("/request")
def create_request(req: ServiceRequestCreate):
    conn = get_connection()
    conn.execute(
        "INSERT INTO service_requests (customer_id, type, description) VALUES (?, ?, ?)",
        (req.customer_id, req.type, req.description)
    )
    conn.commit()
    conn.close()
    return {"status": "Request created successfully"}

@router.get("/requests/{customer_id}")
def get_requests(customer_id: int):
    conn = get_connection()
    rows = conn.execute(
        "SELECT * FROM service_requests WHERE customer_id = ? ORDER BY created_at DESC",
        (customer_id,)
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]
