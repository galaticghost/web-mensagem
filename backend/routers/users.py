from fastapi import APIRouter, Depends
from repository.user import UserRepository
from database.database import get_session
from sqlalchemy.orm import Session
from schema.user import UserSearch

router = APIRouter(
    prefix="/api/users",
    tags=["users"]
)

user_repository = UserRepository()

@router.get("/search", response_model=list[UserSearch])
async def search_users(
    username: str,
    session: Session = Depends(get_session)
):
    if len(username) < 2:
        return []
    return user_repository.search_by_username(session,username)
    