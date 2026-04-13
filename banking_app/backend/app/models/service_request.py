# ─────────────────────────────────────────────────────────────
#  app/models/service_request.py
#  Table: service_requests
#  FK to customers (many requests per customer)
# ─────────────────────────────────────────────────────────────

from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base


class ServiceRequest(Base):
    __tablename__ = "service_requests"

    request_id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )
    customer_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("customers.customer_id"), nullable=False
    )
    # Allowed values: CARD_ISSUE | STATEMENT | CHEQUE
    type: Mapped[str] = mapped_column(String(50), nullable=False)
    description: Mapped[str | None] = mapped_column(String(500), nullable=True)
    # Allowed values: OPEN | IN_PROGRESS | RESOLVED
    status: Mapped[str] = mapped_column(
        String(20), nullable=False, default="OPEN"
    )

    # ── Relationship ───────────────────────────────────────────
    customer: Mapped["Customer"] = relationship(
        "Customer", back_populates="service_requests"
    )

    def __repr__(self) -> str:
        return (
            f"<ServiceRequest request_id={self.request_id} "
            f"type={self.type!r} status={self.status!r}>"
        )