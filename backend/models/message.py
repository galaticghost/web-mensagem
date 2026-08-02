from __future__ import annotations
from database.database import Base
from sqlalchemy import String, DateTime,ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime, UTC

class Message(Base):
    __tablename__ = "messages"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    message: Mapped[str] = mapped_column(
        String(500),
        nullable=False
    )

    #O now é executado apenas quando o python importa o arquivo e
    #como consequência a data fica congelada.
    #O lambda executa cada vez que for criado um novo dado.
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC)
    )

    chat_id: Mapped[int] = mapped_column(ForeignKey("chats.id"))

    chat: Mapped["Chat"] = relationship(back_populates="messages")

    sender_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    sender: Mapped["User"] = relationship(back_populates="messages")