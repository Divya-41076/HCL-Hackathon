# ─────────────────────────────────────────────────────────────
#  Online Banking Hackathon — seed.py
#  Person 4 owns this file.
#
#  Run AFTER uvicorn has started at least once
#  (so create_all has already built the tables), then:
#
#    python seed.py
#
#  Safe to re-run: checks for existing records before inserting.
#  To wipe and re-seed from scratch: delete app.db, restart uvicorn, then run this.
# ─────────────────────────────────────────────────────────────

import sys
import os
from decimal import Decimal
from datetime import datetime, timedelta

# ── Make sure project root is on sys.path ─────────────────────
# This lets us import app.* modules when running `python seed.py` from root.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# ── Load .env before importing anything that reads it ─────────
from dotenv import load_dotenv
load_dotenv()

# ── DB + Models ───────────────────────────────────────────────
from app.db.session import SessionLocal, engine
from app.db.base import Base  # ensures all models are registered

# Import individual model classes for type safety
from app.models.customer import Customer
from app.models.account import Account
from app.models.transaction import Transaction
from app.models.service_request import ServiceRequest
from app.models.bank_staff import BankStaff

# ── Password hashing (reuse Person 1's security module) ───────
from app.core.security import hash_password


# ─────────────────────────────────────────────────────────────
#  Seed data definitions — match EXACTLY with Part 2 §5
# ─────────────────────────────────────────────────────────────

CUSTOMERS = [
    {
        "name": "Ravi Kumar",
        "email": "ravi@demo.com",
        "password": "demo123",
        "phone": "9876543210",
        "address": "Mumbai",
    },
    {
        "name": "Priya Sharma",
        "email": "priya@demo.com",
        "password": "demo123",
        "phone": "9123456780",
        "address": "Delhi",
    },
]

# Accounts are defined AFTER customers are created (need customer_id).
# Balances reflect the state AFTER all 5 seeded transactions have been applied
# so the demo starts with the exact numbers in the spec table.
# Starting balances before transactions:
#   acc1 = 10000 + 500  - 2000 = 8500  → add back to get 10000 pre-tx start
#   We seed final balances directly for simplicity; transaction rows are historical.
ACCOUNTS_TEMPLATE = [
    # (customer_index, account_type, balance, status)
    (0, "SAVINGS",  Decimal("10000.00"), "ACTIVE"),   # account_id=1, Ravi
    (0, "CURRENT",  Decimal("5000.00"),  "ACTIVE"),   # account_id=2, Ravi
    (1, "SAVINGS",  Decimal("8000.00"),  "ACTIVE"),   # account_id=3, Priya
    (1, "CURRENT",  Decimal("3000.00"),  "ACTIVE"),   # account_id=4, Priya
]

# Transactions are inserted as historical records.
# Indices here reference the ACCOUNTS_TEMPLATE list (0-based), not account_id.
TRANSACTIONS_TEMPLATE = [
    # (from_idx, to_idx, amount, status, minutes_ago)
    (0, 2, Decimal("2000.00"), "COMPLETED", 120),
    (1, 3, Decimal("1500.00"), "COMPLETED", 90),
    (2, 0, Decimal("500.00"),  "COMPLETED", 60),
    (0, 3, Decimal("300.00"),  "COMPLETED", 30),
    (2, 1, Decimal("200.00"),  "COMPLETED", 15),
]

SERVICE_REQUESTS_TEMPLATE = [
    # (customer_index, type, description, status)
    (0, "CARD_ISSUE",  "Lost my debit card, please block and reissue.", "OPEN"),
    (1, "STATEMENT",   "Need last 6 months bank statement for visa.",   "IN_PROGRESS"),
]

BANK_STAFF = [
    {
        "email": "admin@bank.com",
        "role": "ADMIN",
        "password": "admin123",
    },
    {
        "email": "support@bank.com",
        "role": "SUPPORT",
        "password": "support123",
    },
]


# ─────────────────────────────────────────────────────────────
#  Helper
# ─────────────────────────────────────────────────────────────

def _exists(session, model, **filters) -> bool:
    """Return True if at least one row matching filters exists."""
    return session.query(model).filter_by(**filters).first() is not None


# ─────────────────────────────────────────────────────────────
#  Main seed function
# ─────────────────────────────────────────────────────────────

