from datetime import datetime

from app.dao.base import BaseDAO
from app.hotels.models import Hotels
from app.database import async_session_maker
import sqlalchemy as sa


class HotelsDAO(BaseDAO):
    model = Hotels
    @classmethod
    async def get_hotels(cls, location: str, date_from: datetime, date_to: datetime):
        async with async_session_maker() as session:
            query = sa.select(cls.model).where(cls.model.location.like(f'%{location}%'))
            all_hotels_by_location = await session.execute(query)
            return all_hotels_by_location.scalars().all()