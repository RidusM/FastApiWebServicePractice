from datetime import datetime

from pydantic import BaseModel


class ObjectBase(BaseModel):
    id: int
    title: str
    location: str
    latitude: str
    longitude: str