from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from schema.user import UserSearch

from services.user import UserService
from database.database import get_session


router = APIRouter(
    prefix="/api/users",
    tags=["users"]
)

user_service = UserService()

@router.get("/search", response_model=list[UserSearch])
async def search_users(
    username: str,
    session: Session = Depends(get_session)
):
    return user_service.search_users(session,username)

