from __future__ import annotations
from database.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Text, ForeignKey, Boolean, UniqueConstraint, Enum

from models.enums import ChatType

class Chat(Base):
    __tablename__ = "chats"

    id: Mapped[int] = mapped_column(primary_key=True)

    type: Mapped[ChatType] = mapped_column(
        Enum(ChatType),
        nullable=False
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    name: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True
    )

    members: Mapped[list["ChatMember"]] = relationship(
        back_populates="chat"
    )

    created_by_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    messages: Mapped[list["Message"]] = relationship(back_populates="chat")

class ChatMember(Base):
    __tablename__ = "chat_members"

    id: Mapped[int] = mapped_column(primary_key=True)

    chat_id: Mapped[int] = mapped_column(ForeignKey("chats.id"))

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    is_admin: Mapped[bool] = mapped_column(
        Boolean,
        default=False
    )

    chat: Mapped["Chat"] = relationship(back_populates="members")

    user: Mapped["User"] = relationship(back_populates="chats")


    __table_args__ = (
        UniqueConstraint(
            "chat_id",
            "user_id",
        ),
    )