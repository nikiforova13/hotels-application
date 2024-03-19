import datetime
from datetime import date

import uvicorn
from fastapi import FastAPI, Query, Depends
from typing import Optional
from pydantic import BaseModel
from app.bookings import bookings_router
from app.users import router_auth
from app.hotels import hotels_router

app = FastAPI()
app.include_router(router_auth)
app.include_router(bookings_router)
app.include_router(hotels_router)


class SHotel(BaseModel):
    address: str
    name: str
    star: int


class HotelsSearchArgs:
    def __init__(
        self,
        location: str,
        date_from: date,
        date_to: date,
        stars: Optional[int] = Query(default=None, ge=1, le=5),
        has_spa: Optional[bool] = None,
    ):
        self.location = location
        self.date_from = date_from
        self.date_to = date_to
        self.stars = stars
        self.has_spa = has_spa


@app.get("/hotels")
def get_hotels(search_args: HotelsSearchArgs = Depends()) -> list[SHotel]:
    hotels = [{"address": "kkkk", "name": "love", "stars": 5}]
    return hotels


class SBooking(BaseModel):
    room_id: int
    date_from: date
    date_to: date


# @app.post("/bookings")
# def add_bookings(booking: SBooking):
#     pass

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8089, reload=True)
