import asyncio

from fastapi import APIRouter, Depends
from app.hotels.schemas import SHotels, SHotelsWithFreeRooms
from datetime import datetime
from app.hotels.dao import HotelsDAO
from fastapi_cache.decorator import cache

router = APIRouter(prefix="/hotels", tags=["Hotels"])


@router.get("/{location}")
@cache(expire=20)
async def get_hotels_by_location_and_time(
    location: str, date_from: datetime, date_to: datetime
) -> list[SHotelsWithFreeRooms]:
    return await HotelsDAO.get_hotels_with_free_rooms(
        location=location, date_from=date_from, date_to=date_to
    )


@router.get("/id/{hotel_id}")
async def get_hotel_by_id(hotel_id: int) -> SHotels:
    return await HotelsDAO.find_by_id(model_id=hotel_id)
