from sqlalchemy.orm import Relationship

from app.database import Base
from sqlalchemy import Column, JSON, Integer, String


class Hotels(Base):
    __tablename__ = "hotels"
    id = Column(Integer, primary_key=True, nullable=False)
    location = Column(String, nullable=False)
    name = Column(String, nullable=False)
    services = Column(JSON)
    rooms_quantity = Column(Integer, nullable=False)
    image_id = Column(Integer)
    room = Relationship("Rooms", back_populates="hotel")

    def __str__(self):
        return f"Hotel {self.name}"
