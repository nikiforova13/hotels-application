import datetime

from pydantic import BaseModel


class SBooking(BaseModel):
    id: int
    room_id: int
    user_id: int
    date_from: datetime.datetime
    date_to: datetime.datetime
    price: int
    total_count: int
    total_days: int
