import datetime

from app.database import async_session_maker
import sqlalchemy as sa
from app.bookings.models import Bookings
from app.dao.base import BaseDAO
from app.hotels.rooms.models import Rooms
from app.exceptions import BookingNotFound


class BookingDAO(BaseDAO):
    model = Bookings

    @classmethod
    async def add(
        cls,
        user_id: int,
        room_id: int,
        date_from: datetime.datetime,
        date_to: datetime.datetime,
    ):
        async with async_session_maker() as session:
            booked_rooms = (
                sa.select(Bookings)
                .where(
                    sa.and_(
                        Bookings.room_id == room_id,
                        sa.or_(
                            sa.and_(
                                Bookings.date_from >= date_from,
                                Bookings.date_to <= date_to,
                            ),
                            sa.and_(
                                Bookings.date_from <= date_from,
                                Bookings.date_to >= date_from,
                            ),
                        ),
                    )
                )
                .cte("booked_rooms")
            )
            get_rooms_left = (
                sa.select(
                    (Rooms.quantity - sa.func.count(booked_rooms.c.room_id)).label(
                        "rooms_left"
                    )
                )
                .select_from(Rooms)
                .outerjoin(booked_rooms, booked_rooms.c.room_id == Rooms.id)
                .where(Rooms.id == room_id)
                .group_by(Rooms.quantity, booked_rooms.c.room_id)
            )
        rooms_left = await session.execute(get_rooms_left)
        rooms_left: int = rooms_left.scalar()
        if rooms_left > 0:
            get_price = sa.select(Rooms.price).filter_by(id=room_id)
            price = await session.execute(get_price)
            price: int = price.scalar()
            add_booking = (
                sa.insert(Bookings)
                .values(
                    room_id=room_id,
                    user_id=user_id,
                    date_from=date_from,
                    date_to=date_to,
                    price=price,
                )
                .returning(Bookings)
            )
            new_booking = await session.execute(add_booking)
            await session.commit()
            return new_booking.scalar()
        else:
            return None

    @classmethod
    async def delete_booking(
            cls,
            user_id: int,
            booking_id: int
    ):
        async with async_session_maker() as session:
            get_booking_by_id_for_current_user = await cls.find_one_or_none(id=booking_id, user_id=user_id)
            print(get_booking_by_id_for_current_user)
            if get_booking_by_id_for_current_user:
                del_booking = sa.delete(Bookings).where(Bookings.id==get_booking_by_id_for_current_user.id)
                await session.execute(del_booking)
                await session.commit()
            else:
                raise BookingNotFound()


