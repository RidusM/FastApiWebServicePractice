import datetime

from sqlalchemy import Column, Integer, String, Date, Time
from database import Base
from typing import TypedDict

class ObjectDict(TypedDict):
    id: int
    title: str
    date: datetime.date
    time: datetime.time
    location: str
    latitude: str
    longitude: str

class Object(Base):
    __tablename__ = "objects"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    date = Column(Date, index=True, nullable=False)
    time = Column(Time, nullable=False)
    location = Column(String, index=True, nullable=True)
    latitude = Column(String, nullable=True)
    longitude = Column(String, nullable=True)

    def __init__(self, id:int, title:str, date:datetime.date, time:datetime.time, location:str, latitude:str, longitude:str):
        self.id = id
        self.title = title
        self.date = date
        self.time = time
        self.location = location
        self.latitude = latitude
        self.longitude = longitude

    def __repr__(self) -> str:
        return f"{self.name}"

    @property
    def serialize(self) -> ObjectDict:
        return {"name": self.name, "price": self.price}

