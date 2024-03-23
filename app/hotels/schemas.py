from pydantic import BaseModel


class SHotels(BaseModel):
    id: int
    name: str
    image_id: int
    location: str
    services: list[str]
    rooms_quantity: int


class SHotelsWithFreeRooms(SHotels):
    rooms_left: int | None = None
