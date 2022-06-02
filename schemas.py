from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class ObjectBase(BaseModel):
    title: str
    location: str
    latitude: str
    longitude: str

class ObjectUpdate(BaseModel):
    newtitle: str

class ObjectCreate(ObjectBase):
    pass