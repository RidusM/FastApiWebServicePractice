from sqlalchemy import Column, Integer, String, Date, Time
from sqlalchemy.orm import relationship

from database import Base


class Object(Base):
    __tablename__ = "objects"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    date = Column(Date, index=True, nullable=False)
    time = Column(Time, nullable=False)
    location = Column(String, index=True, nullable=True)
    latitude = Column(String, nullable=True)
    longitude = Column(String, nullable=True)

