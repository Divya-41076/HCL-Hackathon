from sqlalchemy.orm import Session
from app.models.account import Account

def create_account(db: Session, customer_id: int, account_type: str):
    account = Account(
        customer_id=customer_id,
        account_type=account_type,
        balance=0.00,
        status="ACTIVE"
    )
    db.add(account)
    db.commit()
    db.refresh(account)
    return account

def get_account(db: Session, account_id: int):
    return db.query(Account).filter(Account.account_id == account_id).first()

def list_accounts(db: Session, customer_id: int):
    return db.query(Account).filter(Account.customer_id == customer_id).all()