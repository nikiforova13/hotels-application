from app.database import Base
from sqlalchemy import Column, JSON, Integer, String, ForeignKey, Date, Computed


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
