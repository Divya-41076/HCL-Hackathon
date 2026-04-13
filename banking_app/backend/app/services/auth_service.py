from sqlalchemy.orm import Session
from app.models.customer import Customer
from app.core.security import hash_password, verify_password, create_access_token

def register_customer(db: Session, name: str, email: str, password: str, phone: str = None, address: str = None):
    existing = db.query(Customer).filter(Customer.email == email).first()
    if existing:
        return None
    customer = Customer(
        name=name,
        email=email,
        hashed_password=hash_password(password),
        phone=phone,
        address=address
    )
    db.add(customer)
    db.commit()
    db.refresh(customer)
    return customer

def login_customer(db: Session, email: str, password: str):
    customer = db.query(Customer).filter(Customer.email == email).first()
    if not customer:
        return None
    if not verify_password(password, customer.hashed_password):
        return None
    token = create_access_token({"sub": customer.customer_id})
    return {
        "access_token": token,
        "token_type": "bearer",
        "customer_id": customer.customer_id
    }

def get_customer(db: Session, customer_id: int):
    return db.query(Customer).filter(Customer.customer_id == customer_id).first()