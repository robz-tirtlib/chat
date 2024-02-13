from __future__ import annotations

from datetime import datetime

from typing import List

from sqlalchemy import ForeignKey, DateTime, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.infrastructure.db.models.base import Base


class Dialogue(Base):
    __tablename__ = "dialogues"

    id: Mapped[int] = mapped_column(primary_key=True)
    user1_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    user2_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    dialogue_messages: Mapped[List["DialogueMessage"]] = relationship(
        back_populates="dialogue")


class DialogueMessage(Base):
    __tablename__ = "dialogue_messages"

    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str] = mapped_column(String(40), nullable=False)
    dialogue_id: Mapped[int] = mapped_column(ForeignKey("dialogues.id"))
    sender_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    sent_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now, nullable=False)
    dialogue: Mapped["Dialogue"] = relationship(
        back_populates="dialogue_messages")
