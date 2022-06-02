from datetime import datetime

from pydantic import BaseModel


class ObjectBase(BaseModel):
    id: int
    title: str
    date: str
    time: str
    location: str
    latitude: str
    longitude: str