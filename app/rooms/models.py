from app.database import Base
from sqlalchemy import Column, JSON, Integer, String, ForeignKey, Date, Computed


class Rooms(Base):
    __tablename__ = 'rooms'
    id = Column(Integer, primary_key=True,  nullable=False)
    hotel_id = Column(ForeignKey('hotels.id'))
    name = Column(String, nullable=False)
    description = Column(String)
    price = Column(Integer, nullable=False)
    services = Column(JSON, nullable=False)
    quantity = Column(Integer)
    image_id = Column(Integer)
