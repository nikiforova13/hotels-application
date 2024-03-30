import sqlalchemy as sa

from app.database import async_session_maker


class BaseDAO:
    model = None

    @classmethod
    async def find_by_id(cls, model_id: int):
        async with async_session_maker() as session:
            query = sa.select(cls.model).filter_by(id=model_id)
            res = await session.execute(query)
            return res.scalar_one_or_none()

    @classmethod
    async def find_one_or_none(cls, **kwargs):
        async with async_session_maker() as session:
            query = sa.select(cls.model).filter_by(**kwargs)
            res = await session.execute(query)
            return res.scalar_one_or_none()

    @classmethod
    async def find_all(cls):
        async with async_session_maker() as session:
            query = sa.select(cls.model)  # select * from bookings;
            bookings = await session.execute(query)
            return bookings.scalars().all()

    @classmethod
    async def find_by_filter(cls, **kwargs):
        async with async_session_maker() as session:
            query = sa.select(cls.model).filter_by(**kwargs)
            res = await session.execute(query)
            return res.scalars().all()

    @classmethod
    async def add(cls, **kwargs):
        async with async_session_maker() as session:
            query = sa.insert(cls.model).values(**kwargs)
            await session.execute(query)
            await session.commit()
