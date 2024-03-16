from fastapi import APIRouter
from app.database import async_session_maker
from app.bookings.dao import BookingDAO
import sqlalchemy as sa
from app.bookings.schemas import SBooking
router = APIRouter(prefix='/bookings', tags=['Бронирования'])


@router.get("")
async def get_bookings() -> list[SBooking]:
    return await BookingDAO.find_all()
