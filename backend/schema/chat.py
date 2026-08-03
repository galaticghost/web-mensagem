from pydantic import BaseModel,ConfigDict

from models import ChatType

class CreatePrivateChat(BaseModel):
    user_id: int

class ChatReponse(BaseModel):
    id: int
    display_name: int
    description: str | None
    type: ChatType

    model_config = ConfigDict(from_attributes=True)

class ChatListItem(BaseModel):
    id: int
    type: ChatType
    display_name: str
    description: str | None

class ChatListResponse(BaseModel):
    chats: list[ChatListItem]