def seed():
    # Guarantee tables exist (idempotent — safe to call even if already created)
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        print("\n🌱  Starting seed...\n")

        # ── 1. Bank Staff ──────────────────────────────────────
        print("  👔  Seeding bank_staff...")
        for s in BANK_STAFF:
            if _exists(db, BankStaff, email=s["email"]):
                print(f"       SKIP  {s['email']} already exists.")
                continue
            staff = BankStaff(
                email=s["email"],
                role=s["role"],
                hashed_password=hash_password(s["password"]),
            )
            db.add(staff)
            print(f"       ADD   {s['email']} ({s['role']})")
        db.commit()

        # ── 2. Customers ───────────────────────────────────────
        print("\n  👤  Seeding customers...")
        customer_objects: list[Customer] = []
        for c in CUSTOMERS:
            existing = db.query(Customer).filter_by(email=c["email"]).first()
            if existing:
                print(f"       SKIP  {c['email']} already exists.")
                customer_objects.append(existing)
                continue
            customer = Customer(
                name=c["name"],
                email=c["email"],
                phone=c["phone"],
                address=c["address"],
                hashed_password=hash_password(c["password"]),
                created_at=datetime.utcnow(),
            )
            db.add(customer)
            db.flush()  # assigns customer_id before commit
            customer_objects.append(customer)
            print(f"       ADD   customer_id={customer.customer_id}  {c['name']} <{c['email']}>")
        db.commit()

        # ── 3. Accounts ────────────────────────────────────────
        print("\n  🏦  Seeding accounts...")
        account_objects: list[Account] = []
        for (cust_idx, acc_type, balance, status) in ACCOUNTS_TEMPLATE:
            cust = customer_objects[cust_idx]
            # Idempotency: check by customer + type (each customer has 1 of each type in seed)
            existing = db.query(Account).filter_by(
                customer_id=cust.customer_id,
                account_type=acc_type,
            ).first()
            if existing:
                print(f"       SKIP  account_id={existing.account_id}  customer={cust.name}  {acc_type}")
                account_objects.append(existing)
                continue
            account = Account(
                customer_id=cust.customer_id,
                account_type=acc_type,
                balance=balance,
                status=status,
            )
            db.add(account)
            db.flush()
            account_objects.append(account)
            print(
                f"       ADD   account_id={account.account_id}  "
                f"customer={cust.name}  {acc_type}  balance={balance}  status={status}"
            )
        db.commit()

        # ── 4. Transactions ────────────────────────────────────
        print("\n  💸  Seeding transactions...")
        now = datetime.utcnow()
        for i, (from_idx, to_idx, amount, status, mins_ago) in enumerate(TRANSACTIONS_TEMPLATE):
            from_acc = account_objects[from_idx]
            to_acc   = account_objects[to_idx]
            # Idempotency: skip if a matching tx already exists between same accounts with same amount
            existing = db.query(Transaction).filter_by(
                from_account_id=from_acc.account_id,
                to_account_id=to_acc.account_id,
                amount=amount,
            ).first()
            if existing:
                print(
                    f"       SKIP  tx_id={existing.transaction_id}  "
                    f"from={from_acc.account_id} → to={to_acc.account_id}  amount={amount}"
                )
                continue
            tx = Transaction(
                from_account_id=from_acc.account_id,
                to_account_id=to_acc.account_id,
                amount=amount,
                type="TRANSFER",
                status=status,
                date=now - timedelta(minutes=mins_ago),
            )
            db.add(tx)
            db.flush()
            print(
                f"       ADD   transaction_id={tx.transaction_id}  "
                f"from_account={from_acc.account_id} → to_account={to_acc.account_id}  "
                f"amount={amount}  status={status}"
            )
        db.commit()

        # ── 5. Service Requests ────────────────────────────────
        print("\n  📋  Seeding service_requests...")
        for (cust_idx, req_type, desc, status) in SERVICE_REQUESTS_TEMPLATE:
            cust = customer_objects[cust_idx]
            existing = db.query(ServiceRequest).filter_by(
                customer_id=cust.customer_id,
                type=req_type,
            ).first()
            if existing:
                print(f"       SKIP  request_id={existing.request_id}  {cust.name}  {req_type}")
                continue
            req = ServiceRequest(
                customer_id=cust.customer_id,
                type=req_type,
                description=desc,
                status=status,
            )
            db.add(req)
            db.flush()
            print(
                f"       ADD   request_id={req.request_id}  "
                f"customer={cust.name}  type={req_type}  status={status}"
            )
        db.commit()

        # ── Summary ────────────────────────────────────────────
        print("\n✅  Seed complete!\n")
        print("  Demo login credentials:")
        print("  ┌────────────────────┬────────────────────┬──────────┐")
        print("  │ Name               │ Email              │ Password │")
        print("  ├────────────────────┼────────────────────┼──────────┤")
        print("  │ Ravi Kumar         │ ravi@demo.com      │ demo123  │")
        print("  │ Priya Sharma       │ priya@demo.com     │ demo123  │")
        print("  │ Admin (staff)      │ admin@bank.com     │ admin123 │")
        print("  └────────────────────┴────────────────────┴──────────┘")
        print("\n  Account summary:")
        print("  ┌────────────┬───────────────┬───────────┬────────────┬────────┐")
        print("  │ account_id │ customer      │ type      │ balance    │ status │")
        print("  ├────────────┼───────────────┼───────────┼────────────┼────────┤")
        for acc in account_objects:
            cust_name = next(c.name for c in customer_objects if c.customer_id == acc.customer_id)
            print(
                f"  │ {acc.account_id:<10} │ {cust_name:<13} │ {acc.account_type:<9} │ "
                f"{float(acc.balance):<10.2f} │ {acc.status:<6} │"
            )
        print("  └────────────┴───────────────┴───────────┴────────────┴────────┘")
        print()

    except Exception as exc:
        db.rollback()
        print(f"\n❌  Seed FAILED — rolled back.\n    Error: {exc}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed()