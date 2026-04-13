from fastapi import APIRouter, HTTPException
from .database import get_connection
from .models import LoginRequest

router = APIRouter()

@router.post("/login")
def login(req: LoginRequest):
    conn = get_connection()
    user = conn.execute(
        "SELECT id, name, email FROM customers WHERE email = ? AND password = ?",
        (req.email, req.password)
    ).fetchone()
    conn.close()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {
        "token": f"token-{user['id']}",
        "customer_id": user["id"],
        "name": user["name"],
        "email": user["email"]
    }
