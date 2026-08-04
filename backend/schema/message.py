from pydantic import BaseModel
from datetime import datetime

class SendMessage(BaseModel):
    content: str

class MessageListItem(BaseModel):
    id: int
    message: str
    chat_id: int
    sender_id: int
    created_at: datetime

class MessageListResponse(BaseModel):
    messages: list[MessageListItem]