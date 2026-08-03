from fastapi import APIRouter, WebSocket, Depends
from sqlalchemy.orm import Session

from security.dependencies import get_user_from_token
from services.message import MessageService
from services.chat import ChatRepository
from database.database import get_session
from ws.connection_manager import connection_manager

router = APIRouter(
    prefix="/ws",
    tags=["chatws"] #TOCHANGE
)

message_service = MessageService()
chat_repository = ChatRepository()

@router.websocket("/user")
async def websocket(
    websocket: WebSocket,
    session: Session = Depends(get_session),
):  
    token = websocket.query_params.get("token")
    
    user = get_user_from_token(
        session=session,
        token=token,
    )

    if user is None:
        await websocket.close(code=1008)
        return

    await connection_manager.connect(websocket,user.id)
    
    while True:
        data = await websocket.receive_json()
        print(connection_manager.active_connections)
        message = message_service.send_message(
            session=session,
            content=data["message"],
            chat_id=data["chat_id"],
            user=user
        )

        users = chat_repository.get_users_in_chat(
            session=session,
            chat_id=data["chat_id"]
        )

        await connection_manager.send_to_chat_members(
            session=session,
            users=users,
            message=message
        )
        