from fastapi import WebSocket

from models import User, Message
from schema import RefreshResponse

class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[int, list[WebSocket]] = {}

    async def connect(self,websocket: WebSocket, user_id: int):
        await websocket.accept()
        self.active_connections.setdefault(user_id,[]).append(websocket)


    def disconnect(self,websocket: WebSocket, user_id: int):
        ws_list = self.active_connections.get(user_id)

        if ws_list is None:
            return

        if websocket in ws_list:
            ws_list.remove(websocket)

        if len(ws_list) == 0:
            del self.active_connections[user_id]

    async def send_to_chat_members(
            self,
            users: list[User],
            message: Message
    ):
        for user in users:
            ws_list = self.active_connections.get(user.id)
            if ws_list is None:
                continue
            for ws_conn in ws_list.copy():
                try:
                    await ws_conn.send_json({
                        "type": "message",
                        "content" : {
                            "id": message.id,
                            "message": message.message,
                            "chat_id": message.chat_id,
                            "sender_id": message.sender_id,
                            "created_at": message.created_at.isoformat()
                        }
                    })
                except Exception:
                    self.disconnect(ws_conn, user.id)

connection_manager = ConnectionManager()
                