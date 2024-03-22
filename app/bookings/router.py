from datetime import datetime

from fastapi import APIRouter, Request, Depends
from app.bookings.dao import BookingDAO
from app.users.models import Users
from app.users.dependencies import get_current_user
from app.exceptions import RoomCannotBeBooked

router = APIRouter(prefix="/bookings", tags=["Bookings"])


@router.get("")
async def get_bookings(user: Users = Depends(get_current_user)):  # -> list[SBooking]:
    return await BookingDAO.find_by_filter(user_id=user.id)


@router.post("")
async def add_booking(
    room_id: int,
    date_from: datetime,
    date_to: datetime,
    user: Users = Depends(get_current_user),
):
    booking = await BookingDAO.add(user.id, room_id, date_from, date_to)
    if not booking:
        raise RoomCannotBeBooked
