import datetime

from fastapi import Request, HTTPException, status, Depends
from jose import jwt, JWTError
from app.database import settings
from app.users.dao import UserDAO


def get_token(requst: Request):
    token = requst.cookies.get("booking_access_token")
    if not token:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)
    return token


async def get_current_user(token: str = Depends(get_token)):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, settings.APGORITHM)
    except JWTError:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)

    expire: str = payload.get("exp")
    if not expire or int(expire) < datetime.datetime.utcnow().timestamp():
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)

    user_id: str = payload.get("sub")
    if not user_id:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)

    user = await UserDAO.find_by_id(int(user_id))
    if not user:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)
    return user

    return "user"
