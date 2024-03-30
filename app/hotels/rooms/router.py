from datetime import datetime

from fastapi import APIRouter

from app.hotels.dao import HotelsDAO
from app.hotels.rooms.schemas import SRooms

router = APIRouter(prefix="/hotels", tags=["Rooms"])


@router.get("/{hotel_id}/rooms")
async def get_rooms_certain_hotel(
    hotel_id: int, date_from: datetime, date_to: datetime
) -> list[SRooms]:
    return await HotelsDAO.get_free_rooms_in_certain_hotel(hotel_id, date_from, date_to)
