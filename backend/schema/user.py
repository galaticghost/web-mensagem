from pydantic import BaseModel, EmailStr, Field

class UserCreate(BaseModel):
    username: str = Field(
        min_length=3,
        max_length=30,
        pattern=r"^[a-zA-Z0-9_]+$"
    )
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserSearch(BaseModel):
    id: int
    username: str
    email: EmailStr