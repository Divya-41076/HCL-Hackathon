@router.get("/me")
def get_my_requests(current_user: Customer = Depends(get_current_user), db: Session = Depends(get_db)):
    requests = db.query(ServiceRequest).filter(
        ServiceRequest.customer_id == current_user.customer_id
    ).all()
    return requests