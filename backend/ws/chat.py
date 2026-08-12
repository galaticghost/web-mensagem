from fastapi import APIRouter, WebSocket, Depends, WebSocketDisconnect, HTTPException
from sqlalchemy.orm import Session

from security.dependencies import get_user_from_token
from services.message import MessageService
from services.chat import ChatService
from services.user import UserService
from database.database import get_session
from ws.connection_manager import connection_manager
from errors import MessageError,ChatError

router = APIRouter(
    prefix="/ws",
    tags=["chatws"] #TOCHANGE
)

message_service = MessageService()
chat_service = ChatService()
user_service = UserService()

@router.websocket("/user")
async def websocket(
    websocket: WebSocket,
    session: Session = Depends(get_session),
):  
    token = websocket.query_params.get("token")

    if token is None:
        await websocket.close(
            code=4002,
            reason="TOKEN_MISSING"
        )
        return
    
    user = get_user_from_token(
        session=session,
        token=token,
    )

    if user is None:
        await websocket.close(
            code=4001,
            reason="TOKEN_EXPIRED"
        )
        return

    await connection_manager.connect(websocket,user.id)
    try:
        while True:
            data = await websocket.receive_json()

            message_type = data.get("type")

            if message_type is None:
                await websocket.send_json({
                    "type": "error",
                    "code": "INVALID_MESSAGE"
                })
                continue

            match (message_type):
                case "message":
                    try:
                        message = message_service.send_message(
                            session=session,
                            content=data["content"]["message"],
                            chat_id=data["content"]["chat_id"],
                            user=user
                        )
                    except MessageError as e:
                        await websocket.send_json({
                            "type": "error",
                            "code": e.code
                        })

                    except ChatError as e:
                        await websocket.send_json({
                            "type": "error",
                            "code": e.code
                        })

                    users = chat_service.get_users_in_chat(
                        session=session,
                        chat_id=data["content"]["chat_id"]
                    )

                    users_id =[user.id for user in users]

                    data = {
                        "type": "message",
                        "content" : {
                            "id": message.id,
                            "message": message.message,
                            "chat_id": message.chat_id,
                            "sender_id": message.sender_id,
                            "created_at": message.created_at.isoformat()
                        }
                    }

                    await connection_manager.send_to_users(
                        users_id=users_id,
                        data=data
                    )
                    
    except WebSocketDisconnect:
        connection_manager.disconnect(websocket,user.id)
        