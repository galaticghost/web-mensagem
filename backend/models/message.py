from __future__ import annotations
from database.database import Base
from sqlalchemy import String, DateTime,ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime

class Message(Base):
    __tablename__ = "messages"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    message: Mapped[str] = mapped_column(
        String(500),
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    chat_id: Mapped[int] = mapped_column(ForeignKey("chats.id"))

    chat: Mapped["Chat"] = relationship(back_populates="messages",
                                            foreign_keys=[chat_id])

    sender_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    sender: Mapped["User"] = relationship(back_populates="messages")