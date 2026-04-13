from fastapi import HTTPException

FAKE_REQUESTS = []
REQUEST_COUNTER = [1]

def create_request(customer_id: int, type: str, description: str = None):
    request = {
        "request_id": REQUEST_COUNTER[0],
        "customer_id": customer_id,
        "type": type,
        "description": description,
        "status": "OPEN"
    }
    FAKE_REQUESTS.append(request)
    REQUEST_COUNTER[0] += 1
    return request

def get_request(request_id: int):
    for r in FAKE_REQUESTS:
        if r["request_id"] == request_id:
            return r
    return None

def update_status(request_id: int, status: str):
    request = get_request(request_id)
    if not request:
        return None
    request["status"] = status
    return request

def get_requests_by_customer(customer_id: int):
    return [r for r in FAKE_REQUESTS if r["customer_id"] == customer_id]