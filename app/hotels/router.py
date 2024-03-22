from fastapi import APIRouter, Depends
from app.hotels.schemas import SHotels
from datetime import datetime
from app.hotels.dao import HotelsDAO

router = APIRouter(prefix="/hotels", tags=["Hotels"])


@router.get("/{location}")
async def get_hotels(
    location: str, date_from: datetime, date_to: datetime
) -> list[SHotels]:
    return await HotelsDAO.get_hotels_with_free_rooms(
        location=location, date_from=date_from, date_to=date_to
    )
