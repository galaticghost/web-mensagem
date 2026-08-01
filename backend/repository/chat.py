from sqlalchemy.orm import Session

from models import Chat,ChatMember,ChatType

class ChatRepository:
    def create_private_chat(
            self, 
            session: Session, 
            creator_id: int,
            other_user_id: int,
    ):
        chat = Chat(
            type=ChatType.PRIVATE,
            created_by_id=creator_id
        )

        session.add(chat)
        #O flush envia o chat para o banco de dados, que gera um id para o chat
        session.flush()

        session.add_all([
            ChatMember(
                chat_id=chat.id,
                user_id=creator_id,
                is_admin=False
            ),
            ChatMember(
                chat_id=chat.id,
                user_id=other_user_id,
                is_admin=False
            ),
        ])

        session.commit()
        
        return chat