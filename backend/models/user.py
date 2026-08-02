from __future__ import annotations
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String
from database.database import Base

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    
    username: Mapped[str] = mapped_column(
        String(30),
        unique=True,
        nullable=False
        )

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False)

    password_hash: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    chats: Mapped[list["ChatMember"]] = relationship(
        back_populates="user"
    )

    messages: Mapped[list["Message"]] = relationship(
        back_populates="sender"
    )

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.username!r}, email={self.email!r})"