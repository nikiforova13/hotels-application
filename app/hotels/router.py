from fastapi import APIRouter, Depends
from app.hotels.schemas import SHotels, SHotelsWithFreeRooms
from datetime import datetime
from app.hotels.dao import HotelsDAO

router = APIRouter(prefix="/hotels", tags=["Hotels"])


@router.get("/{location}")
async def get_hotels(
    location: str, date_from: datetime, date_to: datetime
) -> list[SHotelsWithFreeRooms]:
    return await HotelsDAO.get_hotels_with_free_rooms(
        location=location, date_from=date_from, date_to=date_to
    )


@router.get("/id/{hotel_id}")
async def get_hotel_by_id(hotel_id: int) -> SHotels:
    return await HotelsDAO.find_by_id(model_id=hotel_id)