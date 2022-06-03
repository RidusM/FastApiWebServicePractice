import datetime

from sqlalchemy import Column, Integer, String, Date, Time
from database import Base
from typing import TypedDict

dt = datetime.datetime.now()
date_format= "%Y:%m:%d"
time_format= "%H:%M:%S"
dtt = dt.strftime(time_format)
dtd = dt.strftime(date_format)

class ObjectDict(TypedDict):
    id: int
    title: str
    location: str
    latitude: str
    longitude: str
    date: str
    time: str

class Object(Base):
    __tablename__ = "objects"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    date = Column(String)
    time = Column(String)
    location = Column(String, index=True)
    latitude = Column(String)
    longitude = Column(String)


    def __init__(self, title:str, location:str, latitude:str, longitude:str, date:dtd, time:dtt):
        self.date = date
        self.time = time
        self.title = title
        self.location = location
        self.latitude = latitude
        self.longitude = longitude

    def __repr__(self) -> str:
        return f"{self.title}"

    @property
    def serialize(self) -> ObjectDict:
        return {"id": self.id, "title": self.title, "location": self.location, "latitude": self.latitude, "longitude": self.longitude, "date": self.date, "time": self.time}

