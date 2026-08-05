from sqlalchemy.orm import Session
from fastapi import HTTPException,status

from repository import MessageRepository,ChatRepository
from models import Message,User
from errors import MessageError,ChatError

class MessageService:
    def __init__(self):
        self.message_repository = MessageRepository()
        self.chat_repository = ChatRepository()

    """
    Envia uma mensagem para o banco de dados.
    Caso o usuário não esteja no chat em que a mensagem
    deve ser enviada, ela é negada.
    Usada no ws.
    """
    def send_message(
            self,
            session: Session,
            content: str,
            chat_id: int,
            user: User
    ):
        content = content.strip()

        if not content:
            raise MessageError("MESSAGE_EMPTY")

        if len(content) > 500:
            raise MessageError("MESSAGE_TOO_LONG")

        if not self.chat_repository.user_exists_in_chat(
            session=session,
            user_id=user.id,
            chat_id=chat_id
        ):
            raise ChatError("USER_NOT_IN_CHAT")
        
        message = Message(
            message=content,
            chat_id=chat_id,
            sender_id=user.id
        )
        
        self.message_repository.create(
            session=session,
            message=message
        )

        return message