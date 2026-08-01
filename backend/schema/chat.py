from pydantic import BaseModel

class CreatePrivateChat(BaseModel):
    user_id: int