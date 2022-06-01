from typing import Union

from pydantic import BaseModel


class ObjectBase(BaseModel):
    title: str
    location: Union[str, None] = None


class ObjectCreate(ObjectBase):
    pass


class Object(ObjectBase):
    id: int

    class Config:
        orm_mode = True
