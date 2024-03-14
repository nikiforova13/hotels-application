
import sqlalchemy as sa
from app.database import async_session_maker

class BaseDAO:
    model = None
    @classmethod
    async def find_all(cls):
        async with async_session_maker() as session:
            query = sa.select(cls.model)  # select * from bookings;
            bookings = await session.execute(query)
            return bookings.scalars().all()