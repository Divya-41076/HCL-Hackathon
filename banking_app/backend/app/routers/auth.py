@router.get("/me")
def get_me(current_user: Customer = Depends(get_current_user)):
    return {
        "customer_id": current_user.customer_id,
        "name": current_user.name,
        "email": current_user.email,
        "phone": current_user.phone,
        "address": current_user.address
    }