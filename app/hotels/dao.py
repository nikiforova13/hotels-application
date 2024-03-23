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
    async def get_all_booked_rooms(cls, date_from: datetime, date_to: datetime):
        """
            -- 	получить все забронированные комнаты в отеле и количество броней для конкретной комнаты room_id
        WITH booked_rooms as (SELECT rooms.id as room_id, hotels.id as hotel_id, count(rooms.id) as count_booked_specific_rooms
        FROM bookings
        LEFT JOIN rooms on bookings.room_id=rooms.id
        LEFT JOIN hotels on rooms.hotel_id=hotels.id
        WHERE bookings.date_from<='2023-05-20' and bookings.date_to >= '2023-06-20' or  bookings.date_from>='2023-05-20' and bookings.date_to <= '2023-06-20'
        GROUP BY rooms.id, hotels.id)
        """
        booked_rooms = (
            sa.select(
                Rooms.id,
                Rooms.hotel_id,
                sa.func.count(Rooms.id).label("count_booked_specific_rooms"),
            )
            .outerjoin(Bookings, Bookings.room_id == Rooms.id)
            .outerjoin(Hotels, Rooms.hotel_id == Hotels.id)
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
                Rooms.hotel_id,
            )
            .cte("booked_rooms")
        )
        return booked_rooms

    @classmethod
    async def get_hotels_with_free_rooms(
        cls, location: str, date_from: datetime, date_to: datetime
    ):
        """
        -- полная информация об отеле + сколько осталось свободных номеров в отеле
        SELECT hotels.id, hotels.name, hotels.image_id, hotels.location,  hotels.services,  hotels.rooms_quantity, hotels.rooms_quantity - coalesce(count_all_not_awailable_room.count_all_booked_rooms,0) as rooms_left
        FROM hotels LEFT JOIN (
                SELECT hotel_id, sum(count_booked_specific_rooms) as count_all_booked_rooms
                FROM booked_rooms
                GROUP BY hotel_id
                ) count_all_not_awailable_room  ON hotels.id=count_all_not_awailable_room.hotel_id 	WHERE hotels.id=1;
        """
        booked_rooms = await cls.get_all_booked_rooms(date_from, date_to)
        count_all_booked_rooms_in_every_hotel = (
            sa.select(
                booked_rooms.c.hotel_id,
                sa.func.sum(booked_rooms.c.count_booked_specific_rooms).label(
                    "count_all_booked_rooms"
                ),
            )
            .select_from(booked_rooms)
            .group_by(booked_rooms.c.hotel_id)
        ).cte("booked_rooms2")
        hotels_with_free_rooms = (
            sa.select(
                Hotels.__table__.columns,
                (
                    Hotels.rooms_quantity
                    - sa.func.coalesce(
                        count_all_booked_rooms_in_every_hotel.c.count_all_booked_rooms,  # count free rooms
                        0,
                    )
                ).label("rooms_left"),
            )
            .outerjoin_from(
                Hotels,
                count_all_booked_rooms_in_every_hotel,
                Hotels.id == count_all_booked_rooms_in_every_hotel.c.hotel_id,
            )
            .where(Hotels.location.like(f"%{location}%"))
        )

        async with async_session_maker() as session:
            all_hotels_by_location = await session.execute(hotels_with_free_rooms)
            return all_hotels_by_location.mappings().all()

    # @classmethod
    # async def get_rooms_in_certain_hotel(
    #     cls, hotel_id: int, date_from: datetime, date_to: datetime
    # ):
    #     free_rooms = await cls.query_for_get_free_rooms(date_from, date_to)
    #     # print(free_rooms)
    #     a = (
    #         sa.select(Rooms.id, Rooms.hotel_id)
    #         .select_from(free_rooms)
    #         .where(Rooms.hotel_id == hotel_id, Rooms.id)
    #         .join(Rooms, free_rooms.c.id == Rooms.id)
    #     )
    #     print(a)
