from app.database import Base
from sqlalchemy import Column, JSON, Integer, String, ForeignKey, Date, Computed
from sqlalchemy.orm import relationship


class Bookings(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True)
    room_id = Column(ForeignKey("rooms.id"))
    user_id = Column(ForeignKey("users.id"))
    date_from = Column(Date, nullable=False)
    date_to = Column(Date, nullable=False)
    price = Column(Integer, nullable=False)
    total_count = Column(
        Integer, Computed("(date_to - date_from) * price"), nullable=False
    )
    total_days = Column(Integer, Computed("date_to - date_from"), nullable=False)
    user = relationship("Users", back_populates="booking")

    def __str__(self):
        return f"Booking  {self.id}"
