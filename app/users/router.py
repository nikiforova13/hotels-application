from fastapi import APIRouter, HTTPException, status, Response, Depends

from app.users.auth import (
    get_password_hash,
    verify_password,
    authenticate_user,
    create_access_token,
)
from app.users.schemas import SUserAuth
from app.users.dao import UserDAO
from app.users.dependencies import get_current_user
from app.users.models import Users
from app.exceptions import UserAlreadyExistsException, IncorrectEmailOrPasswordException

router = APIRouter(prefix="/auth", tags=["Register Users"])


@router.post("/register")
async def register_user(user_data: SUserAuth):
    existing_user = await UserDAO.find_one_or_none(email=user_data.email)
    if existing_user:
        raise UserAlreadyExistsException
    hashed_password = get_password_hash(password=user_data.password)
    await UserDAO.add(email=user_data.email, hashed_password=hashed_password)


@router.post("/login")
async def login_user(user_data: SUserAuth, response: Response):
    user = await authenticate_user(user_data.email, user_data.password)
    if not user:
        raise IncorrectEmailOrPasswordException
    access_token = create_access_token({"sub": str(user.id)})
    response.set_cookie("booking_access_token", access_token, httponly=True)
    return access_token


@router.post("/logout")
async def logout_user(response: Response):
    response.delete_cookie("booking_access_token")


@router.get("/current_user")
async def get_current_user(current_user: Users = Depends(get_current_user)):
    return current_user
