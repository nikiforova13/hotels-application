from datetime import datetime

from app.dao.base import BaseDAO
from app.hotels.models import Hotels
from app.database import async_session_maker
import sqlalchemy as sa
from app.bookings.models import Bookings
from app.hotels.rooms.models import Rooms


class HotelsDAO(BaseDAO):
    model = Hotels

    @classmethod
    async def get_hotels_with_free_rooms(
        cls, location: str, date_from: datetime, date_to: datetime
    ):
        async with async_session_maker() as session:
            free_rooms = (
                sa.select(
                    Rooms.id,
                    Rooms.quantity,
                    Rooms.hotel_id,
                    (Rooms.quantity - sa.func.count(Rooms.id)).label("count_free"),
                )
                .join(Bookings, Rooms.id == Bookings.room_id)
                .where(
                    sa.or_(
                        sa.and_(
                            Bookings.date_from <= date_from, Bookings.date_to >= date_to
                        ),
                        sa.and_(
                            Bookings.date_from >= date_from, Bookings.date_to <= date_to
                        ),
                    )
                )
                .group_by(
                    Rooms.id,
                    Rooms.quantity,
                    Rooms.hotel_id,
                )
                .cte("booked_rooms")
            )
            hotels_with_free_rooms = (
                sa.select(
                    Hotels.__table__.columns,
                    (sa.func.sum(free_rooms.c.count_free)).label("rooms_left"),
                )
                .select_from(free_rooms)
                .join(Hotels, free_rooms.c.hotel_id == Hotels.id)
                .where(Hotels.location.like(f"%{location}%"))
                .group_by(Hotels.id)
            )

            all_hotels_by_location = await session.execute(hotels_with_free_rooms)
            return all_hotels_by_location.mappings().all()
