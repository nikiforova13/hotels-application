from sqlalchemy import JSON, Column, Computed, Date, ForeignKey, Integer, String
from sqlalchemy.orm import Relationship

from app.database import Base


class Rooms(Base):
    __tablename__ = "rooms"
    id = Column(Integer, primary_key=True, nullable=False)
    hotel_id = Column(ForeignKey("hotels.id"))
    name = Column(String, nullable=False)
    description = Column(String)
    price = Column(Integer, nullable=False)
    services = Column(JSON, nullable=False)
    quantity = Column(Integer)
    image_id = Column(Integer)
    hotel = Relationship("Hotels", back_populates="room")
    bookings = Relationship('Bookings', back_populates='room')
