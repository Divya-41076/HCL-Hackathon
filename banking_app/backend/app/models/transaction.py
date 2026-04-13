# ─────────────────────────────────────────────────────────────
#  app/models/transaction.py
#  Table: transactions
#  Two FKs to accounts — one for sender, one for receiver.
#  This models debit + credit without a join table.
# ─────────────────────────────────────────────────────────────

from datetime import datetime
from decimal import Decimal
from sqlalchemy import Integer, String, Numeric, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base


class Transaction(Base):
    __tablename__ = "transactions"

    transaction_id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )
    from_account_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("accounts.account_id"), nullable=False
    )
    to_account_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("accounts.account_id"), nullable=False
    )
    amount: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    # Allowed values: TRANSFER | DEPOSIT | WITHDRAWAL
    type: Mapped[str] = mapped_column(
        String(20), nullable=False, default="TRANSFER"
    )
    # Allowed values: PENDING | COMPLETED | FAILED
    status: Mapped[str] = mapped_column(
        String(20), nullable=False, default="PENDING"
    )
    date: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False
    )

    # ── Relationships ──────────────────────────────────────────
    # Must specify foreign_keys explicitly because there are TWO FKs to accounts.
    from_account: Mapped["Account"] = relationship(
        "Account",
        foreign_keys=[from_account_id],
        back_populates="sent_transactions",
    )
    to_account: Mapped["Account"] = relationship(
        "Account",
        foreign_keys=[to_account_id],
        back_populates="received_transactions",
    )

    def __repr__(self) -> str:
        return (
            f"<Transaction transaction_id={self.transaction_id} "
            f"from={self.from_account_id} to={self.to_account_id} "
            f"amount={self.amount} status={self.status!r}>"
        )