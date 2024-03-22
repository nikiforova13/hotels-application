from pydantic import BaseModel


class SHotels(BaseModel):
    id: int
    name: str
    image_id: int
    location: str
    services: list[str]
    rooms_quantity: int
    rooms_left: int
