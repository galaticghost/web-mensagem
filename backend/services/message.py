from sqlalchemy.orm import Session

from repository import MessageRepository,ChatRepository
from models import Message,User

class MessageService():
    def __init__(self):
        self.message_repository = MessageRepository()
        self.chat_repository = ChatRepository()

    def send_message(
            self,
            session: Session,
            content: str,
            chat_id: int,
            user: User
    ):

        if not self.chat_repository.user_exists_in_chat(
            session=session,
            user_id=user.id,
            chat_id=chat_id
        ):
            return None
        
        message = Message(
            message=content,
            chat_id=chat_id,
            sender_id=user.id
        )
        
        self.message_repository.create(
            session=session,
            message=message
        )
        #TODO retornar direito
        return message