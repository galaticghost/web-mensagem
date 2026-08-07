from fastapi import status, Depends, APIRouter
from sqlalchemy.orm import Session

from database.database import get_session
from services.user import UserService
from schema import UserLogin, UserCreate,RefreshRequest

user_service = UserService()

router = APIRouter(
    prefix="/api/auth",
    tags=["auth"]
)

@router.post("/login",status_code=status.HTTP_200_OK)
async def login(
    request: UserLogin,
    session: Session = Depends(get_session)
):
    return user_service.login(session,request)

@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(
    request: UserCreate,
    session: Session = Depends(get_session)
):
    return user_service.register(session,request)

@router.post("/logout",status_code=status.HTTP_200_OK)
async def logout(
    refresh_token: RefreshRequest,
    session:Session = Depends(get_session),
):
    return user_service.logout(
        session=session,
        refresh_token=refresh_token.refresh_token
)

@router.post("/refresh", status_code=status.HTTP_200_OK)
async def refresh(
    request: RefreshRequest,
    session: Session = Depends(get_session)
):
    return user_service.refresh_token(
        session=session,
        token=request.refresh_token
    )