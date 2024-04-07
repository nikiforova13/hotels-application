from sqlalchemy import JSON, Column, Integer, String
from sqlalchemy.orm import Relationship

from app.config.database import Base


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
