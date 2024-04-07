from datetime import datetime

from fastapi import APIRouter, BackgroundTasks, Depends
from fastapi_versioning import version
from pydantic import parse_obj_as

from app.bookings.dao import BookingDAO
from app.bookings.schemas import SBooking
from app.exceptions import RoomCannotBeBooked
from app.tasks_celery.tasks import send_booking_confirmation_template
from app.users.dependencies import get_current_user
from app.users.models import Users

router = APIRouter(prefix="/bookings", tags=["Bookings"])


@version(1)
@router.get("")
async def get_bookings(user: Users = Depends(get_current_user)) -> list[SBooking]:
    return await BookingDAO.find_by_filter(user_id=user.id)


@version(1)
@router.post("")
async def add_booking(
    task: BackgroundTasks,
    room_id: int,
    date_from: datetime,
    date_to: datetime,
    user: Users = Depends(get_current_user),
) -> SBooking:
    booking = await BookingDAO.add(user.id, room_id, date_from, date_to)
    if not booking:
        raise RoomCannotBeBooked
    booking_dict = parse_obj_as(SBooking, booking).dict()
    # Celery:
    send_booking_confirmation_template.delay(booking_dict, user.email)
    # BackgroundTasks
    # task.add_task(send_booking_confirmation_template, booking_dict, user.email)
    return booking


@version(2)
@router.delete("/{booking_id}")
async def delete_booking(
    booking_id: int, user: Users = Depends(get_current_user)
) -> None:
    return await BookingDAO.delete_booking(user.id, booking_id)
