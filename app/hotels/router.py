from fastapi import APIRouter, Depends
from pydantic import BaseModel
from datetime import datetime
from app.hotels.dao import HotelsDAO
router = APIRouter(prefix="/hotels", tags=["Hotels"])


class SHotels(BaseModel):
    id: int
    name: str
    image_id: int
    location: str
    services: list[str]
    rooms_quantity: int
    # rooms_left: int


@router.get('/{location}')
async def get_hotels(location: str, date_from: datetime | None = None, date_to: datetime| None = None) -> list[SHotels]:
    return await HotelsDAO.get_hotels(location=location, date_from=date_from, date_to=date_to)

