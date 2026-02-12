from sqlalchemy import String, Date, Numeric
from sqlalchemy.orm import Mapped, mapped_column
from app.infra.db import Base

class Bill(Base):
    __tablename__ = "bills"

    id: Mapped[str] = mapped_column(String(32), primary_key=True)
    due_date: Mapped[str] = mapped_column(Date, nullable=False)
    amount: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    status: Mapped[str] = mapped_column(String(16), nullable=False, default="open")