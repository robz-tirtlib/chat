from __future__ import annotations

from datetime import datetime

from fastapi_users.db import SQLAlchemyBaseUserTableUUID

from sqlalchemy import DateTime, String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from src.infrastructure.db.models.base import Base


class User(SQLAlchemyBaseUserTableUUID, Base):
    # __tablename__ = "user"
    # is inherited from SQLAlchemyBaseUserTableUUID

    first_name: Mapped[str] = mapped_column(String(40), nullable=False)
    last_name: Mapped[str] = mapped_column(String(60), nullable=False)
    joined_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now, nullable=False)
