from pydantic import BaseModel,ConfigDict

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
    users_id: list[int]

class ChatListResponse(BaseModel):
    chats: list[ChatListItem]