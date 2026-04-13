from app.core.security import hash_password, verify_password, create_access_token

FAKE_DB = {}
CUSTOMER_COUNTER = [1]

def register_customer(name: str, email: str, password: str, phone: str = None, address: str = None):
    if email in FAKE_DB:
        return None
    customer = {
        "customer_id": CUSTOMER_COUNTER[0],
        "name": name,
        "email": email,
        "hashed_password": hash_password(password),
        "phone": phone,
        "address": address
    }
    FAKE_DB[email] = customer
    CUSTOMER_COUNTER[0] += 1
    return customer

def login_customer(email: str, password: str):
    customer = FAKE_DB.get(email)
    if not customer:
        return None
    if not verify_password(password, customer["hashed_password"]):
        return None
    token = create_access_token({"sub": customer["customer_id"]})
    return {
        "access_token": token,
        "token_type": "bearer",
        "customer_id": customer["customer_id"]
    }

def get_customer(customer_id: int):
    for customer in FAKE_DB.values():
        if customer["customer_id"] == customer_id:
            return customer
    return None