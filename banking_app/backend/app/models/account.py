# ─────────────────────────────────────────────────────────────
#  app/models/account.py
#  Table: accounts
#  Relationships:
#    accounts → customers         (Many-to-One)
#    accounts → transactions sent (One-to-Many via from_account_id)
#    accounts → transactions received (One-to-Many via to_account_id)
# ─────────────────────────────────────────────────────────────

from decimal import Decimal
from sqlalchemy import Integer, String, Numeric, ForeignKey, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base


class Account(Base):
    __tablename__ = "accounts"

    # CHECK constraint: balance must never go negative
    __table_args__ = (
        CheckConstraint("balance >= 0", name="ck_accounts_balance_non_negative"),
    )

    account_id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )
    customer_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("customers.customer_id"), nullable=False
    )
    # Allowed values: SAVINGS | CURRENT
    account_type: Mapped[str] = mapped_column(String(20), nullable=False)
    balance: Mapped[Decimal] = mapped_column(
        Numeric(12, 2), nullable=False, default=Decimal("0.00")
    )
    # Allowed values: ACTIVE | FROZEN | CLOSED
    status: Mapped[str] = mapped_column(
        String(20), nullable=False, default="ACTIVE"
    )

    # ── Relationships ──────────────────────────────────────────
    customer: Mapped["Customer"] = relationship(
        "Customer", back_populates="accounts"
    )

    # Transactions where this account is the SENDER (from_account_id)
    sent_transactions: Mapped[list["Transaction"]] = relationship(
        "Transaction",
        foreign_keys="Transaction.from_account_id",
        back_populates="from_account",
    )

    # Transactions where this account is the RECEIVER (to_account_id)
    received_transactions: Mapped[list["Transaction"]] = relationship(
        "Transaction",
        foreign_keys="Transaction.to_account_id",
        back_populates="to_account",
    )

    def __repr__(self) -> str:
        return (
            f"<Account account_id={self.account_id} "
            f"type={self.account_type!r} balance={self.balance} status={self.status!r}>"
        )