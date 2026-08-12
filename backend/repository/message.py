from sqlalchemy.orm import Session
from sqlalchemy import select, update

from models import Message, Chat

class MessageRepository:
    """
    Retorna as mensagens de um chat.
    """
    def get_chat_history(
            self,
            session: Session,
            chat_id: int
        ) -> list[Message] | None:

        stmt = (select(Message)
            .where(Message.chat_id == chat_id)
            .order_by(Message.created_at)
        )

        return session.scalars(stmt).all()

    """
    Envia a mensagem para o banco de dados.
    """
    def create(
        self,
        session: Session,
        message: Message
    ) -> Message:
        session.add(message)
        session.flush()

        stmt = (update(Chat)
            .where(
                Chat.id == message.chat_id
            )
            .values(
                last_message_id = message.id,
                last_message_at = message.created_at,
            )
        )

        session.execute(stmt)
        session.commit()

        return message
