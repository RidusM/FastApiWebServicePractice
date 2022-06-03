from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class ObjectBase(BaseModel):
    title: str
    time: str
    date: str
    location: str
    latitude: str
    longitude: str

class ObjectUpdate(BaseModel):
    newtitle: str

class ObjectCreate(BaseModel):
    title: str
    location: str
    latitude: str
    longitude: str