from sqlalchemy.orm import Session
from sqlalchemy import select

from models import Message

class MessageRepository:
    def get_chat_history(
            self,
            session: Session,
            chat_id: int
        ):

        stmt = (select(Message)
            .where(Message.chat_id == chat_id)
            .order_by(Message.created_at)
        )

        return session.scalars(stmt).all()

    def create(
            self,
            session: Session,
            message: Message
        ):
        session.add(message)
        session.commit()
        session.refresh(message)

        return message
