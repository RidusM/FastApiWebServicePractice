from datetime import datetime

from pydantic import BaseModel


class ObjectBase(BaseModel):
    title: str
    location: str
    latitude: str
    longitude: str

class ObjectCreate(ObjectBase):
    pass