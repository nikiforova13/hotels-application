from fastapi import APIRouter
from app.database import async_session_maker
from app.bookings.dao import BookingDAO
import sqlalchemy as sa

router = APIRouter(prefix='/bookings', tags=['Бронирования'])


@router.get("")
async def get_bookings():
    return await BookingDAO.find_all()
