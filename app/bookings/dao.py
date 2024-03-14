from app.database import async_session_maker
import sqlalchemy as sa
from app.bookings.models import Bookings
from app.dao.base import BaseDAO


class BookingDAO(BaseDAO):
    model = Bookings
