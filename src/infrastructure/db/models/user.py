from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column


from src.infrastructure.db.models.base import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(40), nullable=False)
    last_name: Mapped[str] = mapped_column(String(60), nullable=False)
    joined_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now, nullable=False)
