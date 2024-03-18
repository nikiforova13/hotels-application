from fastapi import APIRouter, Request, Depends
from app.bookings.dao import BookingDAO
from app.users.models import Users
from app.users.dependencies import get_current_user

router = APIRouter(prefix="/bookings", tags=["Bookings"])


@router.get("")
async def get_bookings(user: Users = Depends(get_current_user)):  # -> list[SBooking]:
    return await BookingDAO.find_by_filter(user_id=user.id)
