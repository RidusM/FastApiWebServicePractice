import datetime
from typing import List

from sqlalchemy.orm import Session  # type: ignore
import datetime
import models
import schemas
from models import Object

dt = datetime.datetime.now()
date_format= "%Y.%m.%d"
time_format= "%H:%M:%S"
dtt = dt.strftime(time_format)
dtd = dt.strftime(date_format)

def get_objects_by_name(session: Session, title: str) -> Object:
    return session.query(Object).filter(Object.title == title).first()


def get_objects(session: Session, skip: int = 0, limit: int = 100) -> List[Object]:
    return session.query(Object).offset(skip).limit(limit).all()


def create_object(session: Session, title: str, location: str, latitude: str, longitude: str, capacity:int):
    db_objects = models.Object(title=title, location=location, latitude=latitude, longitude=longitude, time=dtt, date=dtd, capacity=capacity)
    session.add(db_objects)
    session.commit()
    session.refresh(db_objects)
    return db_objects
