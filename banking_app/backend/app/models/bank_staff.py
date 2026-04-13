# ─────────────────────────────────────────────────────────────
#  app/models/bank_staff.py
#  Table: bank_staff
#  Standalone — no FK to any other table by design.
#  Staff never own accounts; decoupled from customer domain.
# ─────────────────────────────────────────────────────────────

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base


class BankStaff(Base):
    __tablename__ = "bank_staff"

    staff_id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    # Allowed values: ADMIN | SUPPORT
    role: Mapped[str] = mapped_column(String(20), nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)

    def __repr__(self) -> str:
        return f"<BankStaff staff_id={self.staff_id} email={self.email!r} role={self.role!r}>"