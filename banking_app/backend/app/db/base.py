from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """
    Single declarative base for all ORM models.
    All model classes inherit from this.
    """
    pass


# ── Import every model so SQLAlchemy registers them ──────────
# ORDER MATTERS for FK resolution — import parent tables first.
from app.models.customer import Customer          # noqa: F401, E402
from app.models.bank_staff import BankStaff       # noqa: F401, E402
from app.models.account import Account            # noqa: F401, E402
from app.models.transaction import Transaction    # noqa: F401, E402
from app.models.service_request import ServiceRequest  # noqa: F401, E402