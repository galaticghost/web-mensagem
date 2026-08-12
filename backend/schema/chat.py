from pydantic import BaseModel,ConfigDict

from datetime import datetime
from models import ChatType

class CreatePrivateChat(BaseModel):
    user_id: int

class CreateGroupChat(BaseModel):
    user_ids: list[int]
    name: str
    description: str

class ChatReponse(BaseModel):
    id: int
    display_name: str
    description: str | None
    type: ChatType

    model_config = ConfigDict(from_attributes=True)

class ChatListItem(BaseModel):
    id: int
    type: ChatType
    display_name: str
    description: str | None
    created_at: datetime
    updated_at: datetime
    last_message_id: int | None
    last_message_at: datetime | None
    users_id: list[int]

class ChatListResponse(BaseModel):
    chats: list[ChatListItem]